# 工具栏下属
# 处理标定数据
import os,re,datetime,shutil,threading#,debugpy
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt 
from PyQt5.QtWidgets import QWidget, QFileDialog,QLineEdit, QListWidgetItem, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize,Qt,QTimer,QThread,pyqtSignal
# import matplotlib
# matplotlib.use("Agg")
# from matplotlib.pylab import mpl
# from matplotlib.ticker import ScalarFormatter
# from matplotlib.ticker import FuncFormatter
# mpl.rcParams['font.sans-serif'] = ['SimHei']
# mpl.rcParams['axes.unicode_minus'] = False
def extract_number(filename):
    match = re.search(r'BD(\d+)#',filename)
    return int(match.group(1)) if match else float('inf')
def sort_key(fname,split_rule):
    parts = fname.split(split_rule[0])
    try: return int(parts[split_rule[1]])
    except (IndexError, ValueError):
        return float("inf")
def init_sdf():
    # 初始化文件
    list_columns = [
        "G0", "G+", "G-", 
        "ScaleFactor+", "ScaleFactor-", "NonLinear", 
        "K*x", "K*y", "K*z", 
        "Temp"
    ]
    list_rows = ["Gx", "Gy", "Gz", "Ax", "Ay", "Az"]
    sdf = pd.DataFrame(0,index=list_rows, columns=list_columns)
    return sdf  
def decode_zfG(zfG_str,A_length=4):
    zfG_list = zfG_str.split(' ')[:3]
    if len(zfG_list)<3:
        zfG_list = [zfG_str[:A_length]]*3
    zfG_decode = []
    for cout,strs in enumerate(zfG_list):
        if strs!=4:
            strs = strs.ljust(4,'0')[:4]
        zfg_list = [[],[]]
        for i in range(A_length):
            if strs[i]=='1':
                zfg_list[0].append(i)
            else:
                zfg_list[1].append(i)
        zfG_decode.append(zfg_list)
    return zfG_decode

class MainWindowToolBdcalib:
    def __init__(self, mainWindow):
        self.mw = mainWindow
        # 系数列表
        self.list_input_lineEdit = []
        self.list_input_data = []
        # 正则表达式
        self.list_pathrule_and = []
        self.list_pathrule_nor = []
        self.pixmap = None
        self.work_processData = None
        # 快捷路径
        self.show_path = self.mw.lineEdit_tools_bd3x_showPath
        self.show_file = self.mw.listWidget_tools_bd3x_pathShow
        # 初始化
        self.init_list()
        self.init_data()
        # 逻辑事件
        self.mw.pushButton_tools_bd3x_loadPath.clicked.connect(self.load_path)
        self.mw.listWidget_tools_bd3x_pathShow.itemClicked.connect(self.item_click_showMsg)
        self.mw.listWidget_tools_bd3x_pathShow.itemDoubleClicked.connect(self.item_click_changeFolder)
        self.mw.label_tools_imgShow.resizeEvent = self.label_resizeEvent
        self.mw.pushButton_tools_bd3x_uppath.clicked.connect(self.click_uppath)
        self.mw.checkBox_tools_bd3x_regexFolder.clicked.connect(self.show_all_files)
        self.mw.pushButton_tools_bd3x_avePath.clicked.connect(self.click_avePath)
        self.mw.pushButton_tools_bd3x_modTransform.clicked.connect(self.click_formatConversion)
        self.mw.comboBox_tools_bd3x_preset.currentTextChanged.connect(self.change_preset)
        self.mw.pushButton_tools_bd3x_createBin.clicked.connect(self.click_createBin)
        self.mw.pushButton_tools_bd3x_autoRun.clicked.connect(self.click_autoRun)
        self.mw.pushButton_tools_bd3x_calPara.clicked.connect(self.click_calPara)
        self.mw.pushButton_tools_bd3x_polyFit.clicked.connect(self.click_polyfit)
        self.mw.pushButton_tools_bd3x_flush.clicked.connect(self.show_all_files)
        
    # 初始化所有输入框
    def init_list(self):
        lineEdit_length_count = 40
        for i in range(lineEdit_length_count):
            try:
                lineedit =  self.mw.findChild(QLineEdit,'lineEdit_tools_bd3x_{}'.format(i))
                if lineedit is None: break
                else:self.list_input_lineEdit.append(lineedit)
            except: break
            
            
    # 初始化输入框所有变量
    def init_data(self):
        for count,lineedit in enumerate(self.list_input_lineEdit):
            app_data = lineedit.text() if lineedit.text() else ''
            if len(self.list_input_data)<=count:
                self.list_input_data.append(app_data)
            else:
                self.list_input_data[count] = app_data
        decode_rule_and = self.list_input_data[0]
        decode_rule_nor = self.list_input_data[1]
        self.list_pathrule_and = []
        self.list_pathrule_nor = []
        for count, rule in enumerate(decode_rule_and.split('|')):
            self.list_pathrule_and.append([])   
            for r in re.split(r'[\s,，]+', rule):
                self.list_pathrule_and[count].append(r) if r else None
        for count, rule in enumerate(decode_rule_nor.split('|')):
            self.list_pathrule_nor.append([])
            for r in re.split(r'[\s,，]+', rule):
                self.list_pathrule_nor[count].append(r) if r else None
            
            
    # 打开文件夹载入路径
    def load_path(self):
        folder = QFileDialog.getExistingDirectory(self.mw, "选择文件夹_载入预览路径", "")
        if folder:
            self.show_path.setText(folder)
            self.mw.lineEdit_tools_bd3x_loadPath.setText(folder)
            self.show_all_files(folder)
            
    # 在listWidget_tools_bd3x_pathShow中显示所有正则规则中的文件
    def show_all_files(self,folder):
        if self.mw.sender() == self.mw.checkBox_tools_bd3x_regexFolder:
            folder = self.show_path.text()
        if self.mw.sender() == self.mw.pushButton_tools_bd3x_flush:
            folder = self.show_path.text()
        if len(folder)==0:
            folder = './'
            
        self.init_data()
        try:
            files = os.listdir(folder)
            self.show_file.clear()
            for file in files:
                if os.path.isdir(os.path.join(folder, file)):
                    self.show_file.addItem('[{}]'.format(file))
                else:
                    if self.mw.checkBox_tools_bd3x_regexFolder.isChecked():
                        and_rule = any([all([re.search(r, file) for r in rule]) for rule in self.list_pathrule_and]) if self.list_pathrule_and else True
                        nor_rule = any([any([re.search(r, file) for r in rule]) for rule in self.list_pathrule_nor]) if self.list_pathrule_nor else True
                    else:
                        and_rule = True
                        nor_rule = False
                    if and_rule and (not nor_rule):
                        self.show_file.addItem(file)
        except Exception as e:
            self.show_file.addItem('Error: {}'.format(e))
        
    def append_degugMsg(self,msg):
        now = datetime.datetime.now()
        try: self.mw.textBrowser_tools_bd3x_msglast.setText('{} {}'.format(now.strftime('%H:%M:%S'), msg))
        except Exception as e: print('Error:append_degugMsg: {}'.format(e))
    
    # 根据类型预览文件
    def preview_file(self, mode=0):
        set_list = [
            self.mw.tableWidget_tools_bd3x_fileShow,
            self.mw.textEdit_tools_bd3x_fileShow,
            self.mw.label_tools_imgShow
        ]
        if mode==0:
            set_mode = [True, False, False]
        elif mode==1:
            set_mode = [False, True, False]
        elif mode==2:
            set_mode = [False, False, True]
        elif mode==-1:
            set_mode = [False, False, False]
        for i in range(len(set_list)):
            # set_list[i].setVisible(set_mode[i])
            set_list[i].hide() if not set_mode[i] else set_list[i].show()
    # 点击返回上级目录
    def click_uppath(self):
        current_path = self.show_path.text()
        parent_path = os.path.dirname(current_path)
        if os.path.isdir(parent_path) and parent_path != current_path:
            self.show_path.setText(parent_path)
            self.show_all_files(parent_path)
            self.append_degugMsg('进入上级目录:\n {}'.format(parent_path))
    # 双击进入文件夹
    def item_click_changeFolder(self,item):
        if item.text().startswith('[') and item.text().endswith(']'):
            folder_name = item.text()[1:-1]
            new_path = os.path.join(self.show_path.text(), folder_name)
            if os.path.isdir(new_path):
                self.show_path.setText(new_path)
                self.show_all_files(new_path)
                self.append_degugMsg('进入文件夹:\n [{}]'.format(folder_name))
    # 单击预览文件
    def item_click_showMsg(self,item):
        img_list = ['png','jpg','jpeg','bmp','tif','tiff']
        txt_list = ['txt','csv','log','ini','json','xml']
        if item.text().startswith('[') and item.text().endswith(']'):
            # 如果是双击，则进入列表中
            self.preview_file(mode=-1)
        elif any([item.text().lower().endswith('.'+ext) for ext in img_list]):
            self.preview_file(mode=2)
            self.append_degugMsg('载入图片:\n {}'.format(item.text()))
            item_path = os.path.join(self.show_path.text(), item.text())    
            self.pixmap = QPixmap(item_path)
            self.update_imgShow_pixmap()
            self.mw.label_tools_imgShow.setScaledContents(False)
        elif any([item.text().lower().endswith('.'+ext) for ext in txt_list]):
            # 尝试使用pd读取前10行
            try:
                import pandas as pd
                # 尝试使用gb2312和utf-8打开文件
                df = pd.read_csv(
                    os.path.join(self.show_path.text(), item.text()), 
                    encoding='gb2312',
                    delim_whitespace=True, 
                    nrows=100,
                    dtype='str',
                    encoding_errors="replace"
                )
                self.preview_file(mode=0)
                table = self.mw.tableWidget_tools_bd3x_fileShow
                table.clear()
                table.setRowCount(len(df))
                table.setColumnCount(len(df.columns))
                table.setHorizontalHeaderLabels(df.columns.tolist())
                for i in range(len(df)):
                    for j in range(len(df.columns)):
                        table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))
                table.resizeColumnsToContents()
                self.append_degugMsg('载入表格:\n {}'.format(item.text()))
            #否则使用普通文本读取前10行
            except Exception as e:
                print('读取为表格失败:', e)
                try:
                    with open(os.path.join(self.show_path.text(), item.text()), 'r', encoding='gb2312', errors='replace') as f:
                        content = ''.join([f.readline() for _ in range(100)])
                    self.preview_file(mode=1)
                    textedit = self.mw.textEdit_tools_bd3x_fileShow
                    textedit.setPlainText(content)
                    self.append_degugMsg('载入文本:\n {}'.format(item.text()))
                except Exception as e2:
                    self.preview_file(mode=-1)
                    self.append_degugMsg('无法载入文件\n {}: {}, {}'.format(item.text(), e, e2)) 
        else:
            self.preview_file(mode=-1)
            self.append_degugMsg('不支持预览该文件:\n {}'.format(item.text()))

    def update_imgShow_pixmap(self):
        if self.pixmap :
            self.mw.label_tools_imgShow.setPixmap(
                self.pixmap.scaled(
                    QSize(
                        int(self.mw.label_tools_imgShow.size().width()-20),
                        int(self.mw.label_tools_imgShow.size().height()-40)
                    ),
                    # self.mw.label_tools_imgShow.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
    def label_resizeEvent(self, event):
        self.update_imgShow_pixmap()
        QWidget.resizeEvent(self.mw.label_tools_imgShow, event)
        
    def click_avePath(self):
        # 打开文件夹
        folder_path = QFileDialog.getExistingDirectory(self.mw, '选择文件夹_预处理标定数据')
        if folder_path:
            self.show_path.setText(folder_path)
            self.mw.lineEdit_tools_bd3x_avePath.setText(folder_path)
            self.init_data()
            self.show_all_files(folder_path)
            self.append_degugMsg('预处理标定数据中...')
            self.work_processData = class_Worker(folder_path, self.list_input_data, self.list_pathrule_and, self.list_pathrule_nor,self.mw.root_mode)
            self.work_processData.finished.connect(self.task_done)
            self.work_processData.mode = 1
            self.work_processData.start()
    def click_formatConversion(self):
        folder_path = QFileDialog.getExistingDirectory(self.mw, '选择文件夹_格式转换_通用')
        if folder_path:
            self.show_path.setText(folder_path)
            self.mw.lineEdit_tools_bd3x_formatPath.setText(folder_path)
            self.init_data()
            self.show_all_files(folder_path)
            self.append_degugMsg('格式转换中...')
            self.work_processData = class_Worker(folder_path, self.list_input_data, self.list_pathrule_and, self.list_pathrule_nor,self.mw.root_mode)
            self.work_processData.finished.connect(self.task_done)
            self.work_processData.mode = 2
            self.work_processData.start()
    def click_calPara(self):
        folder_path = QFileDialog.getExistingDirectory(self.mw, '选择文件夹_参数计算_通用')
        if folder_path:
            self.show_path.setText(folder_path)
            self.mw.lineEdit_tools_bd3x_calPath.setText(folder_path)
            self.init_data()
            self.show_all_files(folder_path)
            self.append_degugMsg('参数计算中...')
            self.work_processData = class_Worker(folder_path, self.list_input_data, self.list_pathrule_and, self.list_pathrule_nor,self.mw.root_mode)
            self.work_processData.preset_name = self.mw.comboBox_tools_bd3x_preset.currentText()
            self.work_processData.finished.connect(self.task_done)
            self.work_processData.mode = 3
            self.work_processData.start()
    def click_polyfit(self):
        folder_path = QFileDialog.getExistingDirectory(self.mw, '选择文件夹_拟合曲线_通用')
        if folder_path:
            self.show_path.setText(folder_path)
            self.mw.lineEdit_tools_bd3x_calPath.setText(folder_path)
            self.init_data()
            self.show_all_files(folder_path)
            self.append_degugMsg('拟合曲线中...')
            self.work_processData = class_Worker(folder_path, self.list_input_data, self.list_pathrule_and, self.list_pathrule_nor,self.mw.root_mode)
            self.work_processData.preset_name = self.mw.comboBox_tools_bd3x_preset.currentText()
            self.work_processData.finished.connect(self.task_done)
            self.work_processData.mode = 4
            self.work_processData.start()
            
    def task_done(self):
        try:debug_info = self.work_processData.debug_info;self.work_processData.debug_info = ''
        except Exception as e: debug_info = '未读取到信息'
        if len(debug_info)>0: self.append_degugMsg(f'处理数据完成：\n{debug_info}')
        else: self.append_degugMsg('处理数据完成\n未读取到信息')
        self.show_all_files(self.show_path.text())
    def change_preset(self):
        self.append_degugMsg('未读取到预设文件')
    def click_createBin(self):
        self.append_degugMsg('未读取到pyc文件')
    def click_autoRun(self):
        self.append_degugMsg('未实现的功能')
    
            

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
class class_Worker(QThread):
    finished = pyqtSignal(str)
    
    def __init__(self, folder_path,list_input_data,list_pathrule_and, list_pathrule_nor,root_mode):
        super().__init__()
        self.root_mode = root_mode
        self.folder_path = folder_path
        self.list_input_data = list_input_data
        self.folder_path = folder_path
        self.list_pathrule_and = list_pathrule_and
        self.list_pathrule_nor = list_pathrule_nor
        self.preset_name = ''
        self.debug_info = ''
        self.mode = 0
        self.G = 9.801538877
        

    def run(self):
        if self.root_mode:
            try:
                import debugpy
                debugpy.debug_this_thread()
            except Exception as e:
                self.debug_info = '无法开启调试: {}'.format(e)
        if self.mode==0:
            self.debug_info = '未设置处理模式'
        # 对所有数据取均值
        elif self.mode==1:
            self.ave_all_data()
        # 格式转换为matlab处理格式
        elif self.mode==2:
            self.format_all_data()
        # 计算所有参数[零位、标度、非线性、非正交]
        elif self.mode==3:
            if 'chy' in self.preset_name:
                self.cal_all_para_chy()
            else:   
                self.cal_all_para()
        # 计算全温拟合曲线
        elif self.mode==4:
            if 'chy' in self.preset_name:
                self.cal_all_polyfit_chy()
            else:
                self.cal_all_polyfit()
            
        else:
            self.debug_info = '未知的处理模式'
        self.finished.emit('线程work_processData结束')
        
        
        
    def ave_all_data(self):
        # 初始化变量
        ave_length_split = self.list_input_data[10]
        drop_row_footer = self.list_input_data[11]
        rollings = self.list_input_data[12]
        save_data_accuracy = self.list_input_data[14]
        
        try:ave_length_split = int(ave_length_split)
        except:ave_length_split = 1
        try:rollings = int(rollings)
        except:rollings = 1
        try:save_data_accuracy = int(save_data_accuracy)
        except:save_data_accuracy = 6
        drop_row_footer = []
        try:drop_row_footer = [int(r) for r in re.split(r'[\s,，]+',drop_row_footer)]
        except:drop_row_footer = []
        if len(drop_row_footer)!=2: drop_row_footer = [0, 0]
        list_all_input = []
        
        # 读取原始数据并分隔list
        for i in range(8):
            input_data = self.list_input_data[i+2]
            input_list = []
            for j in range(3):
                try:
                    if i<4: input_list.append( int( re.split(r'[\s,，]+',input_data)[j] ) )
                    else: input_list.append( float( re.split(r'[\s,，]+',input_data)[j] ) )
                except Exception as e:
                    try: input_list.append(input_list[j-1])
                    except: input_list.append(1)

            list_all_input.append(input_list)

        # 保存轴系重排
        save_list_axis = []
        save_list_para = []
        for i in range(4):
            save_list_axis+=list_all_input[i]
        for i in range(4):  
            save_list_para+=list_all_input[i+4]
            
            
        path = self.folder_path
        # 创建ave和std文件夹
        save_ave_path = os.path.join(path, 'all_ave')
        save_std_path = os.path.join(path, 'all_std')
        if os.path.exists(save_ave_path):
            shutil.rmtree(save_ave_path)
        os.makedirs(save_ave_path)
        if os.path.exists(save_std_path):
            shutil.rmtree(save_std_path)
        os.makedirs(save_std_path)
        

            
        
        total_folder = 0
        total_file = 0
        total_error = 0
        # 遍历文件夹
        load_paths = path
        for plan_name in os.listdir(load_paths):
            if not os.path.isdir(os.path.join(load_paths, plan_name)):
                continue
            if plan_name.startswith('all_'):
                continue    
            total_folder += 1
            list_all_file = [f for f in os.listdir(os.path.join(load_paths, plan_name)) if re.search(r'BD(\d+)#',f)]
            sorted_list_files = sorted(list_all_file,key=extract_number)
            
            list_regex_name = []
            for file_name in sorted_list_files:
                and_rule = any([all([re.search(r, file_name) for r in rule]) for rule in self.list_pathrule_and]) if self.list_pathrule_and else True
                nor_rule = any([any([re.search(r, file_name) for r in rule]) for rule in self.list_pathrule_nor]) if self.list_pathrule_nor else True
                if and_rule and not nor_rule:
                    total_file+=1
                    total_error+=1
                    list_regex_name.append(file_name)    
                    df = pd.read_csv(
                        os.path.join(load_paths, plan_name, file_name),
                        encoding='gb2312',
                        delim_whitespace=True,skiprows=drop_row_footer[0], skipfooter=drop_row_footer[1]
                    )
                    if len(df) < ave_length_split:
                        ave_length = len(df)
                    else:
                        ave_length = (len(df)//ave_length_split)*ave_length_split
                    df_ave = df.iloc[-ave_length:,:].mean()
                    and_rule_list = [all([re.search(r, file_name) for r in rule]) for rule in self.list_pathrule_and]
                    try: save_rule_name = '_'.join(self.list_pathrule_and[and_rule_list.index(True)])
                    except: save_rule_name = 'other'
                    try:turntable = re.search(r'(?:loc|spd)\[([^\]]+)\]', file_name).group(1)
                    except: turntable = 'None'
                    save_name = '{}_{}.txt'.format(plan_name,save_rule_name)
                    save_ave_file = os.path.join(save_ave_path, save_name)
                    save_name = '{}_{}_roll{}s.txt'.format(plan_name,save_rule_name,rollings)
                    save_std_file = os.path.join(save_std_path, save_name)
                    # 均值
                    if not os.path.exists(save_ave_file):
                        self.init_save_aveFile(save_ave_file)
                    save_file_data = []
                    save_file_data.append('[{}]'.format(turntable))
                    for count,axis in enumerate(save_list_axis):
                        save_data = df_ave[axis]*save_list_para[count]
                        save_file_data.append(f"{save_data:.{save_data_accuracy}f}")
                    save_file_data.append(str(ave_length))
                    with open(save_ave_file, 'a+', newline='', encoding='gb2312') as f:
                        f.write('\t'.join(save_file_data)+'\n')
                    # 标准差
                    if not os.path.exists(save_std_file):
                        self.init_save_aveFile(save_std_file)
                    save_file_data = []
                    save_file_data.append('[{}]'.format(turntable))
                    for count,axis in enumerate(save_list_axis):
                        if count<6:
                            save_data = df.iloc[-ave_length:,axis].rolling(rollings).mean().std()*save_list_para[count]
                        else:
                            save_data = df.iloc[-ave_length:,axis].mean()*save_list_para[count]
                        save_file_data.append(f"{save_data:.{save_data_accuracy}f}")
                    save_file_data.append(str(ave_length))
                    with open(save_std_file, 'a+', newline='', encoding='gb2312') as f:
                        f.write('\t'.join(save_file_data)+'\n')
                        
                    total_error-=1
                    
                    
        self.debug_info = f'文件夹：{total_folder}，文件：{total_file}，错误：{total_error}'
        
    def init_save_aveFile(self,save_file_path):
        # Turntable	Gx(deg/h)	Gy(deg/h)	Gz(deg/h)	Ax(m/s2)	Ay(m/s2)	Az(m/s2)	GxTemp	GyTemp	GzTemp	AxTemp	AyTemp	AzTemp	Length
        save_title_list = [
            'Turntable', 'Gx(deg/h)', 'Gy(deg/h)', 'Gz(deg/h)', 'Ax(m/s2)', 'Ay(m/s2)','Az(m/s2)',
            'GxTemp', 'GyTemp', 'GzTemp', 'AxTemp', 'AyTemp', 'AzTemp', 'Length'
        ]
        try:
            with open(save_file_path, 'w+', newline='', encoding='gb2312') as f:
                f.write('{}\n'.format('\t'.join(save_title_list)))
        except Exception as e:
            self.append_degugMsg('初始化保存文件失败:\n {}'.format(e))
        

    def format_all_data(self):
        format_count = self.list_input_data[13]
        save_data_accuracy = self.list_input_data[14]
        try: format_count = int(format_count)
        except: format_count = 10
        try: save_data_accuracy = int(save_data_accuracy)
        except: save_data_accuracy = 6
        path = self.folder_path
        if os.path.isdir(os.path.join(path, 'all_ave')):
            pass
        elif os.path.basename(path) == 'all_ave':
            path = os.path.dirname(path)
        else:
            self.debug_info = '未找到all_ave文件夹'
            return
        ave_path = os.path.join(path, 'all_ave')
        format_path = os.path.join(path, 'all_format')
        if os.path.exists(format_path):
            shutil.rmtree(format_path)
        os.makedirs(format_path)
        total_folder = 1
        total_file = 0
        total_error = 0
        # 遍历文件夹
        for filename in os.listdir(ave_path):
            if not filename.endswith('.txt'):
                continue
            total_file += 1
            total_error+=1
            try:
                df = pd.read_csv(os.path.join(ave_path, filename), encoding='gb2312', delim_whitespace=True)
            except Exception as e:
                print('读取文件{}失败:\n {}'.format(filename, e))
                continue
            sdf = pd.concat([
                df.iloc[:, 1:7],  # 6 列
                pd.DataFrame(0, index=df.index, columns=[f"zero{i}" for i in range(3)]),  # 3 列 0
                df.iloc[:, 7:13], # 6 列
                pd.DataFrame(0, index=df.index, columns=[f"zero{i}" for i in range(4)])   # 4 列 0
            ], axis=1)
            save_name = filename.split('.txt')[0] + '_format.txt'
            save_data = sdf.values.tolist()
            f = open(os.path.join(format_path, save_name),'w+')
            count = 0
            for line in save_data:
                # save_line = '\t'.join([ '{:.6f}'.format(data) for data in line ])
                save_line = '\t'.join([f"{data:.{save_data_accuracy}f}" for data in line ])
                for i in range(format_count):
                    count+=1
                    if i==(format_count-1): end = 's\n'
                    else: end = '\n'
                    f.write('{}\t'.format(count)+save_line+end)
            f.close()
            total_error-=1
            
        self.debug_info = f'文件夹：{total_folder}，文件：{total_file}，错误：{total_error}'


    def cal_all_para(self):
        # 初始化文件夹
        path = self.folder_path
        if os.path.isdir(os.path.join(path, 'all_ave')):
            pass
        elif os.path.basename(path) == 'all_ave':
            path = os.path.dirname(path)
        else:
            self.debug_info = '未找到all_ave文件夹'
            return
        ave_path = os.path.join(path, 'all_ave')
        para_path = os.path.join(path, 'all_para')
        polyfit_path = os.path.join(path, 'all_polyfit')
        if os.path.exists(para_path):
            shutil.rmtree(para_path)
        os.makedirs(para_path)
        if os.path.exists(polyfit_path):
            shutil.rmtree(polyfit_path)
        os.makedirs(polyfit_path)
        
        # 遍历文件生成参数表和总参数表
        total_folder = 1
        total_file = 0
        total_error = 0
        for filename in os.listdir(ave_path):
            if not filename.endswith('.txt'):
                continue
            total_file+=1
            total_error+=1
            try:
                df = pd.read_csv(os.path.join(ave_path, filename), encoding='gb2312', delim_whitespace=True)
                if (df.shape[0] < 19) or (df.shape[1] < 13):
                    print('文件{}尺寸不正确{}'.format(filename, df.shape))
                    continue
            except Exception as e:
                print('读取文件{}失败:\n {}'.format(filename, e))
                continue
            para_name = filename.split('.txt')[0] + '_para.txt'
            self.cal_paraSave(df,os.path.join(para_path, para_name))
            total_error-=1
        # self.cal_para_polyFit(para_path,polyfit_path)
        self.debug_info = f'文件夹：{total_folder}，文件：{total_file}，错误：{total_error}'
        

        
    # 计算参数
    def cal_paraSave(self,df,save_name):
        if df.columns[0].lower() == 'turntable':
            df = df.drop(df.columns[0], axis=1).reset_index(drop=True)
        save_data_accuracy = self.list_input_data[14]
        try: save_data_accuracy = int(save_data_accuracy)
        except: save_data_accuracy = 6
        degree = self.list_input_data[16]
        try:degree = int(degree)
        except:degree = 1
        # 零位列表
        list_ave = [
            [0,2],
            [1,3,4,6],
            [5,7]
        ]
        list_gZ = [
            [1],
            [0,7],
            [4]
        ]
        list_gF = [
            [3],
            [2,5],
            [6]
        ]
        # 标度列表
        list_scale = [
            [8,10,9,11],
            [18,16,19,17],
            [14,13,15,12]
        ]
        list_turntable = [10,-10,30,-30]
        sdf = init_sdf()
        for i in range(3):
            # 计算零位及正负G
            sdf.iloc[i,0] = np.mean([df.iloc[idx,i] for idx in list_ave[i]])
            sdf.iloc[i+3,0] = np.mean([df.iloc[idx,i+3] for idx in list_ave[i]])
            sdf.iloc[i,1] = np.mean([df.iloc[idx,i] for idx in list_gZ[i]])
            sdf.iloc[i+3,1] = np.mean([df.iloc[idx,i+3] for idx in list_gZ[i]]) 
            sdf.iloc[i,2] = np.mean([df.iloc[idx,i] for idx in list_gF[i]])
            # 计算正负标度（不减零位）
            sdf.iloc[i+3,2] = np.mean([df.iloc[idx,i+3] for idx in list_gF[i]])
            sdf.iloc[i,3] = np.mean([  df.iloc[list_scale[i][j*2],i] / list_turntable[j*2]  for j in range(2) ])
            sdf.iloc[i+3,3] = np.mean([df.iloc[idx,i+3] for idx in list_gZ[i]])
            sdf.iloc[i,4] = np.mean([  df.iloc[list_scale[i][j*2+1],i] / list_turntable[j*2+1] for j in range(2) ])
            sdf.iloc[i+3,4] = np.mean([df.iloc[idx,i+3] for idx in list_gF[i]])
            # 计算非线性度
            # 拟合函数时是否减零位
            data_x = np.array([ df.iloc[idx,i]-sdf.iloc[i,0] for idx in list_scale[i] ])
            # data_x = np.array([ df.iloc[idx,i] for idx in list_scale[i] ])
            data_y = np.array(list_turntable)
            fits = np.polyfit(data_y, data_x, degree)
            y_fit = np.polyval(fits, data_y)
            errors = data_x - y_fit
            sdf.iloc[i,5] = np.abs(errors/fits[0]*1e6/(np.max(list_turntable))).max()
            sdf.iloc[i+3,5] = 0
            # 计算非正交角（减零位）
            begin_axis = np.min(list_scale[i])
            length_axis = len(list_scale[i])
            for j in range(3):
                if i==j: sdf.iloc[i,j+6] = fits[0]
                else:
                    zd_data = df.iloc[begin_axis:length_axis+begin_axis,i] - sdf.iloc[i,0]
                    cd_data = df.iloc[begin_axis:length_axis+begin_axis,j] - sdf.iloc[j,0]
                    sdf.iloc[i,j+6] = (np.arcsin(cd_data/zd_data)/np.pi*180*60).mean()
                    
            for j in range(3):
                if i==j: sdf.iloc[i+3,j+6] = (sdf.iloc[i,1]-sdf.iloc[i,2])/2
                else:
                    sdf.iloc[i+3,j+6] = np.mean([
                        np.arcsin(
                            (df.iloc[axis,j+3]- sdf.iloc[j+3,0]) / (df.iloc[axis,i+3]-sdf.iloc[i+3,0])
                            )/np.pi*180*60 for axis in (list_gZ[i]+list_gF[i])
                        ])
        sdf.iloc[0:6,9] = df.iloc[0:6,6:12].mean(axis=0).to_numpy()
        sdf.to_csv(save_name,sep='\t',encoding='gb2312', float_format=f"%.{save_data_accuracy}f",index_label="axis")
            
    def cal_all_polyfit(self):
        # 初始化文件夹
        path = self.folder_path
        if os.path.isdir(os.path.join(path, 'all_ave')):
            pass
        elif os.path.basename(path) == 'all_ave':
            path = os.path.dirname(path)
        else:
            self.debug_info = '未找到all_ave文件夹'
            return
        para_path = os.path.join(path, 'all_para')
        polyfit_path = os.path.join(path, 'all_polyfit')
        if os.path.exists(polyfit_path):
            shutil.rmtree(polyfit_path)
        os.makedirs(polyfit_path)
        self.cal_para_polyFit(para_path,polyfit_path)    
            
    def cal_para_polyFit(self,para_path,polyfit_path):
        font = 16
        degree = self.list_input_data[17]
        try:degree = int(degree)
        except:degree = 1
        save_data_accuracy = self.list_input_data[14].strip()
        try:save_data_accuracy = int(save_data_accuracy)
        except:save_data_accuracy = 6
        split_rule =  self.list_input_data[15]
        try:split_rule = [split_rule.split()[0], int(split_rule.split()[1])]
        except:
            self.debug_info+='[任务排序]输入错误'
            split_rule = ['_',1]
        list_columns = [
            "零位", "正G", "负G", 
            "正标度", "负标度", "非线性度", 
            "K*x", "K*y", "K*z", 
            "Temp"
        ]
        list_rows = ["Gx", "Gy", "Gz", "Ax", "Ay", "Az"]
        list_all_dfFit = []
        for title in list_columns:
            df_fit = pd.DataFrame([])
            list_all_dfFit.append(df_fit)
        list_regex = [filename for filename in os.listdir(para_path) if 'para.txt' in filename]
        list_regex = sorted(list_regex,key=lambda x:sort_key(x, split_rule))
        total_img = 0
        total_file = 0
        total_error = 0
        for filename in list_regex:
            total_file+=1
            total_error+=1
            df = pd.read_csv(os.path.join(para_path, filename), encoding='gb2312', delim_whitespace=True)
            if df.columns[0].lower() == 'axis':
                df = df.drop(df.columns[0], axis=1)
            for axis in range(df.shape[1]): 
                list_all_dfFit[axis] = pd.concat([list_all_dfFit[axis],df.iloc[:,axis]],axis=1)
            total_error-=1
        save_fitname1 = 'all_polyfit.txt'
        save_fitname2 = 'all_fiterrors.txt'
        f1 = open(os.path.join(polyfit_path,save_fitname1),'w+',encoding='gb2312')
        f2 = open(os.path.join(polyfit_path,save_fitname2),'w+',encoding='gb2312')
        for i in range(6):
            save_msg1 = '[{}_{}阶拟合]\n'.format(list_columns[i],degree)
            save_msg2 = '[{}_拟合残差]\n'.format(list_columns[i])
            for j in range(2):
                total_error+=1
                GA_title = list_rows[j*3:(j+1)*3]
                fig,ax = plt.subplots(1,3,figsize=(18,6))
                for k in range(3):
                    ax[k].set_ylabel(GA_title[k],fontsize=font)
                    ax[k].set_xlabel('Temp',fontsize=font)
                    ax[k].set_title('{}_polyFit'.format(list_columns[i]))
                    ax[k].grid(alpha=0.5)
                    data_y = list_all_dfFit[-1].iloc[j*3+k,:]
                    data_x = list_all_dfFit[i].iloc[j*3+k,:]
                    ax[k].plot(data_y,data_x,'o',label='原始数据')
                    fits = np.polyfit(data_y, data_x, degree)
                    y_fit = np.polyval(fits, data_y)
                    errors = data_x - y_fit
                    data_y_new = np.linspace(data_y.min(), data_y.max(), 100)  
                    y_fit_new = np.polyval(fits, data_y_new)
                    ax[k].scatter(data_y,errors+data_x.mean(),label="残差", color="green", marker="x")
                    ax[k].plot(data_y_new,y_fit_new,label=f"{degree}阶拟合", color="red")
                    ax[k].legend()
                    save_msg1 += '{}:{};\n'.format(
                        GA_title[k],
                        ','.join([f'{fit:.{save_data_accuracy}f}' for fit in fits])
                    )
                    save_msg2+='{}:{};\n'.format(
                        GA_title[k],
                        ','.join([f'{error:.{save_data_accuracy}f}' for error in errors])
                    )
                save_msg1+='\n'
                save_msg2+='\n'
                save_name = str(i)+'_'+''.join(GA_title)+'_{}_degree{}.png'.format(list_columns[i],degree)
                plt.savefig(os.path.join(polyfit_path,save_name))
                total_img+=1
                plt.close(fig)
                total_error-=1
            f1.write(save_msg1)
            f2.write(save_msg2)
        axis_title = list_columns[6:9]
        save_msg1 = '[{}_{}阶拟合]\n'.format(','.join(axis_title),degree)
        save_msg2 = '[{}_拟合残差]\n'.format(','.join(axis_title))
        for j in range(2):
            total_error+=1
            GA_title = list_rows[j*3:(j+1)*3]
            fig,ax = plt.subplots(3,3,figsize=(18,12))
            for i in range(3):
                for k in range(3):
                    ax[i,k].set_ylabel(GA_title[i],fontsize=font)
                    ax[i,k].set_xlabel('{}Temp'.format(' '*30),fontsize=font)
                    ax[i,k].set_title('{}_{}_polyFit'.format(GA_title[i],axis_title[k]))
                    ax[i,k].grid(alpha=0.5)
                    data_y = list_all_dfFit[-1].iloc[j*3+k,:]
                    data_x = list_all_dfFit[i+6].iloc[j*3+k,:]
                    fits = np.polyfit(data_y, data_x, degree)
                    y_fit = np.polyval(fits, data_y)
                    errors = data_x - y_fit
                    data_y_new = np.linspace(data_y.min(), data_y.max(), 100)  
                    y_fit_new = np.polyval(fits, data_y_new)
                    ax[i,k].plot(data_y,data_x,'o',label='原始数据')
                    ax[i,k].scatter(data_y,errors+data_x.mean(),label="残差", color="green", marker="x")
                    ax[i,k].plot(data_y_new,y_fit_new,label=f"{degree}阶拟合", color="red")
                    ax[i,k].legend()
                    save_msg1 += '{}-{}:{};\n'.format(
                        GA_title[i],
                        axis_title[k],
                        ','.join([f'{fit:.{save_data_accuracy}f}' for fit in fits])
                    )
                    save_msg2+='{}-{}:{};\n'.format(
                        GA_title[i],
                        axis_title[k],
                        ','.join([f'{error:.{save_data_accuracy}f}' for error in errors])
                    )
                save_msg1+='\n'
                save_msg2+='\n'
            save_name = '{}_{}_[{}]_degree{}.png'.format(
                str(i+6),''.join(GA_title),''.join(axis_title),degree 
                )
            save_name = re.sub(r'[\\/:*?"<>|]', "n", save_name) 
            plt.savefig(os.path.join(polyfit_path,save_name))
            total_img+=1
            plt.close(fig)
            total_error-=1
        f1.write(save_msg1)
        f2.write(save_msg2)
        f1.close()
        f2.close()
        self.debug_info = f'图像：{total_img}，文件：{total_file}，错误：{total_error}'
        
    
    def cal_all_para_chy(self):
        # 初始化变量
        split_rule_list = []
        for i in range(3):
            rule = self.list_input_data[18+i].strip()
            try:
                split_rule = re.split(r'[\s,，]+',rule) 
                rule = [split_rule[0],split_rule[1], int(split_rule[2])]
            except:
                rule = ['notFoundRule','_',1]
            split_rule_list.append(rule+[i])
        # 初始化文件夹
        path = self.folder_path
        if os.path.isdir(os.path.join(path, 'all_ave')):
            pass
        elif os.path.basename(path) == 'all_ave':
            path = os.path.dirname(path)
        else:
            self.debug_info = '未找到all_ave文件夹'
            return
        ave_path = os.path.join(path, 'all_ave')
        para_path = os.path.join(path, 'all_para')
        if os.path.exists(para_path):
            shutil.rmtree(para_path)
        os.makedirs(para_path)
        total_folder = 1
        total_file = 0
        total_error = 0
        for filename in os.listdir(ave_path):
            if not filename.endswith('.txt'):
                continue
            split_in_name = any([re.search(r[0], filename) and re.search(r[1], filename) for r in split_rule_list])
            if not split_in_name:
                continue
            split_rule = [r for r in split_rule_list if re.search(r[0], filename) and re.search(r[1], filename)][0]
            try:
                df = pd.read_csv(os.path.join(ave_path, filename), encoding='gb2312', delim_whitespace=True)
                # 跳过静态数据和尺寸不对的数据
                if split_rule[3]==2:
                    continue
                if df.shape[0] < 2 or df.shape[1] < 13:
                    print('文件{}尺寸不正确{}'.format(filename, df.shape))
                    continue
            except Exception as e:
                print('读取文件{}失败:\n {}'.format(filename, e))
                continue
            para_name = filename.split('.txt')[0] + '_chip.txt'
            # 处理零位数据
            if split_rule[3]==0:
                self.cal_paraSave_chy_LW(df,os.path.join(para_path, para_name))
            # 处理标度数据
            elif split_rule[3]==1:
                self.cal_paraSave_chy_SL(df,os.path.join(para_path, para_name))
            # 处理静态数据
            elif split_rule[3]==2:
                self.cal_paraSave_chy_JT(df,os.path.join(para_path, para_name))
            else:
                self.debug_info+='未识别的任务排序\n'
                continue
    # 执行处理零位数据操作 G0 G± A0 A± AKxx
    def cal_paraSave_chy_LW(self,df,save_name):
        save_data_accuracy = self.list_input_data[14].strip()
        g0_sort_rule = self.list_input_data[21].strip()
        a1_sort_rule = self.list_input_data[22].strip()
        GA_shift = self.list_input_data[26].strip()
        zfG_encode = self.list_input_data[27].strip()
        try: save_data_accuracy = int(save_data_accuracy)
        except: save_data_accuracy = 6
        try:
            split_data = re.split(r'[\s,，]+',g0_sort_rule)
            g0_sort_rule = [int(split_data[0]),int(split_data[1]), int(split_data[2])]
        except: g0_sort_rule = [0,1,2]
        try:
            split_data = re.split(r'[\s,，]+',a1_sort_rule)
            a1_sort_rule = [int(split_data[0]),int(split_data[1]), int(split_data[2])]
        except: a1_sort_rule = [1,0,2]
        try:
            split_data = re.split(r'[\s,，]+',GA_shift)
            GA_shift = [int(split_data[0]),int(split_data[1]), int(split_data[2])]
        except: GA_shift = [4,4,4]
        zfG_decode = decode_zfG(zfG_encode,GA_shift[1])
        sdf = init_sdf()
        if df.columns[0].lower() == 'turntable':
            df = df.drop(df.columns[0], axis=1).reset_index(drop=True)
        for i in range(3):
            sdf.iloc[g0_sort_rule[i],0] = df.iloc[ GA_shift[0]*i:GA_shift[0]*(i+1),g0_sort_rule[i] ].mean()
            sdf.iloc[g0_sort_rule[i]+3,0] = df.iloc[ GA_shift[0]*i:GA_shift[0]*(i+1),g0_sort_rule[i]+3 ].mean()
            # 正负输出
            sdf.iloc[a1_sort_rule[i],1] = np.mean([
                df.iloc[num+GA_shift[2]+GA_shift[1]*i,a1_sort_rule[i]] for num in zfG_decode[i][0]
            ])
            sdf.iloc[a1_sort_rule[i]+3,1] = np.mean([
                df.iloc[num+GA_shift[2]+GA_shift[1]*i,a1_sort_rule[i]+3] for num in zfG_decode[i][0]
            ])
            sdf.iloc[a1_sort_rule[i],2] = np.mean([
                df.iloc[num+GA_shift[2]+GA_shift[1]*i,a1_sort_rule[i]]   for num in zfG_decode[i][1]    
            ])
            sdf.iloc[a1_sort_rule[i]+3,2] = np.mean([
                df.iloc[num+GA_shift[2]+GA_shift[1]*i,a1_sort_rule[i]+3] for num in zfG_decode[i][1]
            ])
            sdf.iloc[a1_sort_rule[i]+3,3] = sdf.iloc[a1_sort_rule[i]+3,1]
            sdf.iloc[a1_sort_rule[i]+3,4] = sdf.iloc[a1_sort_rule[i]+3,2]
            sdf.iloc[0:6,9] = df.iloc[0:6,6:12].mean(axis=0).to_numpy()
        for count,i in enumerate(a1_sort_rule):
            zd_data = df.iloc[GA_shift[2]+GA_shift[1]*i:GA_shift[2]+GA_shift[1]*(i+1),count+3]
            for j in range(3):
                if count==j:result = (sdf.iloc[i+3,1]-sdf.iloc[i+3,2])/2
                else:
                    cd_data = df.iloc[GA_shift[2]+GA_shift[1]*i:GA_shift[2]+GA_shift[1]*(i+1),j+3]
                    result = (np.arcsin(cd_data/zd_data)/np.pi*180*60).mean()
                sdf.iloc[j+3,count+6] = result

        sdf.to_csv(save_name,sep='\t',encoding='gb2312', float_format=f"%.{save_data_accuracy}f",index_label="axis")
        
    def cal_paraSave_chy_SL(self,df,save_name):
        save_data_accuracy = self.list_input_data[14].strip()
        try: save_data_accuracy = int(save_data_accuracy)
        except: save_data_accuracy = 6
        sl_sort_list = self.list_input_data[23].strip()
        try:
            sl_sort_list = re.split(r'[\s,，]+',sl_sort_list)
            sl_sort_list = [int(sl_sort_list[0]),int(sl_sort_list[1]), int(sl_sort_list[2])]
        except: sl_sort_list = [0,1,2]
        sl_point_list = self.list_input_data[24].strip()
        try:
            sl_point_list_split = re.split(r'[\s,，]+',sl_point_list)
            sl_point_list = []
            if len(sl_point_list_split) != 1:
                for point in sl_point_list_split:
                    sl_point_list.append(int(point))
            else:
                sl_point_list = int(sl_point_list_split[0])
        except: sl_point_list = [10,50,100,150,180]
        sl_para_list = self.list_input_data[25].strip()
        try:
            sl_para_list = re.split(r'[\s,，]+',sl_para_list)
            if len(sl_para_list)==1:
                sl_para_list = [float(sl_para_list[0])]*3
            else:
                sl_para_list = [float(sl_para_list[0]),float(sl_para_list[1]), float(sl_para_list[2])]
        except: sl_para_list = [1,1,1]
        degree = self.list_input_data[16].strip()
        try:degree = int(degree)
        except:degree = 1

        if type(sl_point_list)==int:
            sl_point_list*=2
            sl_point_length = sl_point_list
        elif type(sl_point_list)==list:
            sl_point_list = [i*j for i in sl_point_list for j in [1,-1]]
            sl_point_length = len(sl_point_list)
        else:
            print('速率计数点数输入错误，默认5点')
        def get_max_abs_with_sign(s):
            s = s.replace('[', '').replace(']', '')
            parts = s.split('_')
            nums = []
            for pnum in parts:
                try: nums.append(float(pnum))
                except: pass
            if not nums: 
                return None
            max_num = max(nums, key=lambda x: abs(x))
            return max_num

        sdf = init_sdf()
        if df.columns[0].lower() == 'turntable':
            # 将第一列用下划线分隔并获取绝对值最大的数据,保留正负
            df.iloc[:,0] = df.iloc[:,0].apply(get_max_abs_with_sign)
        fig,ax = plt.subplots(1,3,figsize=(18,6))
        for count,i in enumerate(sl_sort_list):
            data_x = df.iloc[count*sl_point_length:(count+1)*sl_point_length,i+1].reset_index(drop=True)*sl_para_list[i]
            data_x_lw = data_x.mean()
            if type(sl_point_list)==list:
                data_y = pd.Series(sl_point_list).reset_index(drop=True)
            else:
                data_y = df.iloc[count*sl_point_length:(count+1)*sl_point_length,0].reset_index(drop=True)
            fits = np.polyfit(data_x-data_x_lw, data_y, degree)
            y_fit = np.polyval(fits, data_y)
            errors = data_x-data_x_lw - y_fit
            data_y_new = np.linspace(data_y.min(), data_y.max(), 100)  
            y_fit_new = np.polyval(fits, data_y_new)
            ax[i].scatter(data_y, (data_x-data_x_lw)/data_y, label='原始数据')
            ax[i].plot(y_fit_new, data_y_new/y_fit_new, color='red', label='拟合曲线',linewidth=2)
            ax[i].plot(data_y,1/fits[-2]*data_y/data_y,label='拟合标度倒数', color='orange', linestyle='--')
            ax[i].set_xlabel('转台速率')
            ax[i].set_ylabel('实际输出/转台速率')
            ax[i].set_title('{}轴标度非线性度拟合'.format('XYZ'[i]))
            ax[i].legend()
            ax[i].grid(alpha=0.5)
            ax[i].yaxis.set_major_formatter(ScalarFormatter(useMathText=False))
            ax[i].yaxis.get_major_formatter().set_scientific(False)
            ax[i].yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.6f}'.format(y)))
            sdf.iloc[i,3] = ((data_x[data_y>0])/(data_y[data_y>0])).mean()
            sdf.iloc[i,4] = ((data_x[data_y<0])/(data_y[data_y<0])).mean()
            sdf.iloc[i,5] = (errors/data_y/fits[0]).abs().max()*1e6/180
            zd_data = data_x - data_x_lw
            for j in range(3):
                if i==j:
                    result = fits[-2]
                else:
                    cd_data = df.iloc[count*sl_point_length:(count+1)*sl_point_length,j+1].reset_index(drop=True)*sl_para_list[j]
                    result = (np.arcsin(cd_data/zd_data)/np.pi*180*60).mean()
                sdf.iloc[j,i+6] = result
        sdf.to_csv(save_name,sep='\t',encoding='gb2312', float_format=f"%.{save_data_accuracy}f",index_label="axis")


    def cal_paraSave_chy_JT(self,df,save_name):
        pass
    def cal_all_polyfit_chy(self):
        print('chy拟合曲线')
        pass