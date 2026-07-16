from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from Automated_testing import Ui_MainWindow
from pyqtgraph.Qt import QtCore
import binascii
import datetime
import os
import serial
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import pandas as pd
import numpy as np
import serial
import serial.tools.list_ports as sports
import threading
import time
import os
import struct

# 设置pandas显示 多列显示和输出对齐
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
# pd.set_option('display.colheader_justify', 'left')
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("通用自动测试上位机_蔡_功能测试版_2404_V0.1")
        self.show_message_length = 30   # 显示的最大行数
        
        # 初始化界面元素
        self.inside_location = 0.0
        self.inside_speed = 0.0
        self.outside_location = 0.0
        self.outside_speed = 0.0
        self.automatic_time = 0          # 自动测试时间  
        self.power_flag = False
        self.plan_name = ''             # 自动标定进度名称
        
        
        # 初始化使用元素
        self.short_time = '000000'
        self.normal_time = '00:00:00'
        self.show_message_automatic_list = []
        self.show_message_singletest = None
        self.show_message_dis1_list = []
        self.show_message_list = []             # 12输出显示
        for i in range(12):
            self.show_message_list.append([])
        self.show_message_dataframe = []        # 12路绘图显示
        for i in range(12):
            self.show_message_dataframe.append(pd.DataFrame([]))
        
        
        # 初始化多线程标志位
        self.test_mode = None
        self.threading_test_flag = False        # 12路测试总标志
        self.threading_list_flag = []           # 12子线程测试标志位
        for i in range(12):
            self.threading_list_flag.append(False)
        self.save_data_flag = False     # 保存数据标志位
        self.save_aver_flag = False     # 标定结束一个位置，取均值
        self.save_ztrd_flag = False     # 转台到位标志位
        self.turntable_ready = False     # 标定可以开始标志位
        self.plan_threading_flag = False# 自动测试标志位
        self.turntable_will_turn = True # 转台转动标志位
        
        # debug调试状态
        self.debug_flag = False
        self.debug_read_rules = False
        self.bebug_binding = False
        self.debug_begin_test = False
        self.debug_threading = True
        self.debug_update_5s = False
        self.debug_update_5s_file = False
        
        # 初始化解算规则列表-新
        self.decode_rule_list = []    # 解算规则
        self.decode_save_list = []    # 是否保存
        self.decode_para_list = []    # 系数
        self.decode_titl_list = []    # 标题
        self.decode_cout_list = []    # 排序序号
        self.decode_sort_list = []    # 排序后列表
        self.decode_edia_list = []    # 大小端
        self.receive_hz = 200
        
        
        # 配置文件路径
        self.para_com_filename = './配置文件/para_com.txt'
        self.para_config_filename = './配置文件/para_config.txt'
        self.model_list = [
            ['通讯','转台','电源','温箱','装订','自动'],
            ['protocal','turntable','power','tempbox','binding','automatic'],
            ['解算规则','标定规则','none','none','装订规则','自动规则']
        ]
        
        # 配置文件默认设置
        self.config_hold_time = 5           # 转台稳定后等待时间
        self.config_save_ms = 0             # 是否保存毫秒值 1True/0False
        self.config_save_BD_average = 1     # 是否将标定过程各点取均值存放
        self.config_save_BD_bin = 1         # 是否保存标定过程中16进制原始数
        self.config_save_BD_1file = 1       # 将标定过程各点存储到一个文件/多个文件
        self.save_decimal_point = 6         # 保存时保留小数点后几位
        self.save_test_title = 1            # 创建文件时将协议中的标题内容一并保存
        self.config_power_model = 1         # 电源型号：1程控电源，2继电器
        self.config_special_flag = None     # 特殊标志位
        self.config_decode_header_type = 1  # 0:使用帧头模式/1:使用2帧头中间模式/2:使用帧头帧尾模式
        
        # 解算规则配置
        self.rules_lists_format = 'xcbB?hHiIlLqQfdspPtyY'   # 解算规则可用范围
        
        # 总控-刷新comboBox串口
        self.comboBox_update_com_flag = True
        self.comboBox_update_rules_flag = True
        self.comboBox_com_list = [self.comboBox_protocal_com, 
                                self.comboBox_turntable_com, 
                                self.comboBox_power_com,
                                self.comboBox_tempbox_com,
                                self.comboBox_binding_com,
                                self.combox_set_com_all]
        self.combox_com_list = [self.combox_set_com_1,
                                self.combox_set_com_2,
                                self.combox_set_com_3,
                                self.combox_set_com_4,
                                self.combox_set_com_5,
                                self.combox_set_com_6,
                                self.combox_set_com_7,
                                self.combox_set_com_8,
                                self.combox_set_com_9,
                                self.combox_set_com_10,
                                self.combox_set_com_11,
                                self.combox_set_com_12]
        self.combox_com_open_list = [self.pushButton_com_open_1,
                                    self.pushButton_com_open_2,
                                    self.pushButton_com_open_3,
                                    self.pushButton_com_open_4,
                                    self.pushButton_com_open_5,
                                    self.pushButton_com_open_6,
                                    self.pushButton_com_open_7,
                                    self.pushButton_com_open_8,
                                    self.pushButton_com_open_9,
                                    self.pushButton_com_open_10,
                                    self.pushButton_com_open_11,
                                    self.pushButton_com_open_12]
        self.comboBox_binding_list = [self.lineEdit_binding_latitude,
                                      self.lineEdit_binding_longitude,
                                      self.lineEdit_binding_height,
                                      self.lineEdit_binding_time]
        # 十二路开关设置
        for i in range(12):
            self.combox_com_open_list[i].clicked.connect(self.change_button)
        for binding in self.comboBox_binding_list:
            binding.textChanged.connect(self.binding_change)
        for combox in self.comboBox_com_list+self.combox_com_list:
            combox.view().setMinimumWidth(85)
            
        # 总控开关切换
        self.pushButton_com_open_all.clicked.connect(self.change_button_all)
        # 单路通讯协议同步多路更新
        self.comboBox_protocal_com.currentTextChanged.connect(self.protocal_com_change)
        self.comboBox_protocal_baund.currentTextChanged.connect(self.protocal_com_change)
        self.comboBox_protocal_check.currentTextChanged.connect(self.protocal_com_change)
        self.combox_set_com_1.currentTextChanged.connect(self.comboBox_com_change)
        self.combox_set_baund_1.currentTextChanged.connect(self.comboBox_com_change)
        self.comboBox_set_check_1.currentTextChanged.connect(self.comboBox_com_change)
        # 多路文件名同步更新
        self.lineEdit_file_names_all.textChanged.connect(self.filenames_change)
        # 规则更新同步
        self.comboBox_protocal_rule.currentTextChanged.connect(self.read_rules)
        self.pushButton_begin_test.clicked.connect(self.begin_test)
        self.pushButton_stop_test.clicked.connect(self.stop_test)
        
        
        # 事件更新计数
        self.show_timer_count0 = 0
        self.show_timer_count1 = 0
        self.show_timer_count2 = 0
        self.show_timer_count3 = 0
        # 打开软件自动更新一次所有状态
        self.show_message_01s()
        self.show_message_05s()
        self.show_message_1s()
        self.show_message_5s()
        
        # 读取默认配置文件
        self.read_default_para_com()
        self.read_default_para_config()
        
        # 事件0.1s更新
        self.show_timer0 = QTimer(self)
        self.show_timer0.timeout.connect(self.show_message_01s)
        self.show_timer0.start(100)
        # 事件0.5s更新
        self.show_timer1 = QTimer(self)
        self.show_timer1.timeout.connect(self.show_message_05s)
        self.show_timer1.start(500)
        # 事件1s更新
        self.show_timer2 = QTimer(self)
        self.show_timer2.timeout.connect(self.show_message_1s)
        self.show_timer2.start(1000)
        # 事件3s更新
        self.show_timer3 = QTimer(self)
        self.show_timer3.timeout.connect(self.show_message_5s)
        self.show_timer3.start(5000)
    
    # 事件更新0.1s线程，用于更新数据输出和绘图
    def show_message_01s(self):
        if len(self.show_message_dis1_list)>0:
            self.textBrowser_progress_display1.append(self.show_message_dis1_list.pop(0))
            self.textBrowser_progress_display1.verticalScrollBar().setValue(self.textBrowser_progress_display1.verticalScrollBar().maximum())

        if len(self.show_message_automatic_list)>0:
            self.textBrowser_automatic_ruleline.append(self.show_message_automatic_list.pop(0))
            self.textBrowser_automatic_ruleline.verticalScrollBar().setValue(self.textBrowser_automatic_ruleline.verticalScrollBar().maximum())
        for i in range(12):
            if len(self.show_message_list[i])>0:
                textBrowsers = self.findChild(QtWidgets.QTextBrowser,'textBrowser_%s'%(i+1))
                textBrowsers.append(self.show_message_list[i].pop(0))
                textBrowsers.verticalScrollBar().setValue(textBrowsers.verticalScrollBar().maximum())
            
            
    # 事件更新0.5s线程，用于更新数据输出和绘图
    def show_message_05s(self):
        self.show_timer_count1 += 1
    # 事件更新1s线程，用于按秒更新界面元素
    def show_message_1s(self):
        self.show_timer_count2 += 1
        self.lcdNumber_inside_location.display('{:.2f}'.format(self.inside_location))
        self.lcdNumber_inside_speed.display('{:.2f}'.format(self.inside_speed))
        self.lcdNumber_outside_location.display('{:.2f}'.format(self.outside_location))
        self.lcdNumber_outside_speed.display('{:.2f}'.format(self.outside_speed))
        self.lcdNumber_automatic_time.display(int(self.automatic_time))
        self.radioButton_power_flag.setChecked(self.power_flag)
        # 转换时分秒
        self.test_time = datetime.datetime.now().strftime('%H%M%S')
        self.normal_time = datetime.datetime.now().strftime('%H:%M:%S')
        # 绘图
        '''
        plot_axis = self.comboBox_multiple_choice.currentText()
        axis_list = []
        # title_list = []
        for i in range(3):
            plot_axis_text = self.findChild(QtWidgets.QLineEdit, 'lineEdit_plot_axis_{}'.format(i+1)).text()
            try:
                axis_list.append(int(plot_axis_text.split()[0]))
            except:
                axis_list.append(i+1)
            '''
    # 事件更新5s线程，用于更新串口等对时间不敏感内容
    def show_message_5s(self):
        self.show_timer_count3 += 1
        # 更新串口  #串口更新
        if self.comboBox_update_com_flag:
            plist = list(serial.tools.list_ports.comports())
            com_lists = []
            for com in plist:
                com_lists.append(str(list(com)[0]))
            # com_lists.sort()
            com_lists = sorted(com_lists,key=lambda x:int(x[3:]))
            for comboBox in self.comboBox_com_list+self.combox_com_list:
                comboBox_com_list = []
                for count in range(comboBox.count()):
                    comboBox_com_list.append(comboBox.itemText(count))
                try:    
                    comboBox_com_list.remove('None')
                except:
                    if self.debug_update_5s:
                        print('comboBox_com_list中没有None项:{}'.format(comboBox_com_list))
                comboBox_com_list = sorted(comboBox_com_list,key=lambda x:int(x[3:]))
                if comboBox_com_list==com_lists:
                    if self.debug_update_5s:
                        print('没有新的com口')
                    continue
                elif self.debug_update_5s:
                    print('选择了新的com口:{}'.format(com_lists))
                select_combo = comboBox.currentText()
                comboBox.clear()
                comboBox.addItem('None')
                for com in com_lists:
                    comboBox.addItem(com)
                comboBox.setCurrentText(select_combo)
                # if select_combo in com_lists:
                #     comboBox.setCurrentText(select_combo)
                # else:
                #     comboBox.setCurrentIndex(0)
        # 更新规则文件 #协议更新
        if self.comboBox_update_rules_flag:
            model_list = self.model_list
            for i in range(len(model_list[0])):
                file_path = model_list[2][i]
                if file_path.lower()=='none':
                    continue
                file_list = []
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                for file_name in os.listdir('./'+file_path):
                    file_name = file_name.split('.txt')[0]
                    file_list.append(file_name)
                file_list.sort()
                
                comboBox = self.findChild(QtWidgets.QComboBox,'comboBox_%s_rule'%(model_list[1][i]))
                comboBox_file_list = []
                for count in range(comboBox.count()):
                    comboBox_file_list.append(comboBox.itemText(count))
                try:    
                    comboBox_file_list.remove('选择协议')
                except:
                    if self.debug_update_5s_file:
                        print('comboBox_file_list中没有选择协议项:{}'.format(comboBox_file_list))
                if comboBox_file_list==file_list:
                    if self.debug_update_5s_file:
                        print('没有新的协议')
                    continue
                else:
                    if self.debug_update_5s_file:
                        print('comboBox_file_list:{}\nfile_list:{}'.format(comboBox_file_list,file_list))
                if comboBox is None:
                    if self.debug_update_5s_file:
                        print('未找到对应控件：comboBox_%s_rule'%(model_list[1][i]))
                    continue
                select_combo = comboBox.currentText()
                comboBox.clear()
                comboBox.addItem('选择协议')
                for rule in file_list:
                    comboBox.addItem(rule)
                # comboBox.setCurrentText(select_combo)
                if select_combo in file_list:
                    comboBox.setCurrentText(select_combo)
                else:
                    comboBox.setCurrentIndex(0)
            
    # 多路开关按钮切换 20240425
    def change_button(self):
        sender = self.sender()
        sender.setText('开启') if sender.text()=='关闭' else sender.setText('关闭')
    # 多路开关总控 20240425
    def change_button_all(self):
        sender = self.sender()
        set_text = '开启' if sender.text()=='关闭' else '关闭'
        sender.setText(set_text)
        for i in range(12):
            button = self.findChild(QtWidgets.QPushButton,'pushButton_com_open_%s'%(i+1))
            if button is not None:
                button.setText(set_text)
            else:
                print('未找到对应控件：pushButton_com_open_%s'%(i+1))
    # 单路多路同步更新 20240425
    def protocal_com_change(self):
        protocal_com = self.comboBox_protocal_com.currentText()
        protocal_baund = self.comboBox_protocal_baund.currentText()
        protocal_check = self.comboBox_protocal_check.currentText()
        self.combox_set_com_1.setCurrentText(protocal_com)
        self.combox_set_baund_1.setCurrentText(protocal_baund)
        self.comboBox_set_check_1.setCurrentText(protocal_check)
    def comboBox_com_change(self):
        protocal_com = self.combox_set_com_1.currentText()
        protocal_baund = self.combox_set_baund_1.currentText()
        protocal_check = self.comboBox_set_check_1.currentText()
        self.comboBox_protocal_com.setCurrentText(protocal_com)
        self.comboBox_protocal_baund.setCurrentText(protocal_baund)
        self.comboBox_protocal_check.setCurrentText(protocal_check)
    # 多路文件名同步更新 20240425
    def filenames_change(self):
        filenames = self.lineEdit_file_names_all.text()
        for i in range(12):
            lineEdit = self.findChild(QtWidgets.QLineEdit,'lineEdit_file_names_%s'%(i+1))
            if lineEdit is not None:
                lineEdit.setText(filenames+'_'+str(i+1))
            else:
                print('未找到对应控件：lineEdit_file_names_%s'%(i+1))
    # 读取默认配置文件-全局串口 20240427
    def read_default_para_com(self):
        # 串口默认配置
        para_name = self.para_com_filename
        if not os.path.exists(para_name):
            self.textBrowser_automatic_ruleline.append('未读取到默认配置文件({})'.format(para_name))
        else:
            with open(para_name,'r',encoding='gb2312',errors='replace') as f:
                for line in f:
                    para_rule_list = line.split()
                    if line.startswith('#'):
                        continue
                    elif len(para_rule_list)<3:
                        continue
                    elif para_rule_list[1]=='protocal':
                        self.comboBox_protocal_com.setCurrentText(para_rule_list[2])
                        self.comboBox_protocal_baund.setCurrentText(para_rule_list[3])
                        self.comboBox_protocal_check.setCurrentText(para_rule_list[4])
                    elif para_rule_list[1]=='turntable':
                        self.comboBox_turntable_com.setCurrentText(para_rule_list[2])
                    elif para_rule_list[1]=='power':
                        self.comboBox_power_com.setCurrentText(para_rule_list[2])
                    elif para_rule_list[1]=='temp':
                        self.comboBox_tempbox_com.setCurrentText(para_rule_list[2])
                    elif para_rule_list[1]=='binding':
                        self.comboBox_binding_com.setCurrentText(para_rule_list[2])
                    elif 'tab_' in para_rule_list[1]:
                        self.findChild(QtWidgets.QComboBox,'combox_set_com_%s'%(para_rule_list[1][4:])).setCurrentText(para_rule_list[2])
                        self.findChild(QtWidgets.QComboBox,'combox_set_baund_%s'%(para_rule_list[1][4:])).setCurrentText(para_rule_list[3])
                        self.findChild(QtWidgets.QComboBox,'comboBox_set_check_%s'%(para_rule_list[1][4:])).setCurrentText(para_rule_list[4])
                        self.findChild(QtWidgets.QComboBox,'comboBox_stopbit_%s'%(para_rule_list[1][4:])).setCurrentText(para_rule_list[5])
                        self.findChild(QtWidgets.QPushButton,'pushButton_com_open_%s'%(para_rule_list[1][4:])).setText(para_rule_list[6])
                    else:
                        self.textBrowser_automatic_ruleline.append('未知配置项：%s'%(para_rule_list))
    # 读取默认配置文件-全局设置 20240507
    def read_default_para_config(self):
        para_name = self.para_config_filename
        if not os.path.exists(para_name):
            self.textBrowser_automatic_ruleline.append('未读取到默认配置文件({})'.format(para_name))
        else:
            with open(para_name,'r',encoding='gb2312',errors='replace') as f:
                for line in f:
                    para_rule_list = line.split()
                    if line.startswith('#'):
                        continue
                    elif len(para_rule_list)<3:
                        continue
                    # 默认转台速度设置
                    elif para_rule_list[1]=='in_spd':
                        self.lineEdit_inside_speed.setText(para_rule_list[2])
                    elif para_rule_list[1]=='in_acc':
                        self.lineEdit_inside_acceleration.setText(para_rule_list[2])
                    elif para_rule_list[1]=='out_spd':
                        self.lineEdit_outside_speed.setText(para_rule_list[2])
                    elif para_rule_list[1]=='out_acc':
                        self.lineEdit_outside_acceleration.setText(para_rule_list[2])
                    # 默认转台稳定后等待时间
                    elif para_rule_list[1]=='hold_time':
                        self.config_hold_time = int(para_rule_list[2])
                    # 是否保存毫秒值
                    elif para_rule_list[1]=='save_ms':
                        self.config_save_ms = int(para_rule_list[2])
                    # 是否保存标定各位置均值
                    elif para_rule_list[1]=='save_BD_average':
                        self.config_save_BD_average = int(para_rule_list[2])
                    # 是否将数据保存到一个文件中
                    elif para_rule_list[1]=='save_BD_1file':
                        self.config_save_BD_1file = int(para_rule_list[2])
                    # 保存时保留小数点后几位
                    elif para_rule_list[1]=='save_decimal_point':
                        self.save_decimal_point = int(para_rule_list[2])
                    # 创建文件时将协议中的标题内容一并保存
                    elif para_rule_list[1]=='save_test_title':
                        self.save_test_title = int(para_rule_list[2])
                    # 是否保存标定16进制原始数
                    elif para_rule_list[1]=='save_BD_bin':
                        self.config_save_BD_bin = int(para_rule_list[2])
                    # 程控电源模式/继电器模式
                    elif para_rule_list[1]=='power_model':
                        self.config_power_model = int(para_rule_list[2])
                    # 默认使用对应规则列表中的对应序号
                    elif para_rule_list[1]=='default_protocal':
                        self.comboBox_protocal_rule.setCurrentIndex(int(para_rule_list[2]))
                    elif para_rule_list[1]=='default_turntable':
                        self.comboBox_turntable_rule.setCurrentIndex(int(para_rule_list[2]))
                    elif para_rule_list[1]=='default_binding':
                        self.comboBox_binding_rule.setCurrentIndex(int(para_rule_list[2]))
                    elif para_rule_list[1]=='default_automatic':
                        self.comboBox_automatic_rule.setCurrentIndex(int(para_rule_list[2]))
                    # 默认使用寻找帧头模式
                    elif para_rule_list[1]=='decode_header_type':
                        self.config_decode_header_type = int(para_rule_list[2])
                    else:
                        self.textBrowser_automatic_ruleline.append('未知配置项：%s'%(para_rule_list))
    # 读取载入解算规则文件  20240513
    # 读取规则文件并更新全局变量
    # debug:惯导协议改文件中行60标题无法使用"卫星数"，暂时替换为其他
    def read_rules(self):
        if self.debug_flag:
            print('def_read_rules')
        # 打开规则文件
        try:
            rule_name = self.comboBox_protocal_rule.currentText()
            if len(rule_name)==0:
                if self.debug_flag:
                    print('没有选择规则文件:{}'.format(rule_name))
                return False
            if rule_name=='选择协议':
                return False
            with open('./解算规则/{}.txt'.format(rule_name), 'r',encoding='gb2312',errors='ignore') as file:
                rules = file.read()
                
        except Exception as e:
            self.textBrowser_automatic_ruleline.append('读取规则文件失败:'+str(e))
            return False
        # 规则初始化
        rules_lists_format = self.rules_lists_format
        decode_rule_list = []    # 解算规则
        decode_save_list = []    # 是否保存
        decode_para_list = []    # 系数
        decode_titl_list = []    # 标题
        decode_cout_list = []    # 排序序号
        decode_sort_list = []    # 排序后列表
        decode_edia_list = []    # 大小端

        default_edia = '>'     # 默认大小端

        decode_rule = []
        decode_save = []
        decode_para = []
        decode_titl = []
        decode_cout = []
        
        # 帧头帧尾
        self.decode_rule_header = b'' 
        self.decode_rule_ender = b'' 
        read_line_count = 0
        # 逐行读取规则文件
        for lines in rules.split('\n'):
            read_line_count+=1
            # 规则文件配置项
            if lines.startswith('#'):
                if len(lines.split())<3:
                    print('规则文件长度过少:{}'.format(lines))
                    continue
                # 波特率
                elif lines.split()[1].lower() == 'baund':
                    self.comboBox_protocal_baund.setCurrentText(lines.split()[2])
                    self.combox_set_baund_all.setCurrentText(lines.split()[2])
                # 校验位
                elif lines.split()[1].lower() == 'check':   
                    self.comboBox_protocal_check.setCurrentText(check2chinese(lines.split()[2]))
                    self.comboBox_set_check_all.setCurrentText(check2chinese(lines.split()[2]))
                # 帧头
                elif lines.split()[1].lower() == 'header':
                    self.decode_rule_header = bytes.fromhex(''.join(lines.split()[2:]))
                # 帧尾
                elif lines.split()[1].lower() == 'ender':
                    self.decode_rule_ender = bytes.fromhex(''.join(lines.split()[2:]))
                # 帧率
                elif lines.split()[1].lower() == 'receive_hz':
                    self.receive_hz = try_set_text(lines.split()[2],int,200)
                # 经度
                elif lines.split()[1].lower() == 'longitude':
                    self.lineEdit_binding_longitude.setText(lines.split()[2])
                # 纬度
                elif lines.split()[1].lower() == 'dimensions':
                    self.lineEdit_binding_latitude.setText(lines.split()[2])
                # 高度
                elif lines.split()[1].lower() == 'height':
                    self.lineEdit_binding_height.setText(lines.split()[2])
                # 对准时间
                elif lines.split()[1].lower() == 'alignment_time':
                    self.lineEdit_binding_time.setText(lines.split()[2])
                # 特殊标志位
                elif lines.split()[1].lower() == 'special_flag':
                    self.config_special_flag = lines.split()[2]
                    
                elif lines.split()[1].lower() == 'rulelist':
                    continue
                # 读取规则文件-新
                elif lines.split()[1].lower()=='rulehead':
                    decode_edia_list.append(lines.split()[2])
                    if len(decode_rule)==0:
                        continue
                    else:
                        decode_save_list.append(decode_save)
                        decode_para_list.append(decode_para)
                        decode_titl_list.append(decode_titl)
                        decode_cout_list.append(decode_cout)
                        decode_edia_list.append(default_edia)
                        
                        decode_rule = []
                        decode_save = []
                        decode_para = []
                        decode_titl = []
                        decode_cout = []
                    # default_edia = lines.split()[2]
                else:
                    if self.debug_flag | self.debug_read_rules:
                        print('未知规则:<{}>split:<{}>'.format(lines,lines.split()))
                    continue
            # 判断不合法规则
            elif len(lines)==0 | len(lines.split())==0:
                continue
            elif len(lines.split())<5:
                self.textBrowser_automatic_ruleline.append('规则文件错误:《{}》：《{}》'.format(read_line_count,lines))
                continue
            elif lines.split()[0] not in rules_lists_format:
                self.textBrowser_automatic_ruleline.append('不在解算规则范围内《{}》'.format(lines))
                continue
            # 读取合法规则文件
            else:
                # 读取规则文件-新
                lines_split = lines.split()
                decode_rule.append(lines_split[0])
                decode_save.append(lines_split[1])
                decode_para.append(lines_split[2])
                decode_titl.append(lines_split[3])
                decode_cout.append(lines_split[4])
        # 
        if len(decode_rule)!=0:
            decode_rule_list.append(decode_rule)
            decode_save_list.append(decode_save)
            decode_para_list.append(decode_para)
            decode_titl_list.append(decode_titl)
            decode_cout_list.append(decode_cout)
            # decode_edia_list.append(default_edia)
    
        decode_sort_list = []
        for test_order in decode_cout_list:
            max_count = 0
            sorted_list = []
            for i in range(len(test_order)):
                if str(i) in test_order:
                    continue
                else:
                    max_count = i
                    break
            for i in range(len(test_order)):
                if test_order[i]=='N':
                    sorted_list.append(str(max_count))
                    max_count +=1
                else:
                    sorted_list.append(test_order[i])
            decode_sort_list.append(sorted_list)
        decode_fram_leng = calculate_frame_length(decode_rule_list)
        if self.debug_flag | self.debug_read_rules:
            print('读取规则文件')
            print('decode_rule_list={}'.format(decode_rule_list))
            print('decode_save_list={}'.format(decode_save_list))
            print('decode_para_list={}'.format(decode_para_list))
            print('decode_titl_list={}'.format(decode_titl_list))
            print('decode_cout_list={}'.format(decode_cout_list))
            print('decode_sort_list={}'.format(decode_sort_list))
            print('decode_edia_list={}'.format(decode_edia_list))
            print('decode_fram_leng={}'.format(decode_fram_leng))

        self.decode_rule_list = decode_rule_list    # 解算规则
        self.decode_save_list = decode_save_list    # 是否保存
        self.decode_para_list = decode_para_list    # 系数
        self.decode_titl_list = decode_titl_list    # 标题
        self.decode_cout_list = decode_cout_list    # 排序序号
        self.decode_sort_list = decode_sort_list    # 排序后列表
        self.decode_edia_list = decode_edia_list    # 大小端
        self.decode_fram_leng = decode_fram_leng    # 帧长度
        
        # self.comboBox_begin_axis.clear()
        # for i in range(len(title_sort)):
        #     self.comboBox_begin_axis.addItem('{} {}'.format(i,self.title_sorted[i]))
        # self.comboBox_begin_axis.setCurrentIndex(1)
                                                
        # self.textBrowser_fileCsv.append('主机规则载入完成')      
        # self.fileCsv_append_flag = True
    def binding_change(self):
        if self.bebug_binding:
            print('binding_change')
        binding_latitude = try_get_text(self.lineEdit_binding_latitude,float,0)
        binding_longitude = try_get_text(self.lineEdit_binding_longitude,float,0)
        binding_height = try_get_text(self.lineEdit_binding_height,float,0)
        binding_time = try_get_text(self.lineEdit_binding_time,float,0)
        binding_latitude = int(binding_latitude*1e7)
        binding_longitude = int(binding_longitude*1e7)
        binding_height = int(binding_height)
        binding_time = int(binding_time/5)

        command_list1 = ['55','AA']
        command_list = []
        command_list.append('FF')
        command_list.append('66')
        command_list+=hexcut2list(struct.pack('>i', binding_longitude).hex().upper())
        command_list+=hexcut2list(struct.pack('>i', binding_latitude).hex().upper())
        command_list+=hexcut2list(struct.pack('>i', binding_height).hex().upper())[-2:]
        command_list+=hexcut2list(struct.pack('>i', binding_time).hex().upper())[-1:]
        checks = struct.pack('B',calculate_checksum(bytes.fromhex(''.join(command_list)))).hex().upper()
        command_list.append(checks)
        if self.bebug_binding:
            print(' '.join(command_list1+command_list))
        self.lineEdit_binding_command.setText(' '.join(command_list1+command_list))
        
    def stop_test(self):
        if self.debug_flag:
            print('停止测试')
        self.show_message_automatic_list.append('{} 停止测试'.format(self.normal_time))
        self.threading_test_flag = False
        self.plan_threading_flag = False
    # 点击开始测试事件，判断测试模式
    def begin_test(self):
        if self.debug_flag:
            print('开启测试')
        self.read_rules()
        protocal_rule = self.comboBox_protocal_rule.currentText()
        protocal_com = self.comboBox_protocal_com.currentText()
        protocal_baund = self.comboBox_protocal_baund.currentText()
        protocal_check = self.comboBox_protocal_check.currentText()
        turntable_rule = self.comboBox_turntable_rule.currentText()
        turntable_com = self.comboBox_turntable_com.currentText()
        power_com = self.comboBox_power_com.currentText()
        binding_rule = self.comboBox_binding_rule.currentText()
        tempbox_com = self.comboBox_tempbox_com.currentText()
        automatic_rule = self.comboBox_automatic_rule.currentText()
        
        if self.debug_flag | self.debug_begin_test:
            print('protocal::rule: {}\tcom:{}\tbaund:{}\tcheck:{}'.format(protocal_rule,protocal_com,protocal_baund,protocal_check))
            print('turntable:rule: {}\tcom:{}'.format(turntable_rule,turntable_com))
            print('power_com:rule: {}'.format(power_com))
            print('binding__:rule: {}'.format(binding_rule))
            print('tempbox_c:rule: {}'.format(tempbox_com))
            print('automatic:rule: {}'.format(automatic_rule))
        
        begin_test_mode = 'only_test'
        self.save_aver_flag = False
        self.save_data_flag = False
        self.save_ztrd_flag = False
        self.turntable_ready = False
        
        
        if not ((turntable_rule.lower()=='none')|(turntable_rule.lower()=='选择协议')):
            begin_test_mode = 'turntable_test'
        if not ((automatic_rule.lower()=='none')|(automatic_rule.lower()=='选择协议')):
            begin_test_mode = 'automatic_test'
        self.test_mode = begin_test_mode
        self.show_message_automatic_list.append('{} 模式:{}'.format(self.normal_time,testmode2chinese(begin_test_mode))) 
        if begin_test_mode=='only_test':
            self.save_data_flag = True
            self.turntable_ready = True
            self.only_test()
        elif begin_test_mode=='turntable_test':
            self.bd_test()
        elif begin_test_mode=='automatic_test':
            self.plan_threading_flag = True
            self.turntable_ready = False
            self.plan_test()
            
        
        
    # 单独测试模式、通用惯导采集
    def only_test(self):
        protocal_rule = self.comboBox_protocal_rule.currentText()
        protocal_com = self.comboBox_protocal_com.currentText()
        protocal_baund = self.comboBox_protocal_baund.currentText()
        protocal_check = self.comboBox_protocal_check.currentText()
        thread_receive_list = []
        thread_decode_list = []
        self.threading_test_flag = True
        for i in range(12):
            time.sleep(0.01)
            if self.combox_com_open_list[i].text() == '开启':
                if protocal_com.lower()=='none':
                    self.show_message_dis1_list.append('tab_{}:线程开启，串口{}'.format(i+1,protocal_com))
                    continue
                self.threading_list_flag[i] = True
                thread = threading.Thread(target=self.receive_data_threading,args=(i,))
                thread.setDaemon(True)
                thread_receive_list.append(thread)
                thread.start()
    def bd_test(self):
        protocal_rule = self.comboBox_protocal_rule.currentText()
        protocal_com = self.comboBox_protocal_com.currentText()
        protocal_baund = self.comboBox_protocal_baund.currentText()
        protocal_check = self.comboBox_protocal_check.currentText()
        thread_receive_list = []
        thread_decode_list = []
        for i in range(12):
            time.sleep(0.01)
            if self.combox_com_open_list[i].text() == '开启':
                if protocal_com.lower()=='none':
                    self.show_message_dis1_list.append('tab_{}:线程开启，串口{}'.format(i+1,protocal_com))
                    continue
                self.threading_list_flag[i] = True
                thread = threading.Thread(target=self.receive_data_threading,args=(i,))
                thread.setDaemon(True)
                thread_receive_list.append(thread)
                thread.start()
        thread = threading.Thread(target=self.begin_test_bd)
        thread.setDaemon(True)
        thread.start()
    def plan_test(self):
        thread = threading.Thread(target=self.plan_test_threading)
        thread.setDaemon(True)
        thread.start()
        
        

    def receive_data_threading(self,thread_num):
        print('tab_{}:接收进程开启'.format(thread_num))
        # 串口信息载入
        com = self.combox_com_list[thread_num].currentText()
        baund = self.findChild(QtWidgets.QComboBox,'combox_set_baund_%s'%(thread_num+1)).currentText()
        check = self.findChild(QtWidgets.QComboBox,'comboBox_set_check_%s'%(thread_num+1)).currentText()
        stop = self.findChild(QtWidgets.QComboBox,'comboBox_stopbit_%s'%(thread_num+1)).currentText()
        name = self.findChild(QtWidgets.QLineEdit,'lineEdit_file_names_%s'%(thread_num+1)).text()
        checks = check2serial(check)
        stops = stop2chinese(stop)
        if self.debug_flag | self.debug_threading:
            print('thread_num:{}\tcom:{}\tbaund:{} check:{} stop:{} name:{}'.format(thread_num,com,baund,check,stop,name))
        
        # 规则信息载入
        decode_rule_list    = self.decode_rule_list     # 解算规则
        decode_save_list    = self.decode_save_list     # 是否保存
        decode_para_list    = self.decode_para_list     # 系数
        decode_titl_list    = self.decode_titl_list     # 标题
        decode_cout_list    = self.decode_cout_list     # 排序序号
        decode_sort_list    = self.decode_sort_list     # 排序后列表
        decode_edia_list    = self.decode_edia_list     # 大小端
        decode_rule_header  = self.decode_rule_header   # 帧头
        decode_rule_ender   = self.decode_rule_ender    # 帧尾
        decode_fram_leng    = self.decode_fram_leng     # 帧长
        receive_hz          = self.receive_hz           # 频率
        save_decimal_point  = self.save_decimal_point   # 精度
        save_test_title     = self.save_test_title      # 标题
        hz_count = 0
        receive_s_count = 0
        receive_hz_count = 0
        
        
        if self.debug_threading:
            print('decode_fram_leng:{}'.format(decode_fram_leng))
        # 测试信息初始化
        now = datetime.datetime.now()
        save_time = '{}{}{}'.format(now.hour,now.minute,now.second)
        file_path = './测试数据/{}{}/{}/'.format(int2str(now.year),int2str(now.month),int2str(now.day))
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        all_data = b''
        
        
        # 保存文件名
        if len(self.plan_name)>0:
            name = '{}#{}'.format(name,self.plan_name)
        hex_filename = '{}{}_{}_hex.hex'.format(file_path,name,save_time)
        hz_filename  = '{}{}_{}_hz.txt'.format(file_path,name,save_time)
        calib_filename= '{}{}_{}_hz_calib.txt'.format(file_path,name,save_time)
        s_filename   = '{}{}_{}_s.txt'.format(file_path,name,save_time)
        ave_filename = '{}{}_{}_ave.txt'.format(file_path,name,save_time)
        
        sorted_title_list = []
        for i in range(len(decode_save_list)):
            sorted_title_list+=[decode_titl_list[i][decode_sort_list[i].index(str(j))] for j in range(len(decode_titl_list[i])) if decode_save_list[i][decode_sort_list[i].index(str(j))]=='1']
        zeros_list = [0 for i in range(len(sorted_title_list))]
        receive_data_s = zeros_list
        
        # 创建标题
        if save_test_title:
            if not os.path.exists(s_filename):
                with open(s_filename,'a+') as f:
                    f.write('\t'.join(sorted_title_list)+'\n')
        # 创建串口线程
        try:
            serials = serial.Serial(com, baund, parity=checks,stopbits=stops)
        except:
            self.show_message_dis1_list.append('tab_{}:尝试开启串口失败,com:{},线程关闭'.format(thread_num,com))
            self.threading_list_flag[thread_num] = False
        while self.threading_test_flag & self.threading_list_flag[thread_num]:
            waiting = serials.in_waiting
            if waiting>=decode_fram_leng:
                cache_hex_data = serials.read(waiting)
                if self.config_save_BD_bin:
                    with open(hex_filename,'ab+') as f:
                        f.write(cache_hex_data)
                all_data += cache_hex_data
            if not self.turntable_ready:
                all_data = b''
            if len(all_data)>=decode_fram_leng*2:
                frame = all_data[:decode_fram_leng]
                next_frame = all_data[decode_fram_leng:decode_fram_leng*2]
                if frame.startswith(decode_rule_header) & next_frame.startswith(decode_rule_header): 
                    all_data = all_data[decode_fram_leng:]
                    hz_count+=1
                    receive_hz_count+=1
                    receive_data_hz = decode_hex_frame_list(frame,decode_rule_list,decode_save_list,decode_para_list,decode_sort_list,decode_edia_list)
                    # D501惯导专用保存毫秒输出到标定文件中
                    if self.config_save_ms:
                        if self.turntable_will_turn:
                            will_turn_flag = '1'
                        else:
                            will_turn_flag = '0'
                        for i in range(3):
                            receive_data_hz[i+1] = int(receive_data_hz[i+1]*1000)
                        for i in range(3):
                            receive_data_hz[i+1+3] = round(receive_data_hz[i+1+3],save_decimal_point)
                        receive_data_hz[7] = int(receive_data_hz[7]*16)
                        receive_data_hz[8] = int(receive_data_hz[8]*400)
                        
                        calib_cache_list = []
                        temp1 = receive_data_hz[7]
                        temp2 = receive_data_hz[8]
                        
                        with open(hz_filename,'a+') as f:  
                            temp_receive_data_hz = ''
                            # temp_receive_data_hz+=str(receive_data_hz[0]).ljust(10,' ')+'\t'
                            temp_receive_data_hz+=str(receive_hz_count).ljust(10,' ')+'\t'
                            for i in range(6):
                                temp_receive_data_hz+=str(receive_data_hz[i+1]).rjust(16,' ')+'\t'
                            for i in range(3):
                                temp_receive_data_hz+=str(receive_data_hz[7]).rjust(6,' ')+'\t'
                            for i in range(3):
                                temp_receive_data_hz+=str(receive_data_hz[8]).rjust(6,' ')+'\t'
                            temp_receive_data_hz+=str(0).rjust(6,' ')+'\t'
                            for i in range(2):
                                temp_receive_data_hz+=str(0).rjust(3,' ')+'\t'
                            temp_receive_data_hz+=str(0).rjust(6,' ')+'\t'
                            temp_receive_data_hz+=str(0).rjust(3,' ')+'\t'
                            for i in range(2):
                                temp_receive_data_hz+=str(0).rjust(6,' ')+'\t'
                            temp_receive_data_hz+=str(0).rjust(3,' ')
                            f.write(temp_receive_data_hz+'\n')
                            
                        with open(calib_filename,'a+') as f:
                            calib_receive_data_hz = ''
                            # calib_receive_data_hz+=str(receive_data_hz[0]).ljust(10,' ')+'\t'
                            calib_receive_data_hz+=str(receive_hz_count).ljust(10,' ')+'\t'
                            for i in range(6):
                                calib_receive_data_hz+=str(receive_data_hz[i+1]).rjust(16,' ')+'\t'
                            calib_receive_data_hz+=str(will_turn_flag).rjust(2,' ')
                            f.write(calib_receive_data_hz+'\n')
                            
                    if hz_count<receive_hz+1:
                        receive_data_s = [receive_data_s[i]+receive_data_hz[i] for i in range(len(receive_data_hz))]
                    else:
                        hz_count = 0
                        receive_s_count+=1
                        receive_data_s = [i/receive_hz for i in receive_data_s]
                        receive_data_save = '\t'.join([str(round(i,save_decimal_point)) for i in receive_data_s])
                        with open(s_filename,'a+') as f:
                            f.write(receive_data_save+'\n')
                        receive_data_s = zeros_list
                        self.show_message_list[thread_num].append(receive_data_save)
                        self.show_message_dataframe[thread_num] = pd.concat([self.show_message_dataframe[thread_num],pd.DataFrame(receive_data_s).T],axis=0)
                        
                        receive_data_s = zeros_list
                else:
                    all_data = all_data[1:]
                        
                        
                    
                    
                    
                
            else:
                time.sleep(1/self.receive_hz)
                    
    def plan_test_threading(self):
        count =0
        select_plan_name = self.comboBox_automatic_rule.currentText()
        plan_rule_name = './自动规则/{}.txt'.format(select_plan_name)
        plan_files = pd.read_csv(plan_rule_name,sep='\\s+',header=None,encoding='gb2312')
        max_plan = len(plan_files)-1
        wait_count = 0
        real_time = time.time()
        begin_time = time.time()
        while self.plan_threading_flag:
            list_plan = list(plan_files.iloc[count])
            # print(list_plan)
            if list_plan[0].startswith('#'):
                count+=1
            elif list_plan[1]=='wait':
                # print('等待时间:{:.2f}'.format(time.time()-real_time))
                if time.time()-begin_time>int(list_plan[2]):
                    count+=1
                    begin_time = time.time()
                else:
                    self.automatic_time = int(list_plan[2])-(time.time()-begin_time)
                    time.sleep(1)
                    wait_count+=1
            elif list_plan[1]=='power':
                count+=1
                print('电源时间:{:.2f}'.format(time.time()-real_time))
                if list_plan[2]=='on':
                    serial_com = self.comboBox_com_sate.currentText()
                    serials = serial.Serial(serial_com, 57600)
                    serials.write(':OUTP 1\n'.encode())
                    serials.close()
                elif list_plan[2]=='off':
                    self.plan_name = ''
                    serial_com = self.comboBox_com_sate.currentText()
                    serials = serial.Serial(serial_com, 57600)
                    serials.write(':OUTP 0\n'.encode())
                    serials.close()
                else:
                    print('未知电源命令')
                begin_time = time.time()
            elif list_plan[1]=='test':
                count+=1
                self.plan_name = str(list_plan[2])
                begin_time = time.time()
            elif list_plan[1]=='bd':
                count+=1
                if list_plan[2]=='on':
                    begin_time = time.time()
                    self.threading_test_flag = False
                    time.sleep(0.1)
                    self.threading_test_flag = True
                    time.sleep(0.1)
                    self.turntable_ready = False
                    self.bd_test()
                else:
                    begin_time = time.time()     
            else:
                print('未知控制命令:{}，跳过'.format(list_plan))
                count+=1
               
    def begin_test_bd(self):
        inside_location = 0
        outside_location = 0
        inside_speed = 20
        outside_speed = 20
        inside_acceleration = 20
        outside_acceleration = 20
        
        waittime = 2
        rule_count =0
        send_check=True
        self.serial_test_begin_flag = False
        self.serial_receive_flag=True
        begin_time = time.time()
        bd_begin_time = begin_time
        bd_rulename = './{}/{}.txt'.format('标定规则',self.comboBox_turntable_rule.currentText())
        rule_file = pd.read_csv(bd_rulename,header=None,skiprows=2,encoding='gb2312',sep='\\s+')
        com_port = self.comboBox_turntable_com.currentText()
        turntable_serial = serial.Serial(com_port, 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        turntable = Turntable_class()
        while (rule_count<len(rule_file)) & self.plan_threading_flag:
            time.sleep(0.5)
            i=rule_count
            if send_check:
                send_check=False
                inside_location=int(rule_file[1][i])
                outside_location=int(rule_file[2][i])
                inside_speed=int(rule_file[3][i])
                outside_speed=int(rule_file[4][i])
                test_time = int(rule_file[5][i])
                mode = 'None'
                if (rule_file[3][i]==0)&(rule_file[4][i]==0):
                    # 转台固定 方位模式
                    turntable.inside_location(inside_location,inside_speed,inside_acceleration)
                    turntable.outside_location(outside_location,outside_speed,outside_acceleration)
                else:
                    # 内外旋转
                    print('**********错误的转台位置设定**************')
                    
                message = turntable.get_command()
                turntable_serial.write(bytes.fromhex(message))

                waittime = (int(rule_file[5][i])+15+1)
                
            if (time.time()-begin_time>10)& (not self.serial_test_begin_flag):
                self.serial_test_begin_flag = True
                self.turntable_ready = True
                print('开始陀螺数据接收')
                self.turntable_will_turn = False
            if time.time()-begin_time>waittime+8:
                self.turntable_will_turn = True
            if time.time()-begin_time>waittime+10:
                print('一组测试结束')
                self.serial_test_begin_flag = False
                send_check = True
                rule_count+=1

                message = 'aaaa555538000100800000000000000000000000008000000000000000000000000000000000000000000000000000ff000000ffffffff34'
                turntable_serial.write(bytes.fromhex(message))
                time.sleep(1)
                begin_time = time.time()
        # 转台停止 标定结束 
        self.threading_test_flag = False
         


# 根据规则解算数据 - 旧
def decode_hex_frame(frame,rules_format,rules_head,rules_saveck,rules_paras):
    bit_data = []
    for i in range(len(rules_format)):
        if str(rules_saveck[i])=='1':
            bit_frame_length = struct.calcsize(rules_head[i]+rules_format[i])
            before_frame_length = struct.calcsize('>'+''.join(rules_format[:i]))
            frame_data = frame[before_frame_length:before_frame_length+bit_frame_length]
            if str(rules_paras[i])=='1':
                decode_frame_data = struct.unpack(rules_head[i]+rules_format[i],frame_data)[0]
            else:
                decode_frame_data = struct.unpack(rules_head[i]+rules_format[i],frame_data)[0] *float(rules_paras[i])
                
            bit_data.append(decode_frame_data)
        else:
            continue
    return bit_data

def try_set_text(obj,types,default=1):
    try: return types(obj)
    except: return types(default)
def try_get_text(obj,types,default=1):
    try: return types(obj.text())
    except: return types(default)
def int2str(string,rjust=2,strjust='0'):
    return str(string).rjust(rjust,strjust)
def hex2int(strings):
    return int(strings,16) if bin(int(strings,16))[2:].rjust(len(strings)*4,'0')[0]=='0' else int(strings,16)-int(len(strings)*'F',16)-1
def int2hex(string,rjust=2):
    return hex(string)[2:].rjust(rjust,'0')[-rjust:].upper() if int(string)>0 else int2hex(int('F'*rjust,16)+int(string)+1,rjust)
def reverse(string):
    return ''.join([string[len(string)-i*2-2:len(string)-i*2] for i in range(len(string)//2)])
def hexcut2list(string):
    return [string[i*2:i*2+2] for i in range(len(string)//2)]
def struct_unpack_int3(string):
    return int(struct.unpack('<i',b'\x00'+string)[0]/256)
# 校验位中规则转换
def check2serial(data):
    import serial
    try: return [serial.PARITY_NONE,serial.PARITY_EVEN,serial.PARITY_ODD][['无校验','偶校验','奇校验'].index(str(data).lower())]
    except: return serial.PARITY_NONE
# 停止位中规则
def stop2chinese(data):
    import serial
    try: return [serial.STOPBITS_ONE,serial.STOPBITS_TWO][['stop1','stop2'].index(str(data).lower())]
    except: return serial.STOPBITS_ONE
# 校验位中英转换
def check2chinese(data):
    try: return ['无校验','偶校验','奇校验'][['none','even','odd'].index(str(data).lower())]
    except: return '无校验'
def chinese2check(data):
    try: return [serial.PARITY_NONE,serial.PARITY_EVEN,serial.PARITY_ODD][['无校验','偶校验','奇校验'].index(str(data).lower())]
    except: return serial.PARITY_NONE
# 规则文件中英转换
def rulename2chinese(data):
    try: return ['解算规则','标定规则','装订规则','自动规则'][['protocal','turntable','binding','automatic'].index(str(data).lower())]
    except: return '错误名称'
# 测试模式中英转换
def testmode2chinese(data):
    try: return ['惯导测试','转台标定','自动测试'][['only_test','turntable_test','automatic_test'].index(str(data).lower())]
    except: return '错误名称'
# 计算协议长度
def calculate_frame_length(rules_format_list):
    before_frame_length = 0
    for rules_format in rules_format_list:
        for i in rules_format:
            if (i.lower()=='y'):
                before_frame_length += 3
            else:
                before_frame_length += struct.calcsize('>'+i)
    return before_frame_length
def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum += byte
    return checksum & 0xFF 
# 按规则列表转换十六进制原始数
def decode_hex_frame_list(frame,decode_rule_list,decode_save_list,decode_para_list,decode_sort_list,decode_edia_list):
    decode_data_list = []
    decode_struct_tolegth = 0
    for i in range(len(decode_edia_list)):
        decode_bit_list = []
        decode_struct = decode_edia_list[i]+''.join(decode_rule_list[i])
        decode_struct_length =struct.calcsize(decode_struct)
        decode_tuple = list(struct.unpack(decode_struct,frame[decode_struct_tolegth:decode_struct_length]))
        decode_struct_tolegth += decode_struct_length
        for j in range(len(decode_tuple)):
            try:
                decode_sort_num = decode_sort_list[i].index(str(j))
            except:
                print('decode_hex_frame_list:排序序号超出列表长度')
                continue
            if decode_save_list[i][decode_sort_num]=='1':
                decode_para_num = decode_para_list[i][decode_sort_num]
                if decode_para_num=='1':
                    decode_bit_list.append(decode_tuple[decode_sort_num])
                else:
                    decode_bit_list.append(decode_tuple[decode_sort_num]*float(decode_para_num))
        decode_data_list+=decode_bit_list
    return decode_data_list
            

class Turntable_class:
    def __init__(self):
        # 转台通讯协议数据帧格式
        self.header='AAAA5555'
        self.command_length = '3800'
        self.command_count = '0100'
        self.inside_command='80'
        self.inside_para1 = '00000000'
        self.inside_para2 = '00000000'
        self.inside_para3 = '00000000'
        self.outside_command='00'
        self.outside_para1 = '00000000'
        self.outside_para2 = '00000000'
        self.outside_para3 = '00000000'
        self.otherside_command='00'
        self.otherside_para1 = '00000000'
        self.otherside_para2 = '00000000'
        self.otherside_para3 = '00000000'
        self.thermostat_command = 'FF'
        self.thermostat_speed = '00'
        self.thermostat_target= '0000'
        self.spare_command = 'FFFFFFFF'
        self.check_command = '00'
        self.all_hex = ''
        self.split_hex = ''
    # 组合各数据帧 计算校验并返回总指令
    def get_command(self):
        all_hex = ''.join([self.command_length,self.command_count,self.inside_command,self.inside_para1,self.inside_para2,self.inside_para3,self.outside_command,self.outside_para1,self.outside_para2,self.outside_para3,self.otherside_command,self.otherside_para1,self.otherside_para2,self.otherside_para3,self.thermostat_command,self.thermostat_speed,self.thermostat_target,self.spare_command])
        # self.command_count = int2hex(int(reverse(self.command_count),16)+1,4)
        # print(self.command_count)
        split_hex = ''
        check = 0
        for i in range(len(all_hex)//2):
            bit = all_hex[i*2:i*2+2]
            split_hex+=bit+' '
            check+=int(bit,16)
        check = int2hex(check)
        all_hex += check
        split_hex += check
        self.check_command = check
        self.all_hex = self.header+all_hex
        self.split_hex = 'AA AA 55 55 '+split_hex
        return self.all_hex
    # 内框置零
    def reset_inside(self):
        self.inside_command='00'
        self.inside_para1 = '00000000'
        self.inside_para2 = '00000000'
        self.inside_para3 = '00000000'
        return self.get_command()
    # 外框置零
    def reset_outside(self):
        self.outside_command='00'
        self.outside_para1 = '00000000'
        self.outside_para2 = '00000000'
        self.outside_para3 = '00000000'
        return self.get_command()
    # 内框归零
    def reset_inside(self):
        self.inside_command = '81'
        self.inside_para1 = reverse(int2hex(0*10000,8))
        self.inside_para2 = reverse(int2hex(10*10000,8))
        self.inside_para3 = reverse(int2hex(10*100,8))
        return self.get_command()
    # 外框归零
    def reset_outside(self):
        self.outside_command = '81'
        self.outside_para1 = reverse(int2hex(0*10000,8))
        self.outside_para2 = reverse(int2hex(10*10000,8))
        self.outside_para3 = reverse(int2hex(10*100,8))
        return self.get_command()
    # 内框设置位置
    def inside_location(self,location=0,speed=10,acceleration=10):
        self.inside_command = '81'
        self.inside_para1 = reverse(int2hex(int(location*10000),8))
        self.inside_para2 = reverse(int2hex(int(speed*10000),8))
        self.inside_para3 = reverse(int2hex(int(acceleration*100),8))
        return self.get_command()
    # 内框设置速率
    def inside_speed(self,speed=10,acceleration=10):
        self.inside_command = '82'
        self.inside_para1 = reverse(int2hex(int(speed*10000),8))
        self.inside_para2 = reverse(int2hex(int(acceleration*100),8))
        self.inside_para3 = '00000000'
        return self.get_command()
    # 外框设置位置

    def outside_location(self,location=0,speed=10,acceleration=10):
        self.outside_command = '81'
        self.outside_para1 = reverse(int2hex(int(location*10000),8))
        self.outside_para2 = reverse(int2hex(int(speed*10000),8))
        self.outside_para3 = reverse(int2hex(int(acceleration*100),8))
        return self.get_command()
    # 外框设置速率
    def outside_speed(self,speed=10,acceleration=10):
        self.outside_command = '82'
        self.outside_para1 = reverse(int2hex(int(speed*10000),8))
        self.outside_para2 = reverse(int2hex(int(acceleration*100),8))
        self.outside_para3 = '00000000'
        return self.get_command()
        
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
