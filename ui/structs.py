import struct 
import ctypes
import time
import numpy as np
import pandas as pd
from funs.fun_chy2 import *
from funs.fun_sate import *
from PyQt5 import QtWidgets, QtGui, QtCore
# 三轴转台结构体
import serial
import time







# 结构体 通用装订规则
class struct_general_bind:
    def __init__(self):
        self.struct_path = './'
        self.struct_name = 'general_bind'
        self.struct_decode = 'xcbB?hHiIlLqQfdspPtyY'
        self.struct_format = '<'
        self.struct_packRule = ''
        self.struct_len = 0
        self.struct_sendHz = 1
        self.struct_packList = []
        self.struct_paraList = []
        self.struct_titlList = []
        self.struct_dataList = []
        self.struct_buttonList = []
        self.struct_default = ''
        self.struct_typeCheck = 'None'
        self.struct_ruleCheck = False
        self.struct_debugList = []
        self.struct_debugFlag = False
        
    def read_struct_file(self,struct_file):
        self.init_structList()
        if len(struct_file)==0:
            return 
        for line in struct_file.split('\n'):
            split_data = line.split()
            if len(split_data)<3:
                continue
            if line.startswith('#'):
                tar = split_data[1].lower()
                val = split_data[2]
                if 'default' in tar:
                    self.struct_default = ''.join(split_data[2:])
                if ('rulehead' in tar)|('format' in tar):
                    self.struct_format = try_return_format(val)
                if ('send_hz' in tar)|('autohz' in tar):
                    self.struct_sendHz = try_return_int(val,1)
                if 'sum' in tar.lower():
                    self.struct_typeCheck = 'sum'
                    self.struct_ruleCheck = try_return_checkRule(val)
                if 'crc' == tar.lower():
                    self.struct_typeCheck = 'crc'
                    self.struct_ruleCheck = try_return_checkRule(val)
                if 'crc16' == tar.lower():
                    self.struct_typeCheck = 'crc16'
                    self.struct_ruleCheck = try_return_checkRule(val)
                if 'crc32' == tar.lower():
                    self.struct_typeCheck = 'crc32'
                    self.struct_ruleCheck = try_return_checkRule(val)
                if ('crc' in tar.lower()) & ('0x00' in tar.lower()):
                    self.struct_typeCheck = 'crc_00'
                    self.struct_ruleCheck = try_return_checkRule(val)
                if ('crc' in tar.lower()) & ('0xff' in tar.lower()):
                    self.struct_typeCheck = 'crc_ff'
                    self.struct_ruleCheck = try_return_checkRule(val)
                if ('crc_mcrf4' == tar.lower())|( ('crc' in tar.lower())&('mcrf4' in tar.lower()) ):
                    self.struct_typeCheck = 'crc_mcrf4'
                    self.struct_ruleCheck = try_return_checkRule(val)
                if 'button' in tar.lower():
                    self.struct_buttonList.append([val,''.join(split_data[3:])])
                    
            elif len(split_data)<4:
                self.struct_debugList.append('未知规则行:{}'.format(line))
            elif split_data[0] in self.struct_decode:
                self.struct_packList.append(split_data[0])
                self.struct_paraList.append(try_return_num(split_data[1]))
                self.struct_titlList.append(split_data[2])
                self.struct_dataList.append(split_data[3])
            else:
                self.struct_debugList.append('未知规则行:{}'.format(line))
                continue
        self.get_struct_len()
    def init_structList(self):
        self.struct_ruleCheck = False
        self.struct_typeCheck = 'None'
        self.struct_packList = []
        self.struct_paraList = []
        self.struct_titlList = []
        self.struct_dataList = []
        self.struct_buttonList = []
        self.struct_debugList = []
    def get_struct_len(self):
        self.struct_len = 0
        self.struct_packRule = self.struct_format+''.join(self.struct_packList)
        self.struct_len = struct.calcsize(self.struct_packRule)
        return self.struct_len,self.struct_packRule 
      
      
        
class struct_tab_setting:
    def __init__(self,mw,tab=1):
        self.tab = tab  
        def get_widget(widget_type, object_name):
            widget = getattr(mw, object_name, None)
            if widget is None:
                widget = mw.findChild(widget_type, object_name)
            return widget

        self.com = get_widget(QtWidgets.QComboBox, 'combox_set_com_{}'.format(tab))
        self.baund = get_widget(QtWidgets.QComboBox, 'combox_set_baund_{}'.format(tab))
        self.check = get_widget(QtWidgets.QComboBox, 'comboBox_set_check_{}'.format(tab))
        self.stop = get_widget(QtWidgets.QComboBox, 'comboBox_stopbit_{}'.format(tab))
        self.open = get_widget(QtWidgets.QPushButton, 'pushButton_com_open_{}'.format(tab))
        self.name = get_widget(QtWidgets.QLineEdit, 'lineEdit_file_names_{}'.format(tab))
        self.plan = get_widget(QtWidgets.QLineEdit, 'lineEdit_plan_names_{}'.format(tab))
        self.rule = None
        
        self.flag_open = (self.open.text()=='开启')
    
    def set_com(self,com='COM1'):
        self.com.setCurrentText(str(com))
    def set_baund(self,baund=115200):
        self.baund.setCurrentText(str(baund))
    def set_check(self,check='无校验'):
        self.check.setCurrentText(str(check))
    def set_stop(self,stop='Stop1'):
        
        self.stop.setCurrentText(str(stop))
    def set_open(self,open='开启'):
        self.open.setText(str(open))
        self.flag_open = (open=='开启')
    def switch_open(self):
        self.open.setText('关闭' if self.get_open_flag() else '开启') 
    def set_name(self,name='autosave'):
        self.name.setText('{}_{}'.format(name,self.tab))
    def set_plan(self,plan=''):
        self.plan.setText(str(plan))
        
    def get_com(self):
        return self.com.currentText()
    def get_baund(self):
        return self.baund.currentText()
    def get_check(self):
        return self.check.currentText()
    def get_stop(self):
        return self.stop.currentText()
    def get_open(self):
        return self.open.text()
    def get_open_flag(self):
        return self.open.text()=='开启'
    def get_name(self):
        return self.name.text()
    def get_plan(self):
        return self.plan.text()

class struct_sate:
    def __init__(self):
        self.flag_sate_receive = False
        self.threading_flag_sate = False
        # 卫导串口
        self.serials = None
        # 发送缓存
        self.list_sate_send = []
        # 接收缓存
        self.list_sate_receive = []     
        # 分类接收缓存
        self.list_sate_ascii_msg = []
        for i in range(8):
            self.list_sate_ascii_msg.append([])
        # 分类保存缓存
        self.list_sate_flag = []
        for i in range(8):
            self.list_sate_flag.append(False)
        # 分类保存文件名
        self.list_sate_name = []
        for i in range(8):
            self.list_sate_name.append('')
        # 添加卫导标题
        self.list_sate_titl = []
        for i in range(8):
            self.list_sate_titl.append([])
        # 添加卫导长度
        self.list_sate_leng = []
        for i in range(8):
            self.list_sate_leng.append(0)
        # 处理后保存卫导数据
        self.list_sate_msg = []
        for i in range(8):
            self.list_sate_msg.append([])

        
        self.init_sate_name()
        self.init_sate_titl()
        self.init_sate_leng()
        self.init_sate_zero()
        self.init_sate_shap()

    
    def init_sate_name(self):
        self.list_sate_name[0] = '发送'
        self.list_sate_name[1] = '反馈'
        self.list_sate_name[2] = '$GNGGA'
        self.list_sate_name[3] = '$GPGGA'
        self.list_sate_name[4] = '$BDGGA'
        self.list_sate_name[5] = '$GNVTG'
        self.list_sate_name[6] = '#HEADINGA'
        self.list_sate_name[7] = '$KSXT'
    
    def init_sate_save(self,lists):
        for i in range(8):
            self.list_sate_flag[i] = lists[i]
    def init_sate_titl(self):
        for i in range(3):
            shift = 2
            self.list_sate_titl[i+shift].append('纬度')
            self.list_sate_titl[i+shift].append('经度')
            self.list_sate_titl[i+shift].append('卫星')
            self.list_sate_titl[i+shift].append('精度')
            self.list_sate_titl[i+shift].append('高度')
        for i in range(1):
            shift = 5
            self.list_sate_titl[i+shift].append('真北航向')
            self.list_sate_titl[i+shift].append('磁北航向')
            self.list_sate_titl[i+shift].append('水平速度')
            self.list_sate_titl[i+shift].append('水平速度')
            self.list_sate_titl[i+shift].append('模式指示')
        for i in range(1):
            shift = 6
            self.list_sate_titl[i+shift].append('航向')
            self.list_sate_titl[i+shift].append('俯仰')
            self.list_sate_titl[i+shift].append('航向偏差')
            self.list_sate_titl[i+shift].append('俯仰偏差')
            self.list_sate_titl[i+shift].append('跟踪卫星')
            self.list_sate_titl[i+shift].append('使用卫星')
        for i in range(1):
            shift = 7
            self.list_sate_titl[i+shift].append('utc时间')
            self.list_sate_titl[i+shift].append('经度')
            self.list_sate_titl[i+shift].append('纬度')
            self.list_sate_titl[i+shift].append('海拔高')
            self.list_sate_titl[i+shift].append('东速')
            self.list_sate_titl[i+shift].append('北速')
            self.list_sate_titl[i+shift].append('天速')
    def init_sate_leng(self):
        for i in range(8):
            self.list_sate_leng[i] = len(self.list_sate_titl[i])
    def init_sate_zero(self):
        for i in range(8):
            pass
    def init_sate_shap(self):
        self.list_sate_msg = []
        for i in range(8):
            self.list_sate_msg.append([])
            for j in range(self.list_sate_leng[i]):
                self.list_sate_msg[i].append(0.0)



        
    def append_sare_send(self,send_data):
        self.list_sate_send.append('{}\r\n'.format(send_data).encode('ascii'))
        
    def append_sate_receive(self,receive_data):
        self.list_sate_receive.append(receive_data)
        self.replace_sate_receive()
    
    def replace_sate_receive(self):
        while len(self.list_sate_receive)>0:
            sate_data = self.list_sate_receive.pop(0)
            on_rule = False
            for i in range(6):
                if self.list_sate_name[i+2] in sate_data:
                    self.list_sate_ascii_msg[i+2].append(sate_data)
                    # print('{} :{}'.format(i,sate_data))
                    on_rule = True
                    if i<3:
                        self.list_sate_msg[i+2] = GPGGA2loc(sate_data)
                        # print(GPGGA2loc(sate_data))
                    elif i==3:
                        self.list_sate_msg[i+2] = GNVTG2loc(sate_data)
                    elif i==4:
                        self.list_sate_msg[i+2] = HEADINGA2loc(sate_data)
                    elif i==5:
                        self.list_sate_msg[i+2] = KSXT2loc(sate_data)
                    break
            if not on_rule:
                self.list_sate_ascii_msg[1].append(sate_data)
    def clear_sate_list(self,num):
        self.list_sate_msg[num] = [0]*len(self.list_sate_msg[num])

class clickEventThread_decodeShow(QtCore.QThread):
    update_signal = QtCore.pyqtSignal(str)
    def run(self):
        for i in range(10):
            time.sleep(1)
            self.update_signal.emit('事件更新:{}s'.format(i+1))
            

class struct_turnTable3x:
    def __init__(self):
        self.list_debugMsg = []
        self.list_showMsg = []
        self.str_lastRec = ''
        self.list_mode = [0, 0, 0]  # 运行模式
        # 默认位置
        self.list_commandLocation = [0, 0, 0]
        # 默认速度
        self.list_commandSpeed = [10, 10, 10]
        # 默认加速度
        self.list_commandAcceleration = [10, 10, 10]
        self.list_recLocation = [0,0,0]
        self.list_recSpeed = [0,0,0]
        self.list_recReadySts = [False,False,False]
        self.flag_theading = False
        self.serial = None
        self.serial_com = 'COM1'
        self.serial_check = False
        

    def append_debugMsg(self, msg):
        if isinstance(msg, list):
            msg = ', '.join([str(i) for i in msg])
        self.list_debugMsg.append(str(msg))
        while len(self.list_debugMsg) > 10:
            self.list_debugMsg.pop(0)

    def append_showMsg(self, msg):
        if isinstance(msg, list):
            msg = ', '.join([str(i) for i in msg])
        self.list_showMsg.append(str(msg))
        while len(self.list_showMsg) > 100:
            self.list_showMsg.pop(0)
    # 调试信息清除
    def append_msgClear(self):
        self.list_showMsg.clear()
        self.list_debugMsg.clear()
    def serial_open(self):
        emsg = ''
        result,emsg =  self.serial_close()
        if not result:
            return False, emsg
        try:
            self.serial = serial.Serial(self.serial_com, 115200)
            return True, '串口已打开:{}'.format(self.serial_com)
        except Exception as e:
            self.append_debugMsg('开启串口异常: {}'.format(e))
            self.serial = None
            return False, '串口打开失败: {}'.format(e)

    def serial_close(self):
        if self.serial is None:
            return True,'串口未打开'
        else:
            try:
                self.serial.close()
                self.serial = None
                return True, '串口已关闭'
            except Exception as e:
                self.append_debugMsg('重启串口异常: {}'.format(e))
                return False, '串口关闭失败: {}'.format(e)
    # 尝试读取串口数据
    def serial_tryRec(self, tryCount=30, waitTime=0.01):
        count = 0
        while count < tryCount:
            count += 1
            try:
                wait = self.serial.in_waiting
                if wait > 0:
                    recdata = self.serial.read(wait)
                    return recdata
            except Exception as e:
                self.append_debugMsg('获取数据错误: {}'.format(e))
            time.sleep(waitTime)
        return False
    def serial_try_clear(self):
        try:
            wait = self.serial.in_waiting
            if wait > 0:
                rec_data = self.serial.read(wait)
                self.append_debugMsg('清除接收缓存:{}'.format(rec_data.decode()))
                return rec_data
            else:
                return False
        except Exception as e :
            return False
                
    # 尝试发送和读取校验
    def sendAndRec(self, sendMsg='', recMsg=''):
        clear_result = self.serial_try_clear()
        # if clear_result:
        #     print('清理转台控制缓存区:{}'.format(clear_result))
        if len(sendMsg) > 0:
            # print('sendMsg: {}'.format(sendMsg))
            try:
                self.serial.write(sendMsg.encode())
            except Exception as e:
                self.append_debugMsg('发送指令错误: {}'.format(e))
                return False
        try:
            rec = self.serial_tryRec()
            if not rec:
                self.append_showMsg('未接收到转台指令')
                return False
            if len(recMsg) > 0:
                if isinstance(recMsg, list):
                    if all(item in rec.decode() for item in recMsg):
                        self.append_showMsg('OK:{}'.format(sendMsg))
                        return True
                elif isinstance(recMsg, str):
                    if recMsg in rec.decode():
                        self.append_showMsg('OK:{}'.format(sendMsg))
                        return True
                else:
                    self.append_showMsg('错误校验指令')
                    self.append_debugMsg('指令格式错误: {}'.format(recMsg))
                    return False
            else:
                # self.append_debugMsg('Rec:{}'.format(rec.decode()))
                self.str_lastRec = rec.decode()
                return rec.decode()
        except Exception as e:
            self.append_debugMsg('接收指令错误: {}'.format(e))
            return False
        self.append_showMsg('校验失败: {}'.format(recMsg))
        self.append_debugMsg(
            '校验失败: send:<{}> check:<{}> rec:<{}>'.format(sendMsg, recMsg, rec.decode())
        )
        return False

    # 通讯校验和
    def sumCheckAscii(self, string):
        return sum(ord(c) for c in string) & 0xFF

    # 通讯检查
    def sendMsg_chk(self):
        return self.sendAndRec('$MNCHK,1*CE\r\n', '$ASCHK,OK*30')
    # 进入远控
    def sendMsg_rem(self):
        return self.sendAndRec('$MNREM,1*DC\r\n', '$ASREM,OK*3E')
    # 返回本控
    def sendMsg_loc(self):
        return self.sendAndRec('$MNLOC,1*D6\r\n', '$ASLOC,OK*38')
    # 使能
    def sendMsg_enb(self):
        return self.sendAndRec('$MNENB,1*CD\r\n', '$ASENB,OK*2F')
    # 断开使能
    def sendMsg_dis(self):
        return self.sendAndRec('$MNDIS,1*D8\r\n', '$ASDIS,OK*3A')
    # 转台寻零
    def sendMsg_hmz(self):
        return self.sendAndRec('$MNHMZ,1*E7\r\n', '$ASHMZ,OK*49')
    # 运行模式
    def sendMsg_mod(self, a, b, c):
        msg_list = [a, b, c]
        for i in msg_list:
            if str(i) not in ['0', '1', '2']:
                self.append_showMsg('转台运行模式设置错误: {}'.format([a, b, c]))
                self.append_debugMsg('转台运行模式设置错误: {}'.format([a, b, c]))
                return False
        sendMsg = 'MNMOD,{},{},{}'.format(a, b, c)
        # recMsg = 'ASMOD,{},{},{},OK'.format(a, b, c)
        recMsg = ['ASMOD','OK']
        return self.sendAndRec(
            '${}*{:02X}\r\n'.format(sendMsg, self.sumCheckAscii(sendMsg)),
            recMsg
            )
    # 位置设置
    def sendMsg_pos(self, a, b, c):
        msg_list = [a, b, c]
        for i in msg_list:
            try:float(i)
            except:
                self.append_showMsg('转台位置设置错误: {}'.format([a, b, c]))
                self.append_debugMsg('转台位置设置错误: {}'.format([a, b, c]))
                return False
        sendMsg = 'MNPOS,{},{},{}'.format(a, b, c)
        # recMsg = 'ASPOS,{},{},{},OK'.format(a, b, c)
        recMsg = ['ASPOS','OK']
        return self.sendAndRec(
            '${}*{:02X}\r\n'.format(sendMsg, self.sumCheckAscii(sendMsg)),
            recMsg
            )
    # 速度设置
    def sendMsg_vel(self, a, b, c):
        msg_list = [a, b, c]
        send_list = []
        for i in msg_list:
            try:send_list.append(float(i))
            except:
                self.append_showMsg('转台速度设置错误: {}'.format([a, b, c]))
                self.append_debugMsg('转台速度设置错误: {}'.format([a, b, c]))
                return False
        sendMsg = 'MNVEL,{},{},{}'.format(a, b, c)
        # recMsg = 'ASVEL,{},{},{},OK'.format(a, b, c)
        recMsg = ['ASVEL','OK']
        return self.sendAndRec(
            '${}*{:02X}\r\n'.format(sendMsg, self.sumCheckAscii(sendMsg)),
            recMsg
            )
    # 加速度设置
    def sendMsg_acc(self, a, b, c):
        msg_list = [a, b, c]
        for i in msg_list:
            try:float(i)
            except:
                self.append_showMsg('转台加速度设置错误: {}'.format([a, b, c]))
                return False
        sendMsg = 'MNACC,{},{},{}'.format(a, b, c)
        # recMsg = 'ASACC,{},{},{},OK'.format(a, b, c)
        recMsg = ['ASACC','OK']
        return self.sendAndRec(
            '${}*{:02X}\r\n'.format(sendMsg, self.sumCheckAscii(sendMsg)),
            recMsg
            )
    # 运行
    def sendMsg_run(self):
        return self.sendAndRec('$MNRUN,1*ED\r\n', '$ASRUN,OK*4F')
    # 停止
    def sendMsg_stp(self):
        return self.sendAndRec('$MNSTP,1*EF\r\n', '$ASSTP,OK*51')
    # 状态查询
    def sendMsg_sts(self):
        return self.sendAndRec('$MNSTS,1*F2\r\n', '')