import os
import time
import threading

import serial
import serial.tools.list_ports as sports

from PyQt5 import QtCore, QtWidgets


SOH = 0x01
STX = 0x02
EOT = 0x04
ACK = 0x06
NAK = 0x15
CAN = 0x18
CRC_REQ = ord('C')
PAD = 0x1A


def crc16_ccitt(data: bytes) -> int:
    crc = 0
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc


class YModemBurnWorker(QtCore.QThread):
    log_signal = QtCore.pyqtSignal(str)
    progress_signal = QtCore.pyqtSignal(int)
    result_signal = QtCore.pyqtSignal(bool, str)

    def __init__(self, port: str, baud: int, file_path: str, parent=None):
        super().__init__(parent)
        self.port = port
        self.baud = int(baud)
        self.file_path = file_path
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        ser = None
        try:
            if not os.path.isfile(self.file_path):
                raise FileNotFoundError(f"文件不存在: {self.file_path}")

            file_size = os.path.getsize(self.file_path)
            file_name = os.path.basename(self.file_path)
            if file_size <= 0:
                raise ValueError("固件文件为空")

            self.log_signal.emit(f"打开串口 {self.port} @ {self.baud}")
            ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.2,
                write_timeout=2,
            )
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            with open(self.file_path, "rb") as fw:
                self._send_ymodem(ser, fw, file_name, file_size)

            if self._stop_event.is_set():
                self.result_signal.emit(False, "烧录已取消")
            else:
                self.progress_signal.emit(100)
                self.result_signal.emit(True, "烧录完成")
        except Exception as exc:
            self.result_signal.emit(False, f"烧录失败: {exc}")
        finally:
            if ser is not None:
                try:
                    ser.close()
                except Exception:
                    pass

    def _send_ymodem(self, ser: serial.Serial, fw, file_name: str, file_size: int):
        self._wait_for_byte(ser, CRC_REQ, timeout=15.0, stage="等待目标机发送'C'启动Ymodem")

        info = f"{file_name}\0{file_size}".encode("ascii", errors="ignore")
        header_data = info[:128].ljust(128, b"\x00")
        self._send_packet_with_retry(ser, block_no=0, payload=header_data, use_1k=False)

        sent = 0
        block_no = 1
        while not self._stop_event.is_set():
            raw = fw.read(1024)
            if not raw:
                break
            actual_len = len(raw)
            payload = raw.ljust(1024, bytes([PAD]))
            self._send_packet_with_retry(ser, block_no=block_no, payload=payload, use_1k=True)

            sent += actual_len
            progress = int((sent / file_size) * 100)
            self.progress_signal.emit(max(1, min(progress, 99)))

            block_no = (block_no + 1) % 256

        if self._stop_event.is_set():
            raise RuntimeError("用户中止")

        self._send_eot(ser)
        self._wait_for_byte(ser, CRC_REQ, timeout=10.0, stage="等待目标机请求结束帧")

        end_data = b"\x00" * 128
        self._send_packet_with_retry(ser, block_no=0, payload=end_data, use_1k=False)

    def _send_packet_with_retry(self, ser: serial.Serial, block_no: int, payload: bytes, use_1k: bool):
        if use_1k and len(payload) != 1024:
            raise ValueError("1K数据包长度必须是1024")
        if (not use_1k) and len(payload) != 128:
            raise ValueError("128字节数据包长度必须是128")

        start_flag = STX if use_1k else SOH
        packet = bytearray()
        packet.append(start_flag)
        packet.append(block_no & 0xFF)
        packet.append(0xFF - (block_no & 0xFF))
        packet.extend(payload)
        crc = crc16_ccitt(payload)
        packet.append((crc >> 8) & 0xFF)
        packet.append(crc & 0xFF)

        for _ in range(12):
            if self._stop_event.is_set():
                raise RuntimeError("用户中止")
            ser.write(packet)
            ser.flush()
            resp = self._read_one(ser, timeout=2.5)
            if resp == ACK:
                return
            if resp == CAN:
                raise RuntimeError("目标机取消传输")
        raise TimeoutError(f"数据包确认超时: block={block_no}")

    def _send_eot(self, ser: serial.Serial):
        for _ in range(12):
            if self._stop_event.is_set():
                raise RuntimeError("用户中止")
            ser.write(bytes([EOT]))
            ser.flush()
            resp = self._read_one(ser, timeout=2.0)
            if resp == NAK:
                ser.write(bytes([EOT]))
                ser.flush()
                resp2 = self._read_one(ser, timeout=2.0)
                if resp2 == ACK:
                    return
            elif resp == ACK:
                return
            elif resp == CAN:
                raise RuntimeError("目标机取消传输")
        raise TimeoutError("结束帧EOT握手失败")

    def _wait_for_byte(self, ser: serial.Serial, expected: int, timeout: float, stage: str):
        start = time.time()
        while (time.time() - start) < timeout:
            if self._stop_event.is_set():
                raise RuntimeError("用户中止")
            value = self._read_one(ser, timeout=0.2)
            if value is None:
                continue
            if value == expected:
                return
            if value == CAN:
                raise RuntimeError("目标机取消传输")
        raise TimeoutError(stage)

    @staticmethod
    def _read_one(ser: serial.Serial, timeout: float):
        end_at = time.time() + timeout
        while time.time() < end_at:
            data = ser.read(1)
            if data:
                return data[0]
        return None


class MainWindowToolBurnYmodem:
    def __init__(self, main_window):
        self.mw = main_window
        self.worker = None

        self._build_tab_if_needed()
        self._bind_events()
        self.refresh_ports()

    def _build_tab_if_needed(self):
        tab_widget = getattr(self.mw, "tabWidget_3", None)
        if tab_widget is None:
            return

        tab = getattr(self.mw, "tab_tools_burn", None)
        if tab is None:
            tab = QtWidgets.QWidget()
            tab.setObjectName("tab_tools_burn")
            tab_widget.addTab(tab, "烧录")

        if tab.layout() is not None:
            return

        main_layout = QtWidgets.QVBoxLayout(tab)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        group_serial = QtWidgets.QGroupBox("串口设置", tab)
        serial_layout = QtWidgets.QGridLayout(group_serial)
        lbl_port = QtWidgets.QLabel("串口", group_serial)
        lbl_baud = QtWidgets.QLabel("波特率", group_serial)
        self.mw.comboBox_tools_burn_com = QtWidgets.QComboBox(group_serial)
        self.mw.comboBox_tools_burn_baud = QtWidgets.QComboBox(group_serial)
        self.mw.comboBox_tools_burn_baud.setEditable(True)
        self.mw.comboBox_tools_burn_baud.addItems(["115200", "230400", "460800", "921600"])
        self.mw.pushButton_tools_burn_scan = QtWidgets.QPushButton("刷新串口", group_serial)
        serial_layout.addWidget(lbl_port, 0, 0)
        serial_layout.addWidget(self.mw.comboBox_tools_burn_com, 0, 1)
        serial_layout.addWidget(lbl_baud, 0, 2)
        serial_layout.addWidget(self.mw.comboBox_tools_burn_baud, 0, 3)
        serial_layout.addWidget(self.mw.pushButton_tools_burn_scan, 0, 4)

        group_file = QtWidgets.QGroupBox("固件文件", tab)
        file_layout = QtWidgets.QHBoxLayout(group_file)
        self.mw.lineEdit_tools_burn_file = QtWidgets.QLineEdit(group_file)
        self.mw.lineEdit_tools_burn_file.setPlaceholderText("请选择待烧录的固件文件")
        self.mw.pushButton_tools_burn_browse = QtWidgets.QPushButton("选择文件", group_file)
        file_layout.addWidget(self.mw.lineEdit_tools_burn_file)
        file_layout.addWidget(self.mw.pushButton_tools_burn_browse)

        action_layout = QtWidgets.QHBoxLayout()
        self.mw.pushButton_tools_burn_start = QtWidgets.QPushButton("开始烧录", tab)
        self.mw.pushButton_tools_burn_stop = QtWidgets.QPushButton("停止", tab)
        self.mw.pushButton_tools_burn_stop.setEnabled(False)
        self.mw.progressBar_tools_burn = QtWidgets.QProgressBar(tab)
        self.mw.progressBar_tools_burn.setRange(0, 100)
        self.mw.progressBar_tools_burn.setValue(0)
        action_layout.addWidget(self.mw.pushButton_tools_burn_start)
        action_layout.addWidget(self.mw.pushButton_tools_burn_stop)
        action_layout.addWidget(self.mw.progressBar_tools_burn)

        self.mw.textBrowser_tools_burn_log = QtWidgets.QTextBrowser(tab)

        main_layout.addWidget(group_serial)
        main_layout.addWidget(group_file)
        main_layout.addLayout(action_layout)
        main_layout.addWidget(self.mw.textBrowser_tools_burn_log)

        tab_widget = self.mw.tabWidget_3
        if tab_widget.indexOf(tab) < 0:
            tab_widget.addTab(tab, "烧录")
        else:
            tab_widget.setTabText(tab_widget.indexOf(tab), "烧录")

    def _bind_events(self):
        if not hasattr(self.mw, "pushButton_tools_burn_scan"):
            return
        self.mw.pushButton_tools_burn_scan.clicked.connect(self.refresh_ports)
        self.mw.pushButton_tools_burn_browse.clicked.connect(self.pick_firmware_file)
        self.mw.pushButton_tools_burn_start.clicked.connect(self.start_burn)
        self.mw.pushButton_tools_burn_stop.clicked.connect(self.stop_burn)

    def append_log(self, msg: str):
        now = time.strftime("%H:%M:%S")
        self.mw.textBrowser_tools_burn_log.append(f"[{now}] {msg}")

    def refresh_ports(self):
        combo = getattr(self.mw, "comboBox_tools_burn_com", None)
        if combo is None:
            return
        current = combo.currentText().strip()
        combo.clear()
        ports = [p.device for p in sports.comports()]
        combo.addItems(ports)
        if current and current in ports:
            combo.setCurrentText(current)
        self.append_log(f"检测到串口: {', '.join(ports) if ports else '无'}")

    def pick_firmware_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.mw,
            "选择固件文件",
            "",
            "固件文件 (*.bin *.hex *.img *.fw);;所有文件 (*.*)",
        )
        if path:
            self.mw.lineEdit_tools_burn_file.setText(path)
            self.append_log(f"已选择固件: {path}")

    def start_burn(self):
        if self.worker is not None and self.worker.isRunning():
            self.append_log("烧录任务正在运行")
            return

        port = self.mw.comboBox_tools_burn_com.currentText().strip()
        baud_text = self.mw.comboBox_tools_burn_baud.currentText().strip() or "115200"
        file_path = self.mw.lineEdit_tools_burn_file.text().strip()

        if not port:
            self.append_log("请先选择串口")
            return
        if not os.path.isfile(file_path):
            self.append_log("请选择有效固件文件")
            return

        try:
            baud = int(baud_text)
        except ValueError:
            self.append_log("波特率必须是整数")
            return

        self.worker = YModemBurnWorker(port=port, baud=baud, file_path=file_path, parent=self.mw)
        self.worker.log_signal.connect(self.append_log)
        self.worker.progress_signal.connect(self.mw.progressBar_tools_burn.setValue)
        self.worker.result_signal.connect(self._on_burn_result)

        self.mw.progressBar_tools_burn.setValue(0)
        self.mw.pushButton_tools_burn_start.setEnabled(False)
        self.mw.pushButton_tools_burn_stop.setEnabled(True)
        self.append_log("开始Ymodem烧录")
        self.worker.start()

    def stop_burn(self):
        if self.worker is not None and self.worker.isRunning():
            self.worker.stop()
            self.append_log("已请求停止烧录")

    def _on_burn_result(self, success: bool, message: str):
        self.append_log(message)
        self.mw.pushButton_tools_burn_start.setEnabled(True)
        self.mw.pushButton_tools_burn_stop.setEnabled(False)
        if not success:
            self.mw.progressBar_tools_burn.setValue(0)
