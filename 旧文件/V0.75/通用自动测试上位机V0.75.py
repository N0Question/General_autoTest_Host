from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from Automated_testingV13 import Ui_MainWindow
from pyqtgraph.Qt import QtCore
from fun_chy2 import *
import binascii
import datetime
from datetime import timezone,datetime,timedelta
import os
import serial
# import pyqtgraph.opengl as gl
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

debug_test = 1

update_log = '''
V0.66   较为稳定版本，开始记录细节更新及待更新内容
V0.67   载入功能实现 
V0.68   惯导测试    加入经纬度转换、距离、速度，实时绘图及误差计算
V0.69   转台控制	反应转台状况,状态字显示
V0.71	转台控制	根据转台状态决定是否收数及刹车是否到位
V0.72	惯导协议	加入"drop0datav [num]"，由num判断是否丢弃对应包中为0的数据
V0.73	数据处理	解算数据时判断校验并根据配置决定是否保存
'''
updating_log = '''
转台控制    模块化控制 根据状态字决定是否下一步
数据处理    加入数据处理自动出测试报告

'''

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("通用自动测试上位机_蔡_功能测试版_2411_V0.73")
        self.show_message_length = 30   # 显示的最大行数
        
        # 初始化界面元素
        self.inside_location = 0.0
        self.inside_speed = 0.0
        self.outside_location = 0.0
        self.outside_speed = 0.0
        self.turntable_i_status = '{}'.format('N')    # 转台运动状态
        self.turntable_o_status = '{}'.format('N')     # 转台运动状态
        self.automatic_time = 0          # 自动测试时间  
        self.power_flag = False
        self.plan_name = ''             # 自动标定进度名称
        self.threading_begin_time = 0
        self.default_alpha = 0.6
        self.all_rec_hex = 0
        self.sum_check_err_count = 0
        
        # 初始化绘图元素
        self.graphicsView_gyr_X_adp = self.graphicsView_gyr_X.addPlot()
        self.graphicsView_gyr_Y_adp = self.graphicsView_gyr_Y.addPlot()
        self.graphicsView_gyr_Z_adp = self.graphicsView_gyr_Z.addPlot()
        self.graphicsView_gyr_X_adp.showGrid(x=True,y=True,alpha=self.default_alpha)
        self.graphicsView_gyr_Y_adp.showGrid(x=True,y=True,alpha=self.default_alpha)
        self.graphicsView_gyr_Z_adp.showGrid(x=True,y=True,alpha=self.default_alpha)

        self.gv_pen_x = self.graphicsView_gyr_X_adp.plot(pen='y')
        self.gv_pen_y = self.graphicsView_gyr_Y_adp.plot(pen='y')
        self.gv_pen_z = self.graphicsView_gyr_Z_adp.plot(pen='y')
        self.list_gv_pen = [self.gv_pen_x,self.gv_pen_y,self.gv_pen_z]
        self.list_gv_adp = [self.graphicsView_gyr_X_adp,self.graphicsView_gyr_Y_adp,self.graphicsView_gyr_Z_adp]
        self.list_mean_data = [self.lineEdit_inside_plot_mean1,self.lineEdit_inside_plot_mean2,self.lineEdit_inside_plot_mean3]
        self.list_std_data = [self.lineEdit_inside_plot_stds1,self.lineEdit_inside_plot_stds2,self.lineEdit_inside_plot_stds3]
        
        self.graphicsView_INU_loc_adp = self.graphicsView_INU_loc.addPlot()
        self.graphicsView_INU_loc_error_adp = self.graphicsView_INU_loc_error.addPlot()
        self.graphicsView_INU_speed_adp = self.graphicsView_INU_speed.addPlot()
        self.graphicsView_INU_loc_adp.showGrid(x=True,y=True,alpha=1.0)
        self.graphicsView_INU_loc_error_adp.showGrid(x=True,y=True,alpha=self.default_alpha)
        self.graphicsView_INU_speed_adp.showGrid(x=True,y=True,alpha=self.default_alpha)

        self.scatter = pg.ScatterPlotItem()
        self.graphicsView_INU_loc_adp.addItem(self.scatter)
        self.scatter.setData([1,2,3],[5,6,7])
        self.gv_pen_loc_error = self.graphicsView_INU_loc_error_adp.plot(pen='y')
        self.gv_pen_speed = self.graphicsView_INU_speed_adp.plot(pen='y')


        # 初始化使用元素
        self.short_time = '000000'
        self.normal_time = '00:00:00'
        self.long_time = '00000000_000000'
        self.bd_test_flag = ''
        self.default_longitude = 116.50271
        self.default_latitude = 39.73155
        self.default_g = 9.801538877
        self.show_message_automatic_list = []
        self.show_message_automatic_list_2 = []
        self.show_message_singletest = None
        self.lineEdit_automatic_mode_list = []
        self.show_message_dis1_list = []
        self.show_message_dis2_list = []
        self.show_message_list = []             # 12输出显示
        for i in range(12):
            self.show_message_list.append([])
        self.show_message_dataframe = []        # 12路绘图显示
        for i in range(12):
            self.show_message_dataframe.append(pd.DataFrame([]))
        self.show_message_dataframe_cache = []        # 12路绘图显示
        for i in range(12):
            self.show_message_dataframe_cache.append([])
        self.tableWidget_table_show.setRowCount(40)
        self.tableWidget_table_show.setColumnCount(10)
        
        
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
        
        # 初始化定时线程相关标志位
        self.auto_plot_always   = False # 始终更新绘图，用于实时解算
        self.auto_plot_1time    = False # 仅更新一次绘图，用于打开文件查看时
        self.show_message_clear = False # 清空显示

        # 初始化INU绘图相关标志位
        self.inu_plot_always = False
        self.inu_plot_once = False
        self.inu_plot_clear = False


        # 初始化标定进度相关标志位
        self.bd_count = 0               # 标定进度计数
        self.bd_calib_flag = 0          # 标定转台转动标志位，用于惯导一室通用标定
        self.serial_test_begin_flag = False     # 转台到位标志位
        self.bd_plan_flag = False       # 标定结束标志位
        
        
        
        
        # debug调试状态
        self.debug_flag = False
        self.debug_read_rules = False
        self.bebug_binding = False
        self.debug_begin_test = False
        self.debug_threading = False
        self.debug_update_5s = False
        self.debug_update_5s_file = False
        self.debug_update_1s = False
        self.debug_list_1 = []
        self.debug_list_2 = []
        self.debug_list_3 = []
        self.debug_list_4 = []
        self.lineEdit_debug_QlineEdit_list = []
        self.lineEdit_debug_message_list = []
        for i in range(8):
            self.lineEdit_debug_QlineEdit_list.append(self.findChild(QtWidgets.QLineEdit, 'lineEdit_debug_{}'.format(i+1)))
            self.lineEdit_debug_message_list.append([])
        
        
        # 初始化解算规则列表-新
        self.decode_rule_list = []    # 解算规则
        self.decode_save_list = []    # 是否保存
        self.decode_para_list = []    # 系数
        self.decode_titl_list = []    # 标题
        self.decode_cout_list = []    # 排序序号
        self.decode_sort_list = []    # 排序后列表
        self.decode_edia_list = []    # 大小端
        self.sorted_titl_list = []    # 排序后保存标题
        self.receive_hz = 200
        self.receive_wait_time = 0.005
        self.config_sum_check = None        # 累加校验和位置及其累加位置 格式： [校验和位置,累加起始:累加结束]
        self.drop0data = []             # 惯导通用协议中，在秒值处理中丢弃对应数据中为0的数
        # 初始化结算规则-方法类实现
        self.decode_class = class_rule()
        
        
        # 配置文件路径
        self.para_com_filename = './配置文件/para_com.txt'
        self.para_config_filename = './配置文件/para_config.txt'
        self.model_list = [
            ['通讯','转台','电源','温箱','装订','自动'],
            ['protocal','turntable','power','tempbox','binding','automatic'],
            ['解算规则','标定规则','none','none','装订规则','自动规则']
        ]
        
        # 配置文件默认设置
        self.config_hold_time = 15          # 转台稳定后等待时间
        self.config_save_alldata_ms = 0     # 是否保存所哟毫秒值 
        self.config_save_alldata_s = 0      # 是否保存所有秒值 
        self.config_save_alldata_calib = 0	# 是否保存calib毫秒值 
        self.config_save_readydata_ms = 0	# 是否保存到位毫秒值 
        self.config_save_readydata_s = 0	# 是否保存到位秒值 
        self.config_save_BD_average = 1     # 是否将标定过程各点取均值存放
        self.config_save_alldata_bin = 1         # 是否保存标定过程中16进制原始数
        self.config_save_BD_1file = 1       # 将标定过程各点存储到一个文件/多个文件
        self.save_decimal_point = 6         # 保存时保留小数点后几位
        self.save_test_title = 1            # 创建文件时将协议中的标题内容一并保存
        self.config_power_model = 1         # 电源型号：1程控电源，2继电器
        self.config_special_flag = None     # 特殊标志位
        self.config_decode_header_type = 1  # 0:使用帧头模式/1:使用2帧头中间模式/2:使用帧头帧尾模式
        self.config_turntable_check_status = 0      # 1:根据转台状态反馈来决定是否到位/0:转动命令发送后固定等待hold_time
        self.config_table_row = 40
        self.config_table_col = 10
        self.config_table_round = 6
        self.config_in_spd = 36
        self.config_in_acc = 36
        self.config_out_spd = 24
        self.config_out_acc = 24
        self.default_plot_enable = 1
        self.default_plot_limit = 100000
        self.default_plot_flag = True       # 允许检测文件长度判断是否切换刷新时间
        self.default_plot_time = 1500
        self.default_plot_load = 1200
        self.default_sumcheck_flag = 0

        
        # 解算规则配置
        self.rules_lists_format = 'xcbB?hHiIlLqQfdspPtyY'   # 解算规则可用范围
        
        # 总控-刷新comboBox串口
        self.comboBox_update_com_flag = True
        self.comboBox_update_rules_flag = True
        self.comboBox_update_para_flag = True


        # 全部设置区com口列表
        self.comboBox_com_list = [self.comboBox_protocal_com, 
                                self.comboBox_turntable_com, 
                                self.comboBox_power_com,
                                self.comboBox_tempbox_com,
                                self.combox_set_com_all]
        # 12路com口
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
        # 12路开关按键
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
        self.textBrowser_list = []
        for i in range(12):
            self.textBrowser_list.append( self.findChild(QtWidgets.QTextBrowser,'textBrowser_%s'%(i+1)) )

        # 12路装订缓存区
        self.binding_cache_list = []
        for i in range(12):
            self.binding_cache_list.append([])
        self.ascii_cache_list = []
        for i in range(12):
            self.ascii_cache_list.append([])
        # 装订自动更新
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
        # 多路选择combobox 
        combobox_lists = [
            self.comboBox_plot_choiceTab,
            self.comboBox_INU_choiceTab_stand,
            self.comboBox_INU_choiceTab_target
        ]
        for item in combobox_lists:
            item.clear()
            for i in range(12):
                item.addItem('{} {}'.format(i+1,'路'))
            item.setCurrentIndex(0)
        # for i in range(12):
        #     self.comboBox_plot_choiceTab.addItem('{} {}'.format(i+1,'路'))
        # self.comboBox_plot_choiceTab.setCurrentIndex(1)
        # 默认装订选择设置
        self.comboBox_binding_com.clear()
        self.comboBox_binding_com.addItem('all')
        for i in range(12):
            self.comboBox_binding_com.addItem('{} tab'.format(i+1))
        self.comboBox_binding_com.setCurrentIndex(1)
        # 60所装订选择设置
        self.comboBox_binding_com_60s.clear()
        self.comboBox_binding_com_60s.addItem('all')
        for i in range(12):
            self.comboBox_binding_com_60s.addItem('{} tab'.format(i+1))
        self.comboBox_binding_com_60s.setCurrentIndex(1)
        # 激光惯导#60所 自动装订构造
        self.binding_list_60s = []
        for i in range(10):
            self.binding_list_60s.append( self.findChild(QtWidgets.QLineEdit,'lineEdit_binding_60s_%s'%(i+1)) )
        for binding in self.binding_list_60s:
            binding.textChanged.connect(self.event_update_bingding_60s)


        # 卫导板卡 自动装订构造
        self.sate_com_list = []
        for i in range(3):
            self.sate_com_list.append(self.findChild(QtWidgets.QComboBox,'comboBox_sate_com_%s'%(i+1)) )
        for sate_com in self.sate_com_list:
            sate_com.clear()
            sate_com.addItem('all')
            for i in range(12):
                sate_com.addItem('{} tab'.format(i+1))
            sate_com.setCurrentIndex(1)
        # 卫导板卡 点击事件构建
        self.pushButton_sate_send_1.clicked.connect(self.event_send_sate1)
        self.pushButton_sate_send_2.clicked.connect(self.event_send_sate2)
        self.pushButton_sate_send_3.clicked.connect(self.event_send_sate3)
        # 卫导板卡 更新内容构建
        self.sate_send1_line_list = []  
        self.sate_send2_line_list = []
        self.sate_send1_autotime = 1000
        self.sate_send2_autotime = 1000
        # self.sate_send1_line_list.append(self.comboBox_sate_1_1.currentText())
        # self.sate_send2_line_list.append(self.comboBox_sate_2_1.currentText())
        for i in range(10):
            self.sate_send1_line_list.append( self.findChild(QtWidgets.QLineEdit,'lineEdit_sate_1_%s'%(i+1)) )
        for i in range(9):
            self.sate_send2_line_list.append( self.findChild(QtWidgets.QLineEdit,'lineEdit_sate_2_%s'%(i+1)) )
        self.lineEdit_sate_1_0.textChanged.connect(self.sate_send1_change_time)
        self.lineEdit_sate_2_0.textChanged.connect(self.sate_send2_change_time)
        for sate_line in self.sate_send1_line_list:
            sate_line.textChanged.connect(self.event_update_sate1)
        for sate_line in self.sate_send2_line_list:
            sate_line.textChanged.connect(self.event_update_sate2)
        self.event_update_sate1()
        self.event_update_sate2()





        

        



        # 选择事件集
        # 总控开关切换
        self.pushButton_com_open_all.clicked.connect(self.change_button_all)
        # 单路通讯协议同步多路更新
        self.comboBox_protocal_com.currentTextChanged.connect(self.protocal_com_change)
        self.comboBox_protocal_baund.currentTextChanged.connect(self.protocal_com_change)
        self.comboBox_protocal_check.currentTextChanged.connect(self.protocal_com_change)
        self.combox_set_com_1.currentTextChanged.connect(self.comboBox_com_change)
        self.combox_set_baund_1.currentTextChanged.connect(self.comboBox_com_change)
        self.comboBox_set_check_1.currentTextChanged.connect(self.comboBox_com_change)
        # 绘图逻辑更新-绘制轴向及标题更新 20241012
        self.comboBox_plot_beginAxis.currentTextChanged.connect(self.update_plot_axis)
        self.comboBox_INU_beginAxis_stand.currentTextChanged.connect(self.update_stand_axis)
        self.comboBox_INU_beginAxis_loc.currentTextChanged.connect(self.update_target_loc)
        self.comboBox_INU_beginAxis_spd.currentTextChanged.connect(self.update_target_spd)
        # 多路文件名同步更新
        self.lineEdit_file_names_all.textChanged.connect(self.filenames_change)
        # 规则更新同步
        self.comboBox_protocal_rule.currentTextChanged.connect(self.read_rules)


        # 点击事件集
        self.pushButton_begin_test.clicked.connect(self.begin_test)
        self.pushButton_stop_test.clicked.connect(self.stop_test)
        self.pushButton_begin_test_2.clicked.connect(self.begin_test)
        self.pushButton_stop_test_2.clicked.connect(self.stop_test)
        # 发送装订
        self.pushButton_binding_send.clicked.connect(self.binding_send)
        # 载入文件
        self.pushButton_load_data.clicked.connect(self.event_load_file)
        self.pushButton_load_data_2.clicked.connect(self.event_load_file)
        # 自动获取经纬度
        self.pushButton_autoset_INU.clicked.connect(self.event_autoset_inu)
        # 重新载入para_config文件
        self.pushButton_debug_1.clicked.connect(self.event_reload_config)
        # 激光惯导#60所祥光装订
        # self.pushButton_update_binding_60s.clicked.connect(self.event_update_bingding_60s)
        self.pushButton_binding_send_60s.clicked.connect(self.event_send_bingding_60s)
        # 开关电源
        self.pushButton_power_open.clicked.connect(self.event_power_on)
        self.pushButton_power_close.clicked.connect(self.event_power_off)
        
        self.lineEdit_inside_plot_axis_list = []
        self.lineEdit_inside_plot_para_list = []
        self.init_all_coef()

        
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
        self.show_timer0.start(200)
        # 事件0.5s更新
        self.show_timer1 = QTimer(self)
        self.show_timer1.timeout.connect(self.show_message_05s)
        self.show_timer1.start(500)
        # 事件1s更新
        self.show_timer2 = QTimer(self)
        self.show_timer2.timeout.connect(self.show_message_1s)
        self.show_timer2.start(1000)
        # 事件5s更新
        self.show_timer3 = QTimer(self)
        self.show_timer3.timeout.connect(self.show_message_5s)
        self.show_timer3.start(5000)
        # 事件2s更新
        self.show_timer4 = QTimer(self)
        self.show_timer4.timeout.connect(self.show_message_2s)
        self.show_timer4.start(2000)

        # 卫导定时发送
        self.sate_time1 = QTimer(self)
        self.sate_time1.timeout.connect(self.event_send_sate1)
        self.sate_time1.start(self.sate_send1_autotime)
        # 事件2s更新
        self.sate_time2 = QTimer(self)
        self.sate_time2.timeout.connect(self.event_send_sate2)
        self.sate_time2.start(self.sate_send2_autotime)

        self.init_all_coef_end()

    def init_all_coef_end(self):
        self.lineEdit_INU_plot_stand_lon.setText(str(self.default_longitude))
        self.lineEdit_INU_plot_stand_lat.setText(str(self.default_latitude))
        self.lineEdit_binding_60s_2.setText(str(self.default_longitude))
        self.lineEdit_binding_60s_3.setText(str(self.default_latitude))
        self.lineEdit_sate_1_3.setText(str(self.default_longitude))
        self.lineEdit_sate_1_2.setText(str(self.default_latitude))
        self.tableWidget_table_show.setRowCount(self.config_table_row)
        self.tableWidget_table_show.setColumnCount(self.config_table_col*2)


    def init_all_coef(self):
        self.lineEdit_inside_plot_axis_list = []
        self.lineEdit_inside_plot_para_list = []
        for i in range(3):
            self.lineEdit_inside_plot_axis_list.append(
                self.findChild(QtWidgets.QLineEdit, 'lineEdit_inside_plot_axis{}'.format(i+1))
            )
            self.lineEdit_inside_plot_para_list.append(
                self.findChild(QtWidgets.QLineEdit, 'lineEdit_inside_plot_para{}'.format(i+1))
            )

    
    # 事件更新0.1s线程，用于更新数据输出和绘图
    def show_message_01s(self):
        if self.show_message_clear:
            for i in range(12):
                # textBrowsers = self.findChild(QtWidgets.QTextBrowser,'textBrowser_%s'%(i+1))
                self.textBrowser_list[i].clear()
            self.show_message_clear = False
        if len(self.show_message_dis1_list)>0:
            self.textBrowser_progress_display1.append(self.show_message_dis1_list.pop(0))
            self.textBrowser_progress_display1.verticalScrollBar().setValue(self.textBrowser_progress_display1.verticalScrollBar().maximum())

        if len(self.show_message_dis2_list)>0:
            self.textBrowser_progress_display2.append(self.show_message_dis2_list.pop(0))
            self.textBrowser_progress_display2.verticalScrollBar().setValue(self.textBrowser_progress_display1.verticalScrollBar().maximum())
        
        if len(self.show_message_automatic_list)>0:
            self.textBrowser_automatic_ruleline.append(self.show_message_automatic_list.pop(0))
            self.textBrowser_automatic_ruleline.verticalScrollBar().setValue(self.textBrowser_automatic_ruleline.verticalScrollBar().maximum())
        
        if len(self.show_message_automatic_list_2)>0:
            self.textBrowser_automatic_ruleline_2.append(self.show_message_automatic_list_2.pop(0))
            self.textBrowser_automatic_ruleline_2.verticalScrollBar().setValue(self.textBrowser_automatic_ruleline_2.verticalScrollBar().maximum())
        for i in range(12):
            while len(self.show_message_list[i])>0:
                # textBrowsers = self.findChild(QtWidgets.QTextBrowser,'textBrowser_%s'%(i+1))
                # textBrowsers.append(self.show_message_list[i].pop(0))
                # textBrowsers.verticalScrollBar().setValue(textBrowsers.verticalScrollBar().maximum())
                self.textBrowser_list[i].append( self.show_message_list[i].pop(0) )

                

            
            
    # 事件更新0.5s线程，用于更新数据输出和绘图
    def show_message_05s(self):
        while len(self.lineEdit_automatic_mode_list)>0:
            automatic_show_text = str(self.lineEdit_automatic_mode_list.pop(0))
            self.lineEdit_automatic_mode.setText(automatic_show_text)
            self.lineEdit_automatic_mode_2.setText(automatic_show_text)
        self.show_timer_count1 += 1
        begin_time = time.time()
        for thread_num in range(12):
            while len(self.show_message_dataframe_cache[thread_num])>0:
                add_item = self.show_message_dataframe_cache[thread_num].pop(0)
                self.show_message_dataframe[thread_num] = pd.concat([self.show_message_dataframe[thread_num],pd.DataFrame(add_item).T],axis=0)

    # 事件更新1s线程，用于按秒更新界面元素
    def show_message_1s(self):
        begin_time_1s = time.time()
        self.show_timer_count2 += 1
        try:
            self.lcdNumber_inside_location.display('{:.2f}'.format(self.inside_location))
            self.lcdNumber_inside_speed.display('{:.2f}'.format(self.inside_speed))
            self.lcdNumber_outside_location.display('{:.2f}'.format(self.outside_location))
            self.lcdNumber_outside_speed.display('{:.2f}'.format(self.outside_speed))
            self.lineEdit_turntable_i_status.setText(self.turntable_i_status)
            self.lineEdit_turntable_o_status.setText(self.turntable_o_status)
            self.lcdNumber_automatic_time.display(int(self.automatic_time))
            self.lcdNumber_automatic_time_2.display(int(self.automatic_time))
            self.radioButton_power_flag.setChecked(self.power_flag)
        except Exception as e:
            self.debug_list_3.append('{} UI内容设置错误:{} {}'.format(self.normal_time,'0.5s',e))
        # 转换时分秒
        self.test_time = datetime.now().strftime('%H%M%S')
        self.normal_time = datetime.now().strftime('%H:%M:%S')
        self.long_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        # point_lcd_time = time.time()

        # 绘图 # 若有绘图更新标志auto_plot_always
        if (self.auto_plot_always | self.auto_plot_1time) & self.default_plot_enable:
            # print('self.auto_plot_always{}  {}'.format(self.auto_plot_always,self.auto_plot_1time))
            self.auto_plot_1time = False
            try:
                plot_data_tab = int(self.comboBox_plot_choiceTab.currentText().split()[0])-1
            except:
                plot_data_tab = 0
            # 更新绘图相关设置
            # 获取绘图参数
            list_axis = []
            list_title = []
            list_para = []
            for i in range(3):
                plot_axis_text = self.lineEdit_inside_plot_axis_list[i].text()
                try:plot_axis = int(plot_axis_text.split()[0])
                except:plot_axis = 1
                try:plot_title = str(plot_axis_text.split()[1])
                except:plot_title = 'None'
                plot_para_text = self.lineEdit_inside_plot_para_list[i].text()
                try:plot_para = float(plot_para_text)
                except:
                    plot_para = 1
                list_axis.append(plot_axis)
                list_title.append(plot_title)
                list_para.append(plot_para)

            try:plot_tab = int(self.comboBox_plot_choiceTab.currentText().split()[0])
            except:plot_tab = 1
            skip_count = try_get_text(self.lineEdit_plot_skipcount,int,1)
            end_count = try_get_text(self.lineEdit_plot_endcoun,int,0)
            rolls = try_get_text(self.lineEdit_plot_rolling,int,1)
            plot_dataframe = self.show_message_dataframe[plot_tab-1]
            if self.default_plot_flag:
                if len(plot_dataframe)>self.default_plot_limit:
                    self.show_timer2.start(self.default_plot_time)
                    self.default_plot_flag = False
            
            for i in range(3):
                if len(plot_dataframe)==0:
                    continue
                try:
                    if end_count==0:
                        plot_data = list_para[i]*plot_dataframe.iloc[skip_count:,list_axis[i]].reset_index(drop=True).rolling(rolls).mean()
                    else:    
                        plot_data = list_para[i]*plot_dataframe.iloc[skip_count:-end_count,list_axis[i]].reset_index(drop=True).rolling(rolls).mean()
                    self.list_gv_pen[i].setData(plot_data)
                    try:
                        self.list_gv_adp[i].setTitle(list_title[i])
                    except Exception as e:
                        self.debug_list_1.append('{}设置绘图标题错误:{}'.format(self.normal_time,e))
                    mean_data = plot_data.mean()
                    self.list_mean_data[i].setText('{:.4f}'.format(mean_data))
                    stds_data = float(plot_data.std())
                    # print(stds_data)
                    self.list_std_data[i].setText('{:.4f}'.format(stds_data))
                except Exception as e:
                    print('绘图报错{}'.format(e))
                    # messagess = '暂无数据'
            # 表格绘图
            try:
                table_count = 0 
                if len(plot_dataframe)!=0:
                    for i in plot_dataframe.iloc[-1,:]:
                        row = table_count//self.config_table_col
                        col = table_count%self.config_table_col*2+1
                        item = str(round(i,self.config_table_round))
                        try:
                            self.tableWidget_table_show.setItem(row,col,QtWidgets.QTableWidgetItem(item))
                        except Exception as e:
                            self.debug_list_3.append('{} table填充内容失败:{} {} {}'.format(self.normal_time,row,col,item))
                        table_count+=1

            except Exception as e:
                self.debug_list_3.append('{} table填充内容失败:{}'.format(self.normal_time,e))
                print(plot_dataframe)
            


        # 调试信息输出
        while len(self.debug_list_1)>0:
            self.textBrowser_debug_1.append(self.debug_list_1.pop(0))
        while len(self.debug_list_2)>0:
            self.textBrowser_debug_2.append(self.debug_list_2.pop(0))
        while len(self.debug_list_3)>0:
            self.textBrowser_debug_3.append(self.debug_list_3.pop(0))
        while len(self.debug_list_4)>0:
            self.textBrowser_debug_4.append(self.debug_list_4.pop(0))
        self.lineEdit_debug_message_list[2].append('总接收数:{}'.format(self.all_rec_hex))
        self.lineEdit_debug_message_list[3].append('校验失败:{}'.format(self.sum_check_err_count))

        for i in range(8):
            while len(self.lineEdit_debug_message_list[i])>0:
                self.lineEdit_debug_QlineEdit_list[i].setText(str(self.lineEdit_debug_message_list[i].pop(0)))
        

    #  事件更新2s线程，用于更新INU等需要时间计算的内容
    def show_message_2s(self):
        combobox_list = [
            self.comboBox_INU_choiceTab_stand,
            self.comboBox_INU_beginAxis_stand,
            self.comboBox_INU_choiceTab_target,
            self.comboBox_INU_beginAxis_loc,
            self.comboBox_INU_beginAxis_spd
        ]
        choiceTab_stand=0
        beginAxis_stand=0
        choiceTab_target=0
        beginAxis_loc=0
        beginAxis_spd=0
        get_combobox_list = [
            choiceTab_stand,
            beginAxis_stand,
            choiceTab_target,
            beginAxis_loc,
            beginAxis_spd
        ]
        for i in range(len(combobox_list)):
            try:
                get_combobox_list[i] = int(combobox_list[i].currentText().split()[0])
            except:
                get_combobox_list[i]=1
        
        if (self.inu_plot_always == True) | self.checkBox_INU_update_always.isChecked()| self.checkBox_INU_update_once.isChecked():
            self.checkBox_INU_update_once.setChecked(False)
            try:lon_axis = int(self.lineEdit_INU_plot_target_lon.text().split()[0])
            except:lon_axis = 1
            try:lat_axis = int(self.lineEdit_INU_plot_target_lat.text().split()[0])
            except:lat_axis = 1
            try:stand_lon_axis = int(self.lineEdit_INU_plot_target_lon.text().split()[0])
            except:stand_lon_axis = 1
            try:stand_lat_axis = int(self.lineEdit_INU_plot_target_lat.text().split()[0])
            except:stand_lat_axis = 1
            try:plot_tab = int(self.comboBox_INU_choiceTab_target.currentText().split()[0])
            except:plot_tab = 1
            try:stand_tab = int(self.comboBox_INU_choiceTab_stand.currentText().split()[0])
            except:stand_tab = 1
            try:nspd_axis = int(self.lineEdit_INU_plot_target_northspd.text().split()[0])
            except:nspd_axis = 1
            try:espd_axis = int(self.lineEdit_INU_plot_target_eastspd.text().split()[0])
            except:espd_axis = 1

            skip_count = try_get_text(self.lineEdit_INU_skipcount,int,1)
            end_count = try_get_text(self.lineEdit_INU_endcount,int,0)
            rolls = try_get_text(self.lineEdit_INU_rolling,int,0)
            plot_scatter_data = self.show_message_dataframe[plot_tab-1]
            plot_stand_data = self.show_message_dataframe[stand_tab-1]
            try:
                if end_count==0:
                    tar_lon = plot_scatter_data.iloc[skip_count:,lon_axis].reset_index(drop=True).rolling(rolls).mean()
                    tar_lat = plot_scatter_data.iloc[skip_count:,lat_axis].reset_index(drop=True).rolling(rolls).mean()
                else:
                    tar_lon = plot_scatter_data.iloc[skip_count:-end_count,lon_axis].reset_index(drop=True).rolling(rolls).mean()
                    tar_lat = plot_scatter_data.iloc[skip_count:-end_count,lat_axis].reset_index(drop=True).rolling(rolls).mean()
                
                self.scatter.setData(tar_lon,tar_lat)
            except Exception as e:
                self.debug_list_3.append('{} INU_plot 绘制scatter失败:{}'.format(self.normal_time,e))

            try:
                try:
                    stand_lon = float(self.lineEdit_INU_plot_stand_lon.text())
                except:
                    try:
                        stand_lon_axis = int(self.lineEdit_INU_plot_stand_lon.text().split()[0])
                        if end_count==0:
                            stand_lon = plot_stand_data.iloc[skip_count:,stand_lon_axis].reset_index(drop=True).rolling(rolls).mean()
                        else:
                            stand_lon = plot_stand_data.iloc[skip_count:-end_count,stand_lon_axis].reset_index(drop=True).rolling(rolls).mean()

                    except Exception as e:
                        stand_lon = 116.50271
                        self.debug_list_3.append('获取经度失败，使用默认值{}'.format(stand_lon))
                try:
                    stand_lat = float(self.lineEdit_INU_plot_stand_lat.text())
                except:
                    try:
                        stand_lat_axis =  int(self.lineEdit_INU_plot_stand_lat.text().split()[0])
                        if end_count==0:
                            stand_lat = plot_stand_data.iloc[skip_count:,stand_lat_axis].reset_index(drop=True).rolling(rolls).mean()
                        else:
                            stand_lat = plot_stand_data.iloc[skip_count:-end_count,stand_lat_axis].reset_index(drop=True).rolling(rolls).mean()
                    except Exception as e:
                        stand_lat = 39.73155
                        self.debug_list_3.append('获取纬度失败，使用默认值{}'.format(stand_lat))

                stand_lon = stand_lon*np.pi/180
                stand_lat = stand_lat*np.pi/180
                tar_lon = tar_lon*np.pi/180
                tar_lat = tar_lat*np.pi/180

                # print('stand_lon:{} stand_lat:{}'.format(stand_lon,stand_lat))
                # stand_lon = try_get_text(self.lineEdit_INU_plot_stand_lon,float,39.73155)*np.pi/180
                # stand_lat = try_get_text(self.lineEdit_INU_plot_stand_lat,float,116.50271)*np.pi/180
                
                dlon = tar_lon - stand_lon
                dlat = tar_lat - stand_lat

                a = np.sin(dlat / 2) ** 2 + np.cos(tar_lat) * np.cos(stand_lat) * np.sin(dlon / 2) ** 2
                c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
                c = c*6371000
                self.gv_pen_loc_error.setData(c)
            except Exception as e:
                self.debug_list_3.append('{} INU_plot 绘制位置误差失败:{}'.format(self.normal_time,e))
            try:
                if end_count==0:
                    tar_Nspd = plot_scatter_data.iloc[skip_count:,espd_axis].reset_index(drop=True).rolling(rolls).mean()
                    tar_Espd = plot_scatter_data.iloc[skip_count:,nspd_axis].reset_index(drop=True).rolling(rolls).mean()
                else:
                    tar_Nspd = plot_scatter_data.iloc[skip_count:-end_count,espd_axis].reset_index(drop=True).rolling(rolls).mean()
                    tar_Espd = plot_scatter_data.iloc[skip_count:-end_count,nspd_axis].reset_index(drop=True).rolling(rolls).mean()
                self.gv_pen_speed.setData(np.sqrt( tar_Nspd**2+tar_Espd**2 ))
            
            except Exception as e:
                self.debug_list_3.append('{} INU_plot 绘制速度误差失败:{}'.format(self.normal_time,e))








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
    # 发送装订 20240723
    def binding_send(self):
        send_commands = self.lineEdit_binding_command.text()
        try:
            send_tab = self.comboBox_binding_com.CurrentText()
            chosen_tab = send_tab.split()[0]
            chosen_tab_int = int(chosen_tab)
            self.binding_cache_list[chosen_tab_int-1].append(send_commands)
        except:
            self.debug_list_1.append('装订载入缓存:{}'.format(str(send_commands)))
            for i in range(12):
                self.binding_cache_list[i].append(send_commands)
    # 激光惯导#60所 构造装订函数
    def event_update_bingding_60s(self):
        lineedit_data_list = []
        for lineedit in self.binding_list_60s:
            try:
                get_data = float(lineedit.text())
            except Exception as e:
                get_data = 0
                self.debug_list_2.append('{} 获取装订内容失败:{}'.format(self.normal_time,e))
            lineedit_data_list.append(get_data)
        lineedit_data_list[1] /= 180/(2**31-1)
        lineedit_data_list[2] /= 90/(2**31-1)
        lineedit_data_list[7] /= 0.5
        for i in range(10):
            lineedit_data_list[i] = int(lineedit_data_list[i])



        command_list_head = ['99','66']
        command_list_len = ['2E']
        command_list = []
        command_list += hexcut2list(struct.pack('B', lineedit_data_list[0]).hex().upper())
        command_list += hexcut2list(struct.pack('<i', lineedit_data_list[1]).hex().upper())
        command_list += hexcut2list(struct.pack('<i', lineedit_data_list[2]).hex().upper())
        command_list += hexcut2list(struct.pack('b', lineedit_data_list[3]).hex().upper())
        command_list += hexcut2list(struct.pack('b', lineedit_data_list[4]).hex().upper())
        command_list += hexcut2list(struct.pack('b', lineedit_data_list[5]).hex().upper())
        command_list += ['00']*10   
        command_list += hexcut2list(struct.pack('b', lineedit_data_list[6]).hex().upper())
        command_list += ['00']
        command_list += hexcut2list(struct.pack('<h', lineedit_data_list[7]).hex().upper())
        command_list += hexcut2list(struct.pack('<h', lineedit_data_list[8]).hex().upper())
        command_list += hexcut2list(struct.pack('<h', lineedit_data_list[9]).hex().upper())
        command_list += ['00']*15
        try:
            checks = struct.pack('B',calculate_xorsum(bytes.fromhex(''.join(command_list)))).hex().upper()
        except Exception as e:
            self.debug_list_3.append('{} 60所装订异或校验失败:{}'.format(self.normal_time,e))
        command_list.append(checks)
        command_list = command_list_len+command_list
        try:
            checks = struct.pack('B',calculate_checksum(bytes.fromhex(''.join(command_list)))).hex().upper()
        except Exception as e:
            self.debug_list_3.append('{} 60所装订和校验失败:{}'.format(self.normal_time,e))
        command_list.append(checks)
        try:
            self.textEdit_binging_60s.setText(' '.join(command_list_head+command_list))
        except Exception as e:
            self.debug_list_3.append('{} 60所装订设置内容:{}'.format(self.normal_time,e))

    # 激光惯导#60所 发送装订函数
    def event_send_bingding_60s(self):
        send_commands = self.textEdit_binging_60s.toPlainText()
        try:
            send_tab = self.comboBox_binding_com_60s.CurrentText()
            chosen_tab = send_tab.split()[0]
            chosen_tab_int = int(chosen_tab)
            self.binding_cache_list[chosen_tab_int-1].append(send_commands)
        except:
            self.debug_list_1.append('装订载入缓存12路:{}'.format(str(send_commands)))
            for i in range(12):
                self.binding_cache_list[i].append(send_commands)
    


    # 通用卫导板卡发送函数
    def sate_send1_change_time(self):
        try:
            auto_time = int(self.lineEdit_sate_1_0.text())
            if auto_time>=10:
                self.sate_send1_autotime = auto_time
                self.sate_time1.start(self.sate_send1_autotime)
        except Exception as e:
            self.debug_list_2.append('{} 模块1获取定时时间错误{} {}'.format(self.normal_time,self.lineEdit_sate_1_0.text(),e))
    def sate_send2_change_time(self):
        try:
            auto_time = int(self.lineEdit_sate_2_0.text())
            if auto_time>=10:
                self.sate_send2_autotime = auto_time
                self.sate_time2.start(self.event_send_sate2)
        except Exception as e:
            self.debug_list_2.append('{} 模块2获取定时时间错误{} {}'.format(self.normal_time,self.lineEdit_sate_1_0.text(),e))


    def event_update_sate1(self):
        # $GNGGA,072820.800,3943.91626718,N,11630.17567593,E,1,19,0.714,45.422,M,-10.106,M,,,1.060*55
        ascii_list = []
        sate_list = []
        header = self.comboBox_sate_1_1.currentText()
        for item in self.sate_send1_line_list:
            try:
                sate_list.append(item.text())
            except:
                sate_list.append('')
        
        if len(sate_list[0])>0:
            try:sate_list[0] = str('{:.3f}'.format(float(sate_list[0])))
            except:sate_list[0] = '000000.000'
        if len(sate_list[1])>0:
            try:sate_list[1] = str('{:012.8f}'.format( lat_lon2str(sate_list[1]) ))
            except:sate_list[1] = '3943.91626718'
        if len(sate_list[2])>0:
            try:sate_list[2] = str('{:013.8f}'.format( lat_lon2str(sate_list[2]) ))
            except:sate_list[2] = '11630.17567593'
        if len(sate_list[3])>0:
            try:sate_list[3] = str(int(sate_list[3]))
            except:sate_list[3]='1'
        if len(sate_list[4])>0:
            try:sate_list[4] = str(int(sate_list[4])).rjust(2,'0')
            except:sate_list[4]='00'
        for i in range(3):
            if len(sate_list[5+i])>0:
                try:sate_list[5+i] = str( '{:.3f}'.format(float(sate_list[5+i])) )
                except:sate_list[5+i]='0.000'

        ascii_list.append(header)
        for i in range(2):
            ascii_list.append(sate_list[0+i])
        ascii_list.append('N')
        ascii_list.append(sate_list[2])
        ascii_list.append('E')
        for i in range(4):
            ascii_list.append(sate_list[3+i])
        ascii_list.append('M')
        ascii_list.append(sate_list[7])
        ascii_list.append('M')
        for i in range(2):
            ascii_list.append(sate_list[8+i])
        # print(' '.join(ascii_list))
        ascii_text = ','.join(ascii_list)
        # print(ascii_text)
        check_result = 0x00
        for bit in ascii_text:
            check_result^=ord(bit)
        check_result = hex(check_result&0xff)[2:].rjust(2,'0').upper()
        ascii_text = '$'+ascii_text+'*'+check_result
        self.textEdit_sate_msg_1.setText(ascii_text)
        # print(sate_list)

    def event_update_sate2(self):
        ascii_list = []
        sate_list = []
        header = self.comboBox_sate_2_1.currentText()
        for item in self.sate_send2_line_list:
            try:
                sate_list.append(item.text())
            except:
                sate_list.append('')
        if len(sate_list[0])>0:
            try:sate_list[0] = str('{:03.3f}'.format(float(sate_list[0])))
            except:sate_list[0] = '0.000'
        if len(sate_list[2])>0:
            try:sate_list[2] = str('{:03.3f}'.format(float(sate_list[2])))
            except:sate_list[2] = '0.000'
        if len(sate_list[4])>0:
            try:sate_list[4] = str('{:03.3f}'.format(float(sate_list[4])))
            except:sate_list[4] = '0.000'
        if len(sate_list[6])>0:
            try:sate_list[6] = str('{:04.3f}'.format(float(sate_list[4])))
            except:sate_list[6] = '0.000'
        if len(sate_list[7])>0:
            try:sate_list[7] = str(sate_list[7])
            except:sate_list[7] = 'N'
        ascii_list.append(header)
        for i in range(9):
            ascii_list.append(sate_list[i])
        ascii_text = ','.join(ascii_list)
        # print(ascii_text)
        check_result = 0x00
        for bit in ascii_text:
            check_result^=ord(bit)
        check_result = hex(check_result&0xff)[2:].rjust(2,'0').upper()
        ascii_text = '$'+ascii_text+'*'+check_result
        self.textEdit_sate_msg_2.setText(ascii_text)


        
    def event_send_sate1(self):
        if self.checkBox_sate_utc_1.isChecked():
            utc_now = datetime.now(timezone.utc)
            china_time = utc_now.astimezone( timezone(timedelta(hours=8)) )
            china_utc = china_time.strftime('%H%M%S.%f')[:-3]
            self.lineEdit_sate_1_1.setText(str(china_utc))
        if (self.checkBox_sate_time_1.isChecked()) | (isinstance(self.sender(),QtWidgets.QPushButton)):
            send_commands = self.textEdit_sate_msg_1.toPlainText()
            send_tab = 'all'
            try:
                send_tab = self.comboBox_sate_com_1.currentText()
                chosen_tab = int(send_tab.split()[0])
                self.ascii_cache_list[chosen_tab-1].append(send_commands)
                send_tab = str(chosen_tab)
            except:
                send_tab = 'all'
                for i in range(12):
                    self.ascii_cache_list[i].append(send_commands)
            self.debug_list_1.append('{} 卫导模块1_{}路发送装订:\n  {}'.format(self.normal_time,send_tab,send_commands))

    def event_send_sate2(self):
        if (self.checkBox_sate_time_2.isChecked()) | (isinstance(self.sender(),QtWidgets.QPushButton)):
            # self.debug_list_2.append('{} 卫导模块2发送装订:{}'.format(self.normal_time,'default'))
            send_commands = self.textEdit_sate_msg_2.toPlainText()
            send_tab = 'all'
            try:
                send_tab = self.comboBox_sate_com_2.currentText()
                chosen_tab = int(send_tab.split()[0])
                self.ascii_cache_list[chosen_tab-1].append(send_commands)
                send_tab = str(chosen_tab)
            except Exception as e:
                send_tab = 'all'
                for i in range(12):
                    self.ascii_cache_list[i].append(send_commands)
            self.debug_list_1.append('{} 卫导模块1_{}路发送装订:\n  {}'.format(self.normal_time,send_tab,send_commands))
    def event_send_sate3(self):
        self.debug_list_2.append('{} 模块3装订未设置'.format(self.normal_time))
        return False
    



    # 开启电源事件 20240813
    def event_power_on(self,command='all'):
        if isinstance(self.sender(),QtWidgets.QPushButton):
            command = 'all'
        serial_com = self.comboBox_power_com.currentText()
        self.debug_list_1.append('{} 开启电源{}:{}'.format(self.normal_time,serial_com,command))
        if str(self.config_power_model)=='1':
            power_serials = serial.Serial(serial_com, 57600)
            power_serials.write(':OUTP 1\n'.encode('ascii'))
            time.sleep(0.1)
            power_serials.write(':OUTP 1\n'.encode())
            power_serials.close()
        elif str(self.config_power_model)=='2':
            try:
                power_serials = serial.Serial(serial_com, 9600)
            except Exception as e:
                self.debug_list_1.append('{} 开启电源串口错误:{}'.format(self.normal_time,e))
            if command=='all':
                for power_count in range(4):
                    power_serials.write(('{\"A0%s\":110000}'%(power_count+1)).encode('ascii'))
                time.sleep(0.1)
                for power_count in range(4):
                    power_serials.write(('{\"A0%s\":110000}'%(power_count+1)).encode())
                power_serials.close()
            else:
                power_serials.write(('{\"A0%s\":110000}'%(int(command))).encode())
            power_serials.close()
        else:
            self.show_message_automatic_list.append('未知命令:{}'.format())

    # 关闭电源事件 20240813
    def event_power_off(self,command='all'):
        if isinstance(self.sender(),QtWidgets.QPushButton):
            command = 'all'
        serial_com = self.comboBox_power_com.currentText()
        self.debug_list_1.append('{} 关闭电源{}:{}'.format(self.normal_time,serial_com,command))
        if str(self.config_power_model)=='1':
            power_serials = serial.Serial(serial_com, 57600)
            power_serials.write(':OUTP 0\n'.encode('ascii'))
            time.sleep(0.1)
            power_serials.write(':OUTP 0\n'.encode())
            power_serials.close()
        elif str(self.config_power_model)=='2':
            power_serials = serial.Serial(serial_com,9600)
            # print('com{} 电源off 命令{}'.format(serial_com,command))
            if command=='all':
                for power_count in range(4):
                    power_serials.write(('{\"A0%s\":100000}'%(power_count+1)).encode('ascii'))
                time.sleep(0.1)
                for power_count in range(4):
                    power_serials.write(('{\"A0%s\":100000}'%(power_count+1)).encode())
            else:
                power_serials.write(('{\"A0%s\":100000}'%(int(command))).encode())
            power_serials.close()
            
        else:
            self.show_message_automatic_list.append('未知命令:{}'.format(list_plan[2]))

    # 点击自动设置经纬速度事件 20241028
    def event_autoset_inu(self):
        self.lineEdit_INU_plot_stand_lon.setText(str(self.default_longitude))
        self.lineEdit_INU_plot_stand_lat.setText(str(self.default_latitude))
        self.lineEdit_INU_skipcount.setText('300')
        for i in range(len(self.sorted_titl_list)):
            if '经度' in self.sorted_titl_list[i]:
                self.lineEdit_INU_plot_target_lon.setText('{} {}'.format(i,self.sorted_titl_list[i]))
            if '纬度' in self.sorted_titl_list[i]:
                self.lineEdit_INU_plot_target_lat.setText('{} {}'.format(i,self.sorted_titl_list[i]))
            if ('北' in self.sorted_titl_list[i]) & ('速' in self.sorted_titl_list[i]):
                self.lineEdit_INU_plot_target_northspd.setText('{} {}'.format(i,self.sorted_titl_list[i]))
            if ('东' in self.sorted_titl_list[i]) & ('速' in self.sorted_titl_list[i]):
                self.lineEdit_INU_plot_target_eastspd.setText('{} {}'.format(i,self.sorted_titl_list[i]))
        return 0
    def event_reload_config(self):
        self.read_default_para_config()



    # 载入文件事件 使用df打开文件/使用数据解算hex 20240814
    def event_load_file(self):
        self.auto_plot_always = True
        dir = QtWidgets.QFileDialog()
        try:
            # dir.setDirectory('.//')
            path = os.getcwd()  
            dir.setDirectory(path)
        except:
            dir.setDirectory('C:\\')
        if dir.exec_():
            file_path = str(dir.selectedFiles()[0])
            print(file_path)
        else:
            return False
        try:
            # with open(file_path,'r') as f:
            #     for i in range(10):
            #         print(f.readlines())
            df = pd.read_csv(file_path,sep='\\s+',header=None,skiprows=1)
            self.show_message_dataframe[0] = df
            self.show_message_automatic_list.append('{} 文件长度{} 文件路径:\n{}'.format(self.normal_time,len(df),file_path))
            self.show_timer2.start(self.default_plot_load)
        except Exception as e:
            self.debug_list_3.append('{} 使用空格打开文件失败:{}'.format(self.normal_time,e))
            try:
                df = pd.read_csv(file_path,sep=r'[,，\s]+',header=None,skiprows=1,engine='python')
                self.show_message_dataframe[0] = df
            except Exception as e:
                self.debug_list_3.append('{} 使用逗号打开文件失败:{}'.format(self.normal_time,e))
                try:
                    with open(file_path,'rb+') as f:
                        hex_data = f.read()
                    self.read_rules()
                    self.save_data_flag = True      # 开启保存
                    self.turntable_ready = True     # 忽略转台/ 转台到位标志位
                    self.auto_plot_always = True    # 持续更新绘图
                    self.threading_test_flag = True
                    self.threading_list_flag[0] = True
                    self.lineEdit_automatic_mode_list.append('解算中')
                    self.show_message_automatic_list.append('{} 载入hex文件并尝试解算\n{}'.format(self.normal_time,file_path))
                    # self.threading_receive_data(0,hex_data)
                    thread_receive = threading.Thread(target=self.threading_receive_data,args=(0,hex_data))
                    thread_receive.setDaemon(True)
                    thread_receive.start()


                except Exception as e:
                    self.debug_list_3.append('{} 使用hex打开文件失败:{}'.format(self.normal_time,e))

            # print(hex_data[:100].hex())
            # print(len(hex_data))
        decode_rule_name = self.comboBox_protocal_rule.currentText()
        with open('./解算规则/{}.txt'.format(decode_rule_name), 'r+') as f:
            decode_rule_file = f.read()
        decode_struct = class_rule()
        decode_struct.read_rule_file(decode_rule_file)


 
    # 读取默认配置文件-全局串口 20240427
    def read_default_para_com(self):
        # 串口默认配置
        para_name = self.para_com_filename
        if not os.path.exists(para_name):
            self.show_message_automatic_list.append('未读取到默认配置文件({})'.format(para_name))
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
                        self.show_message_automatic_list.append('read_default_para_com未知配置项：%s'%(para_rule_list))
    # 读取默认配置文件-全局设置 20240507
    def read_default_para_config(self):
        para_name = self.para_config_filename
        if not os.path.exists(para_name):
            self.show_message_automatic_list.append('未读取到默认配置文件({})'.format(para_name))
        else:
            with open(para_name,'r',encoding='gb2312',errors='replace') as f:
                for line in f:
                    para_rule_list = line.split()
                    if line.startswith('#'):
                        continue
                    elif len(para_rule_list)<3:
                        continue
                    try:
                        int_para_confing = float(para_rule_list[2])
                    except:
                        self.show_message_automatic_list.append('未知配置项：%s read_default_para_config'%(para_rule_list))
                        continue
                    # 默认转台速度设置
                    if para_rule_list[1]=='in_spd':
                        self.lineEdit_inside_speed.setText(para_rule_list[2])
                        self.config_in_spd = int(para_rule_list[2])
                    elif para_rule_list[1]=='in_acc':
                        self.lineEdit_inside_acceleration.setText(para_rule_list[2])
                        self.config_in_acc = int(para_rule_list[2])
                    elif para_rule_list[1]=='out_spd':
                        self.lineEdit_outside_speed.setText(para_rule_list[2])
                        self.config_out_spd = int(para_rule_list[2])
                    elif para_rule_list[1]=='out_acc':
                        self.lineEdit_outside_acceleration.setText(para_rule_list[2])
                        self.config_out_acc = int(para_rule_list[2])
                    # 默认转台稳定后等待时间
                    elif para_rule_list[1]=='hold_time':
                        self.config_hold_time = int(para_rule_list[2])
                    # 是否保存毫秒值
                    elif para_rule_list[1]=='save_alldata_ms':
                        self.config_save_alldata_ms = int(para_rule_list[2])
                    # 是否保存毫秒值
                    elif para_rule_list[1]=='save_alldata_s':
                        self.config_save_alldata_s = int(para_rule_list[2])
                    # 是否保存毫秒值
                    elif para_rule_list[1]=='save_alldata_calib':
                        self.config_save_alldata_calib = int(para_rule_list[2])
                    # 是否保存毫秒值
                    elif para_rule_list[1]=='save_readydata_ms':
                        self.config_save_readydata_ms = int(para_rule_list[2])
                    # 是否保存毫秒值
                    elif para_rule_list[1]=='save_readydata_s':
                        self.config_save_readydata_s = int(para_rule_list[2])
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
                    elif para_rule_list[1]=='save_alldata_bin':
                        self.config_save_alldata_bin = int(para_rule_list[2])
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
                    elif para_rule_list[1]=='turntable_check_status':
                        self.config_turntable_check_status = int(para_rule_list[2])
                    elif para_rule_list[1]=='default_longitude':
                        self.default_longitude = float(para_rule_list[2])
                    elif para_rule_list[1]=='default_latitude':
                        self.default_latitude = float(para_rule_list[2])
                    elif para_rule_list[1]=='default_g':
                        self.default_g = float(para_rule_list[2])
                    elif para_rule_list[1]=='default_table_row':
                        self.config_table_row = int(para_rule_list[2])
                    elif para_rule_list[1]=='default_table_col':
                        self.config_table_col = int(para_rule_list[2])//2
                    elif para_rule_list[1]=='default_table_round':
                        self.default_table_round = int(para_rule_list[2])
                    elif para_rule_list[1]=='default_plot_enable':
                        self.default_plot_enable = int(para_rule_list[2])
                    elif para_rule_list[1]=='default_plot_limit':
                        self.default_plot_limit = int(para_rule_list[2])
                    elif para_rule_list[1]=='default_plot_time':
                        self.default_plot_time = int(para_rule_list[2])
                    elif para_rule_list[1]=='default_plot_load':
                        self.default_plot_load = int(para_rule_list[2])
                    elif para_rule_list[1]=='default_sumcheck_flag':
                        self.default_sumcheck_flag = int(para_rule_list[2])
                    else:
                        self.show_message_automatic_list.append('read_default_para_config未知配置项：%s'%(para_rule_list))
    # 读取载入解算规则文件  20240513
    # 读取规则文件并更新全局变量
    # debug:惯导协议改文件中行60标题无法使用"卫星数"，暂时替换为其他
    def read_rules(self):
        # 初始化各项内容
        self.config_sum_check = None
        try:
            sender = self.sender()
            sender_from_combox = isinstance(sender,QtWidgets.QComboBox)
        except Exception as e:
            print('输出sender失败:{}'.format(e))
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
            with open('./解算规则/{}.txt'.format(rule_name), 'r',encoding='gb2312',errors='ignore') as files:
                rules = files.read()
                
        except Exception as e:
            self.show_message_automatic_list.append('读取规则文件失败:'+str(e))
            return False
        # try:
        #     self.decode_class.read_rule_file(rules)
        # except Exception as e:
        #     self.show_message_automatic_list.append('使用类载入规则失败:{} {}'.format(rule_name,e))

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

        drop0data = []
        
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
                    if sender_from_combox:
                        self.comboBox_protocal_baund.setCurrentText(lines.split()[2])
                        self.combox_set_baund_all.setCurrentText(lines.split()[2])
                # 校验位
                elif lines.split()[1].lower() == 'check':   
                    if sender_from_combox:
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
                elif lines.split()[1].lower() == 'latitude':
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
                elif lines.split()[1].lower() == 'sum_check':
                    self.config_sum_check = lines.split()[2]
                elif lines.split()[1].lower() == 'drop0data':
                    line_split = lines.split()[2]
                    for i in range(9):
                        if str(i) in line_split:
                            drop0data.append(i)
                
                    
                elif lines.split()[1].lower() == 'rulelist':
                    continue
                # 读取规则文件-新
                elif lines.split()[1].lower()=='rulehead':
                    # decode_edia_list.append(lines.split()[2])
                    # default_edia = lines.split()[2]
                    if len(decode_rule)==0:
                        default_edia = lines.split()[2]
                        continue
                    else:
                        decode_rule_list.append(decode_rule)
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
                    default_edia = lines.split()[2]
                else:
                    if self.debug_flag | self.debug_read_rules:
                        print('未知规则:<{}>split:<{}>'.format(lines,lines.split()))
                    continue
            # 判断不合法规则
            elif len(lines)==0 | len(lines.split())==0:
                continue
            elif len(lines.split())<5:
                self.show_message_automatic_list.append('规则文件错误:{}\n《{}》：《{}》'.format(rule_name,read_line_count,lines))
                continue
            elif lines.split()[0] not in rules_lists_format:
                self.show_message_automatic_list.append('不在解算规则范围内《{}》'.format(lines))
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
            decode_edia_list.append(default_edia)
        
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
        sorted_title_list = []
        for i in range(len(decode_save_list)):
            sorted_title_list+=[decode_titl_list[i][decode_sort_list[i].index(str(j))] for j in range(len(decode_titl_list[i])) if decode_save_list[i][decode_sort_list[i].index(str(j))]=='1']
        
        self.decode_rule_list = decode_rule_list    # 解算规则
        self.decode_save_list = decode_save_list    # 是否保存
        self.decode_para_list = decode_para_list    # 系数
        self.decode_titl_list = decode_titl_list    # 标题
        self.decode_cout_list = decode_cout_list    # 排序序号
        self.decode_sort_list = decode_sort_list    # 排序后列表
        self.decode_edia_list = decode_edia_list    # 大小端
        self.decode_fram_leng = decode_fram_leng    # 帧长度
        self.sorted_titl_list = sorted_title_list   # 排序后的标题
        
        
        
        # self.comboBox_plot_beginAxis.clear()
        # for i in range(len(sorted_title_list)):
        #     self.comboBox_plot_beginAxis.addItem('{} {}'.format(i,sorted_title_list[i]))
        # self.comboBox_plot_beginAxis.setCurrentIndex(1)
        combobox_lists = [
            self.comboBox_plot_beginAxis,
            self.comboBox_INU_beginAxis_stand,
            self.comboBox_INU_beginAxis_loc,
            self.comboBox_INU_beginAxis_spd
        ]
        for combobox_item in combobox_lists:
            combobox_item.clear()
            for i in range(len(sorted_title_list)):
                combobox_item.addItem('{} {}'.format(i,sorted_title_list[i]))
            combobox_item.setCurrentIndex(1)
                                                
        # self.textBrowser_fileCsv.append('主机规则载入完成')      
        # self.fileCsv_append_flag = True
        # 处理卫导丢0模块
        self.drop0data = []
        if len(drop0data)>0:
            for i in drop0data:
                if i in range(len(decode_save_list)):
                    if i==0:
                        begin = 0
                    else:
                        begin = sum([int(num) for num in decode_save_list[i-1]])
                    end = sum([int(num) for num in decode_save_list[i]])
                    for drop_count in range(begin,begin+end):
                        self.drop0data.append(drop_count)
                else:
                    self.debug_list_2.append('卫导去0值范围错误')
            # print(self.drop0data)
        self.tableWidget_table_show.clearContents()
        for i in range(len(self.sorted_titl_list)):
            row = i//self.config_table_col
            col = i%self.config_table_col*2
            item = self.sorted_titl_list[i]
            messages = 'row:{} col:{} data:{}'.format(row,col,item)
            try:
                self.tableWidget_table_show.setItem(row,col,QtWidgets.QTableWidgetItem(self.sorted_titl_list[i]))
            except Exception as e:
                self.debug_list_2.append('{} 显示table追加item失败：{}'.format(self.normal,messages))

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
        command_list+=hexcut2list(struct.pack('>i', binding_latitude).hex().upper())
        command_list+=hexcut2list(struct.pack('>i', binding_longitude).hex().upper())
        command_list+=hexcut2list(struct.pack('>i', binding_height).hex().upper())[-2:]
        command_list+=hexcut2list(struct.pack('>i', binding_time).hex().upper())[-1:]
        try:
            checks = struct.pack('B',calculate_checksum(bytes.fromhex(''.join(command_list)))).hex().upper()
        except Exception as e:
            print('checks计算错误:{}'.format(e))
            print('command_list:{}'.format(command_list))
        command_list.append(checks)
        if self.bebug_binding:
            print(' '.join(command_list1+command_list))
        self.lineEdit_binding_command.setText(' '.join(command_list1+command_list))
    # 起始更换时刷新三轴绘图内容
    def update_plot_axis(self):
        try:
            currenttext = self.comboBox_plot_beginAxis.currentText()
            if len(currenttext)==0:
                return False
            begin_axis = int(currenttext.split()[0])
        except Exception as e:
            print('update_plot_axis函数错误:{}\t当前项<{}>'.format(e,currenttext))
            return False
        if begin_axis<len(self.sorted_titl_list)-3:
            begin_axis = begin_axis
        else:
            begin_axis = len(self.sorted_titl_list)-3
        for i in range(3):
            self.findChild(QtWidgets.QLineEdit, 'lineEdit_inside_plot_axis{}'.format(i+1)).setText('{} {}'.format(i+begin_axis,self.sorted_titl_list[i+begin_axis]))
    # 更新目标标题和选择
    def update_stand_axis(self):
        try:
            currenttext = self.comboBox_INU_beginAxis_stand.currentText()
            if len(currenttext)==0:
                return False
            begin_axis = int(currenttext.split()[0])
            # begin_axis = int(self.comboBox_INU_beginAxis_stand.currentText().split()[0])
        except Exception as e:
            self.debug_list_1.append('update_stand_axis函数错误:{}\t当前项{}'.format(e,self.comboBox_INU_beginAxis_stand.currentText()))
            return False
        if begin_axis<len(self.sorted_titl_list)-2:
            begin_axis = begin_axis
        else:
            begin_axis = len(self.sorted_titl_list)-2
        try:
            i=0
            self.lineEdit_INU_plot_stand_lon.setText('{} {}'.format(i+begin_axis,self.sorted_titl_list[i+begin_axis]))
            i+=1
            self.lineEdit_INU_plot_stand_lat.setText('{} {}'.format(i+begin_axis,self.sorted_titl_list[i+begin_axis]))
        except Exception as e:
            self.debug_list_1.append('update_stand_axis错误:{}'.format(e))
    def update_target_loc(self):
        try:
            currenttext = self.comboBox_INU_beginAxis_loc.currentText()
            if len(currenttext)==0:
                return False
            begin_axis = int(currenttext.split()[0])
            # begin_axis = int(self.comboBox_INU_beginAxis_loc.currentText().split()[0])
        except Exception as e:
            self.debug_list_1.append('update_target_loc函数错误:{}\t当前项{}'.format(e,self.comboBox_INU_beginAxis_loc.currentText()))
            return False
        if begin_axis<len(self.sorted_titl_list)-2:
            begin_axis = begin_axis
        else:
            begin_axis = len(self.sorted_titl_list)-2
        try:
            i=0
            self.lineEdit_INU_plot_target_lon.setText('{} {}'.format(i+begin_axis,self.sorted_titl_list[i+begin_axis]))
            i+=1
            self.lineEdit_INU_plot_target_lat.setText('{} {}'.format(i+begin_axis,self.sorted_titl_list[i+begin_axis]))
        except Exception as e:
            self.debug_list_1.append('update_target_loc错误:{}'.format(e))
    def update_target_spd(self):
        try:
            currenttext = self.comboBox_INU_beginAxis_spd.currentText()
            if len(currenttext)==0:
                return False
            begin_axis = int(currenttext.split()[0])
            # begin_axis = int(self.comboBox_INU_beginAxis_spd.currentText().split()[0])
        except Exception as e:
            self.debug_list_1.append('update_target_loc函数错误:{}\t当前项{}'.format(e,self.comboBox_INU_beginAxis_spd.currentText()))
            return False
        if begin_axis<len(self.sorted_titl_list)-2:
            begin_axis = begin_axis
        else:
            begin_axis = len(self.sorted_titl_list)-2
        try:
            i=0
            self.lineEdit_INU_plot_target_northspd.setText('{} {}'.format(i+begin_axis,self.sorted_titl_list[i+begin_axis]))
            i+=1
            self.lineEdit_INU_plot_target_eastspd.setText('{} {}'.format(i+begin_axis,self.sorted_titl_list[i+begin_axis]))
        except Exception as e:
            self.debug_list_1.append('update_target_loc错误:{}'.format(e))


        
    
    
    
    
    def stop_test(self):
        if self.debug_flag:
            print('停止测试')
        self.show_message_automatic_list.append('{} 停止测试'.format(self.normal_time))
        # if not self.threading_test_flag:
        #     self.auto_plot_always = False
        self.threading_test_flag = False
        self.plan_threading_flag = False
    # 点击开始测试事件，判断测试模式
    def begin_test(self):
        if self.debug_flag:
            print('开启测试')
        self.read_rules()
        self.default_plot_flag = True
        self.show_timer2.start(1000)
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
        self.save_ztrd_flag = False     # 转台到位标志位
        self.turntable_ready = False
        self.show_message_clear = True  # 清空12路显示信息
        
        
        if not ((turntable_rule.lower()=='none')|(turntable_rule.lower()=='选择协议')):
            begin_test_mode = 'turntable_test'
        if not ((automatic_rule.lower()=='none')|(automatic_rule.lower()=='选择协议')):
            begin_test_mode = 'automatic_test'
        self.test_mode = begin_test_mode
        self.show_message_automatic_list.append('{} 模式:{}'.format(self.normal_time,testmode2chinese(begin_test_mode))) 
        if begin_test_mode=='only_test':
            self.save_data_flag = True      # 开启保存
            self.turntable_ready = True     # 忽略转台/ 转台到位标志位
            self.auto_plot_always = True    # 持续更新绘图
            self.only_test()
        elif begin_test_mode=='turntable_test':
            self.plan_threading_flag = True
            self.bd_test()
        elif begin_test_mode=='automatic_test':
            self.plan_threading_flag = True
            self.turntable_ready = False
            self.bd_plan_flag = False
            self.plan_test()
            
        
        
    # 单独测试模式、通用惯导采集
    def only_test(self):
        protocal_rule = self.comboBox_protocal_rule.currentText()
        protocal_com = self.comboBox_protocal_com.currentText()
        protocal_baund = self.comboBox_protocal_baund.currentText()
        protocal_check = self.comboBox_protocal_check.currentText()
        thread_receive_list = []
        thread_decode_list = []
        self.threading_test_flag = False
        self.threading_begin_time = time.time()
        time.sleep(0.5)
        self.threading_test_flag = True
        self.lineEdit_automatic_mode_list.append('数据接收中')
        for i in range(12):
            self.threading_list_flag[i] = False
            time.sleep(0.01)
            if self.combox_com_open_list[i].text() == '开启':
                if protocal_com.lower()=='none':
                    self.show_message_dis1_list.append('tab_{}:线程开启，串口{}'.format(i+1,protocal_com))
                    continue
                self.threading_list_flag[i] = True
                thread_receive = threading.Thread(target=self.threading_receive_data,args=(i,))
                thread_receive.setDaemon(True)
                # thread_receive.daemon = True
                thread_receive_list.append(thread_receive)
                thread_receive.start()
    # 标定测试模式、转台同步控制
    def bd_test(self):
        if self.test_mode == 'only_test':
            self.only_test()
        elif self.test_mode == 'turntable_test':
            thread_turn = threading.Thread(target=self.begin_test_bd)
            thread_turn.setDaemon(True)
            thread_turn.start()
            self.only_test()
        elif self.test_mode == 'automatic_test':
            self.only_test()
            self.begin_test_bd()
        else:
            print('转台标定时未确定标定逻辑')
    def plan_test(self):
        thread_plan = threading.Thread(target=self.plan_test_threading)
        thread_plan.setDaemon(True)
        thread_plan.start()
        
        
        

    def threading_receive_data(self,thread_num,decode_hex=None):
        if isinstance(decode_hex,bytes):
            load_decode_hex = decode_hex
            # self.debug_list_3.append('{} 解算hex:\n{}'.format(self.normal_time,decode_hex[:200]))
        else:
            load_decode_hex = b''
            
        receive_begin_time = time.time()
        self.debug_list_2.append('{} tab_{}:接收进程开启 当前状态:\nthreading_test_flag:{} threading_list_flag[thread_num]:{}'.format(
            self.normal_time,thread_num,self.threading_test_flag,self.threading_list_flag[thread_num]
            ))
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
        now = datetime.now()
        save_time = '{:02d}{:02d}{:02d}'.format(now.hour,now.minute,now.second)
        file_path = './测试数据/{}{}/{}/'.format(int2str(now.year),int2str(now.month),int2str(now.day))
        # 标定保存文件路径
        bd_file_path=file_path+str(self.plan_name)+'/'
        
        
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
        # 保存文件名
        # if len(self.plan_name)>0:
        #     name = '{}#{}'.format(name,self.plan_name)
        hex_filename = '{}{}_{}_hex.hex'.format(file_path,name,save_time)
        hz_filename  = '{}{}_{}_hz.txt'.format(file_path,name,save_time)
        bd_filename  = '{}{}_{}_bd.txt'.format(file_path,name,save_time)
        calib_filename= '{}{}_{}_hz_calib.txt'.format(file_path,name,save_time)
        s_filename   = '{}{}_{}_s.txt'.format(file_path,name,save_time)
        ave_filename = '{}{}_{}_ave.txt'.format(file_path,name,save_time)
        
        alldata_ms  = ''
        alldata_s   = ''
        all_data = b''
        all_data += load_decode_hex
        alldata_bin = b''
        alldata_calib=''
        readydata_ms= ''
        readydata_s = ''
        pop_count = 0
        frame_error_count = 0
        self.show_message_dataframe[thread_num] = pd.DataFrame([])
        self.show_message_dataframe_cache[thread_num] = []
        self.all_rec_hex = 0
        self.sum_check_err_count = 0
        all_save_data_time = 0
        all_decode_data_time = 0

        config_sum_check = None
        if self.config_sum_check is not None:
            # [2,3:61]
            try:
                split_sum = self.config_sum_check.split('[')[1].split(']')[0]
                split_sum = split_sum.replace('，',',')
                split_sum = split_sum.replace('：',':')
                try:
                    sum_addr = int(split_sum.split(',')[0])
                except Exception as e:
                    self.debug_list_2.append('{} 获取校验和位置出错:{} {}'.format(self.normal_time,split_sum,e))
                    self.config_sum_check = None
                try:
                    sum_addr_begin = int(split_sum.split(',')[1].split(':')[0])
                    sum_addr_end = int(split_sum.split(',')[1].split(':')[1])
                except Exception as e:
                    self.debug_list_2.append('{} 获取校验和起始点出错:{} {}'.format(self.normal_time,split_sum,e))
                    self.config_sum_check = None
                if self.config_sum_check is not None:
                    config_sum_check = [sum_addr,sum_addr_begin,sum_addr_end]
                else:
                    config_sum_check = None
            except Exception as e:
                self.config_sum_check = None
                config_sum_check = None
                self.debug_list_2.append('{} 获取校验和错误:{}'.format(self.normal_time,e))

        
        
        sorted_title_list = []
        for i in range(len(decode_save_list)):
            sorted_title_list+=[decode_titl_list[i][decode_sort_list[i].index(str(j))] for j in range(len(decode_titl_list[i])) if decode_save_list[i][decode_sort_list[i].index(str(j))]=='1']
        zeros_list = [0 for i in range(len(sorted_title_list))]
        last_not0data = zeros_list
        receive_data_s = zeros_list
        # print('当前:{} turntable_ready:{}'.format(thread_num,self.turntable_ready))
        continue_check = False
        # 创建标题
        if save_test_title &self.config_save_BD_1file:
            if not os.path.exists(s_filename):
                with open(s_filename,'a+') as f:
                    f.write('\t'.join(sorted_title_list)+'\n')
        # 创建串口线程
        try:
            if not isinstance(decode_hex,bytes):
                serials = serial.Serial(com, baund, parity=checks,stopbits=stops)
        except :
            time.sleep(1)
            try:
                self.debug_list_2.append('{} tab_{}:第一次开启串口失败,com:{}'.format(self.normal_time,thread_num,com))
                serials = serial.Serial(com, baund, parity=checks,stopbits=stops)
            except Exception as e:
                self.debug_list_2.append('{} tab_{}:第二次开启串口失败,com:{},线程关闭 {}'.format(self.normal_time,thread_num,com,e))
                self.threading_list_flag[thread_num] = False
                self.show_message_automatic_list.append('{} tab_{} com:{} 开启失败'.format(self.normal_time,thread_num,com))
        threading_begin_time = time.time()  
        # print('threading_test_flag:{} threading_list_flag:{} thread_num:{}'.format(
        #     self.threading_test_flag, self.threading_list_flag[thread_num],thread_num
        #     ))
        # print(decode_hex[:200])
        if isinstance(decode_hex,bytes):
            frame_list = [ all_data[i*decode_fram_leng:(i+1)*decode_fram_leng] for i in range(len(all_data)//decode_fram_leng) ]
            frame_list_len = len(frame_list)
            frame_list_count = 0
        # 开始测试
        while self.threading_test_flag & self.threading_list_flag[thread_num]:
            # 发送装订指令
            try:
                if len(self.binding_cache_list[thread_num])>0:
                    send_commands = self.binding_cache_list[thread_num].pop(0)
                    serials.write(bytes.fromhex(send_commands))
                    self.debug_list_1.append('{}：发送装订:{}'.format(thread_num,send_commands))
            except Exception as e:
                # print('发送装订失败')
                self.debug_list_1.append('{} 发送装订失败{}\n{}发送装订失败{}'.format(self.normal_time,send_commands,self.normal_time,e))
            
            try:
                if len(self.ascii_cache_list[thread_num])>0:
                    send_commands = str(self.ascii_cache_list[thread_num].pop(0))+'\r\n'
                    serials.write(send_commands.encode('ascii'))
                    self.debug_list_1.append('{}：发送装订:{}'.format(thread_num,send_commands))
            except Exception as e:
                # print('发送装订失败')
                self.debug_list_1.append('{} 发送装订失败{}\n{}发送装订失败{}'.format(self.normal_time,send_commands,self.normal_time,e))


            # 满足接收要求
            try:
                waiting = serials.in_waiting
            except:
                waiting = 0
            if waiting>=decode_fram_leng:
                cache_hex_data = serials.read(waiting)
                self.all_rec_hex+=waiting
                # print(cache_hex_data)
                if self.config_save_alldata_bin:
                    alldata_bin+=cache_hex_data
                all_data += cache_hex_data
            # 等待转台第一次到位
            if not self.turntable_ready:
            # if not self.serial_test_begin_flag:
                all_data = b''
                alldata_bin = b''
            # print(all_data[:200])
            # 保存原始数据
            if (self.config_save_alldata_bin)&(time.time()-threading_begin_time>10):
                with open(hex_filename,'ab+') as f:
                    f.write(alldata_bin)
                    alldata_bin = b''
                    threading_begin_time = time.time()
            # 长度满足解算要求
            if isinstance(decode_hex,bytes):
                hex_length_result = (len(frame_list)>0) & (frame_list_count<(len(frame_list)-1))
                # print(len())
            else:
                hex_length_result = (len(all_data)>=decode_fram_leng*2)
            if hex_length_result:
                decode_begin_time = time.time()
                if isinstance(decode_hex,bytes):
                    frame = frame_list[frame_list_count]
                    next_frame = frame_list[frame_list_count+1]
                else:
                    frame = all_data[:decode_fram_leng]
                    next_frame = all_data[decode_fram_leng:decode_fram_leng*2]
                if frame.startswith(decode_rule_header) & next_frame.startswith(decode_rule_header): 
                    
                    frame_error_count = 0
                    if isinstance(decode_hex,bytes):
                        # frame_list = frame_list[1:]
                        frame_list_count+=1
                    else:
                        all_data = all_data[decode_fram_leng:]
                    hz_count+=1
                    receive_hz_count+=1
                    receive_data_hz,sum_check_result = decode_hex_frame_list(frame,decode_rule_list,decode_save_list,decode_para_list,decode_sort_list,decode_edia_list,config_sum_check)
                    alldata_ms += '\t '.join(['{:.{}f}'.format(i,save_decimal_point)if type(i)==float else str(int(i)) for i in receive_data_hz])+'\n'
                    readydata_ms += '\t '.join(['{:.{}f}'.format(i,save_decimal_point) for i in receive_data_hz])+'\n'
                    if len(self.drop0data)>0:
                        last_not0data = [ last_not0data[i] if (float(receive_data_hz[i])==0) else receive_data_hz[i]  for i in range(len(receive_data_hz))]

                    if self.config_sum_check is not None:
                        if sum_check_result:
                            sum_check_result = True
                        else:
                            self.sum_check_err_count+=1
                            if self.default_sumcheck_flag:
                                continue
                    
                    # 处理累积calib数据
                    # alldata_calib+=str(receive_hz_count).ljust(10,' ')+'\t'
                    if self.config_save_alldata_calib:
                        alldata_calib+=str(receive_data_hz[0]).ljust(10,' ')+'\t'
                        for i in range(6):
                            alldata_calib+=str(receive_data_hz[i+1]).rjust(16,' ')+'\t'
                        alldata_calib+=str(self.bd_calib_flag).rjust(2,' ')+'\n'
                            # calib_receive_data_hz+=str(receive_data_hz[0]).ljust(10,' ')+'\t'
                            
                    if hz_count<receive_hz+1:
                        receive_data_s = [receive_data_s[i]+receive_data_hz[i] for i in range(len(receive_data_hz))]
                    else:
                        save_data_begin_time = time.time()
                        hz_count = 0
                        receive_s_count+=1  
                        receive_data_s = [i/receive_hz for i in receive_data_s]
                        try:
                            if len(self.drop0data)>0:
                                for i in self.drop0data:
                                    receive_data_s[i] = last_not0data[i]
                        except Exception as e:
                            print('e:{} data:{}'.format(e,self.drop0data))
                        data_save_lists = ['{:.{}f}'.format(i,save_decimal_point)if type(i)==float else str(int(i)) for i in receive_data_s]
                        receive_data_save = '\t'.join(data_save_lists)
                        show_data_save = '    '.join(data_save_lists)
                        self.show_message_list[thread_num].append(show_data_save)
                        # self.show_message_dataframe[thread_num] = pd.concat([self.show_message_dataframe[thread_num],pd.DataFrame(receive_data_s).T],axis=0)
                        self.show_message_dataframe_cache[thread_num].append(receive_data_s)
                        receive_data_s = zeros_list
                        
                        # 满1s开始保存
                        # 常态保存
                        if isinstance(decode_hex,bytes):
                            self.automatic_time = (len(frame_list)-frame_list_count)/len(frame_list)*100
                        if self.config_save_alldata_s:
                            with open(s_filename,'a+') as f:
                                f.write(receive_data_save+'\n')
                        # 常态毫秒保存
                        if self.config_save_alldata_ms:
                            with open(hz_filename,'a+') as f:
                                f.write(alldata_ms)
                                alldata_ms = ''
                        # 到位分文件秒值保存
                        if (self.config_save_readydata_s==1)&(self.serial_test_begin_flag):
                            try:
                                # bd_file_path_s = '{}{}/'.format(bd_file_path,name)
                                bd_file_path_s = '{}{}/{}/'.format(file_path,name,self.plan_name)
                                if not os.path.exists(bd_file_path_s):
                                    os.makedirs(bd_file_path_s)
                                    self.debug_list_2.append('{} 创建文件夹{}'.format(self.normal_time,bd_file_path_s))
                                    # print(bd_file_path_ms)
                                save_file_name = '{}/{}_BD{}#{}#{}_s.txt'.format(bd_file_path_s,name,self.bd_count,self.bd_test_flag,save_time)
                                with open(save_file_name,'a+') as f:
                                    f.write(receive_data_save+'\n')
                            except Exception as e:
                                self.debug_list_3.append('{}保存readydata_s文件失败:{}'.format(thread_num,e))
                        if (self.config_save_readydata_ms==1)&(self.serial_test_begin_flag):
                            try:
                                # bd_file_path_ms = '{}{}/'.format(bd_file_path,name)
                                bd_file_path_ms = '{}{}/{}/'.format(file_path,name,self.plan_name)
                                if not os.path.exists(bd_file_path_ms):
                                    os.makedirs(bd_file_path_ms)
                                    self.debug_list_2.append('{}创建文件夹{}'.format(self.normal_time,bd_file_path_ms))
                                    # print(bd_file_path_ms)
                                save_file_name = '{}/{}_BD{}#{}#{}_hz.txt'.format(bd_file_path_ms,name,self.bd_count,self.bd_test_flag,save_time)
                                with open(save_file_name,'a+') as f:
                                    f.write(readydata_ms) 
                                    readydata_ms = ''
                            except Exception as e:
                                self.debug_list_3.append('{}保存readydata_ms文件失败:{}'.format(thread_num,e))
                        else:
                            readydata_ms = ''
                        # calib标定保存
                        if self.config_save_alldata_calib:
                            try:
                                with open(calib_filename,'a+') as f:
                                    f.write(alldata_calib)
                                    alldata_calib = ''
                            except:
                                # print('保存alldata_calib文件失败')
                                self.debug_list_3.append('保存all_data_calib文件失败')
                        else:
                            alldata_calib = ''
                            
                        save_data_end_time = time.time()-save_data_begin_time
                        self.lineEdit_debug_message_list[1].append('保存数据耗时:{:.6f}'.format(save_data_end_time))
                        all_save_data_time+=save_data_end_time
                        self.lineEdit_debug_message_list[5].append('保存数据总耗时:{:.6f}'.format(all_save_data_time))

                        if thread_num==0:
                            self.automatic_time =  time.time() - self.threading_begin_time 
                                
                        decode_end_time = time.time()-decode_begin_time
                        self.lineEdit_debug_message_list[4].append('解算耗时:{:.6f}'.format(decode_end_time))
                        all_decode_data_time+=decode_end_time
                        self.lineEdit_debug_message_list[5].append('解算数据总耗时:{:.6f}'.format(all_decode_data_time))


                        
                else:
                    frame_error_count+=1
                    # all_data = all_data[1:]
                    if isinstance(decode_hex,bytes):
                        all_data  =b''.join(frame_list[frame_list_count:])
                        frame_list_count = 0
                    hex_find_hex = all_data.find(decode_rule_header)
                    if hex_find_hex==-1:
                        all_data = b''
                        # self.show_message_automatic_list.append('{} 找不到帧头'.format(self.normal_time))
                        if frame_error_count==1:
                            self.debug_list_4.append('{} 找不到帧头'.format(self.normal_time))
                    elif hex_find_hex==0:
                        all_data = all_data[1:]
                        # print('hex_find_hex:{} len:{} decode_rule_header:{} head:{}'.format(
                        #     hex_find_hex,len(all_data),decode_rule_header,all_data[:6]
                        #     ))
                    else:
                        try:
                            all_data = all_data[hex_find_hex:]
                        except:
                            all_data = all_data[1:]
                    
                    self.debug_list_3.append('{} 找不到帧头 重新排序 all_data:{} '.format(
                        self.normal_time,len(all_data)
                        ))
                    pop_count+=1
                    self.lineEdit_debug_message_list[0].append('帧头错误计数：{}'.format(pop_count))
                    
                    if frame_error_count>decode_fram_leng*2:
                        frame_error_count-=decode_fram_leng*receive_hz*60*5
                        if hex_find_hex==-1:
                            self.debug_list_4.append('{} 找不到帧头'.format(self.normal_time))
                        else:
                            self.debug_list_4.append('{} 找到帧头但长度错误'.format(self.normal_time))
                    
                    frame_list = [ all_data[i*decode_fram_leng:(i+1)*decode_fram_leng] for i in range(len(all_data)//decode_fram_leng) ]
                

                
            else:
                time.sleep(0.001)
                if isinstance(decode_hex,bytes):
                    self.lineEdit_automatic_mode_list.append('解算完成')
                    self.automatic_time = 0 
                    self.threading_test_flag = False
                    self.threading_list_flag[thread_num] = False

                    
    def plan_test_threading(self):
        count =0
        select_plan_name = self.comboBox_automatic_rule.currentText()
        plan_rule_name = './自动规则/{}.txt'.format(select_plan_name)
        try:
            plan_files = pd.read_csv(plan_rule_name,sep='\\s+',header=None,encoding='gb2312')
        except:
            plan_files = pd.read_csv(plan_rule_name,sep='\\s+',header=None,encoding='utf-8')
        max_plan = len(plan_files)-1
        wait_count = 0
        real_time = time.time()
        begin_time = time.time()
        while self.plan_threading_flag:
            time.sleep(0.5)
            try:
                list_plan = list(plan_files.iloc[count])
            except:
                # print(plan_files)
                self.show_message_automatic_list.append('{} 自动测试结束'.format(self.normal_time))
                self.plan_threading_flag = False
                break
            # print(list_plan)
            if list_plan[0].startswith('#'):
                count+=1
            elif list_plan[1]=='wait':
                # print('wait等待时间:{:.2f}'.format(time.time()-real_time))
                self.lineEdit_automatic_mode_list.append('自动模式:等待中')
                if time.time()-begin_time>int(list_plan[2]):
                    count+=1
                    begin_time = time.time()
                else:
                    self.automatic_time = int(list_plan[2])-(time.time()-begin_time)
                    time.sleep(1)
                    wait_count+=1
            elif list_plan[1]=='time':
                clock_time = list_plan[2]
                try:
                    clock_time = datetime.strptime(clock_time,'%H:%M')
                    hour = clock_time.hour
                    minute = clock_time.minute
                except:
                    self.debug_list_1.append('解算到点时刻失败:{}'.format(clock_time))
                    count+=1

                now = datetime.now()
                if now.hour == hour and now.minute == minute:
                    self.debug_list_1.append('time时间:{:.2f} {}'.format(time.time()-real_time,clock_time))
                    count+=1
                else:
                    time.sleep(0.5)
                    wait_count+=1
            elif list_plan[1]=='power':
                count+=1
                print('power电源时间:{:.2f}'.format(time.time()-real_time))
                if 'on' in list_plan[2].lower():
                    self.event_power_on(try_split_power_command(list_plan[2]))
                elif 'off' in list_plan[2].lower():
                    self.event_power_off(try_split_power_command(list_plan[2]))
                    self.plan_name = ''
                # elif 'v' in list_plan[2].lower():
                #     serial_com = self.comboBox_power_com.currentText()
                #     power_serials = serial.Serial(serial_com, 57600)
                #     try:
                #         power_v = float(list_plan[2].split(':')[1])
                #     except:
                #         power_v = 0
                #         self.show_message_automatic_list.append('电压设置错误:{}'.format(list_plan[2]))
                #     power_serials.write(':VOLT:B {}\n'.format(power_v).encode())
                #     power_serials.close()
                # elif 'test' in list_plan[2].lower():
                #     serial_com = self.comboBox_power_com.currentText()
                #     power_serials = serial.Serial(serial_com, 57600)
                #     for i in range(3):
                #         power_v = float(2.5*i)
                #         power_serials.write(':VOLT:B {}\n'.format(power_v).encode())
                #         time.sleep(0.001)
                #     power_serials.close()
                # elif 'step' in list_plan[2].lower():
                #     serial_com = self.comboBox_power_com.currentText()
                #     power_serials = serial.Serial(serial_com, 57600)
                #     steps = int(list_plan[2].split(':')[1])
                #     waits = float(list_plan[2].split(':')[2])
                #     powev = float(list_plan[2].split(':')[3])
                #     for i in range(steps):
                #         power_v = float((powev/steps)*(i+1))
                #         power_serials.write(':VOLT:B {}\n'.format(power_v).encode())
                #         time.sleep(waits)
                #     power_serials.close()
                # else:
                # begin_time = time.time()
                #     print('未知电源命令')
            elif 'bind' in list_plan[1].lower():
                count+=1
                self.binding_send()
                begin_time = time.time()
            elif 'test' in list_plan[1].lower():
                count+=1
                begin_time = time.time()
                if 'on' in list_plan[2].lower():
                            
                    self.save_data_flag = True      # 开启保存
                    self.turntable_ready = True     # 忽略转台/ 转台到位标志位
                    self.auto_plot_always = True    # 持续更新绘图
                    self.only_test()
                    self.debug_list_1.append('{} {}'.format(self.normal_time,'开启测试'))
                elif 'off' in list_plan[2].lower():
                    self.debug_list_1.append('{} {}'.format(self.normal_time,'停止测试'))
                    self.threading_test_flag = False
                else:
                    self.debug_list_1.append('{} {} {}'.format(self.normal_time,'未知测试命令',list_plan[2]))

            elif list_plan[1]=='name':
                print('name电源时间:{:.2f}'.format(time.time()-real_time))
                count+=1
                self.plan_name = str(list_plan[2])
                begin_time = time.time()
            elif list_plan[1]=='bd':
                print('bd电源时间:{:.2f}'.format(time.time()-real_time))
                count+=1
                if list_plan[2]=='on':
                    self.threading_test_flag = False
                    time.sleep(0.1)
                    self.threading_test_flag = True
                    time.sleep(0.1)
                    self.turntable_ready = False
                    self.bd_test()
                    begin_time = time.time()
                else:
                    try:
                        bd_name = int(list_plan[2])   
                        self.comboBox_turntable_rule.setCurrentIndex(bd_name)
                        self.threading_test_flag = False
                        time.sleep(0.1)
                        self.threading_test_flag = True
                        time.sleep(0.1)
                        self.turntable_ready = False
                        self.bd_test()
                        begin_time = time.time()
                    except Exception as e:
                        # print('设置错误_bd_name')
                        self.show_message_automatic_list.append('{}自动测试错误:{} 错误'.format(self.normal_time,bd_name))
                        self.debug_list_1.append('{}自动测试错误:{} 错误\n{}'.format(self.normal_time,bd_name,e))
            elif list_plan[1]=='temp':
                print('bd电源时间:{:.2f}'.format(time.time()-real_time))
                count+=1
                try:
                    temp_com = self.comboBox_tempbox_com.currentText()
                    temp_serial = serial.Serial(temp_com, 9600)
                    temp_commands = 'TEMP,S{}'.format(int(list_plan[2]))
                    temp_serial.write(temp_commands.encode())
                    self.show_message_automatic_list.append('{} 温箱:{}'.format(self.normal_time ,temp_commands))
                except Exception as e:
                    self.show_message_automatic_list.append('{} 错误:{}'.format(self.normal_time,temp_commands))
                    self.debug_list_1.append('{} 设置温箱温度错误:{}\n\t{}'.format(self.normal_time,temp_commands,e))
                temp_serial.close()
            else:
                print('未知控制命令:{}，跳过'.format(list_plan))
                count+=1
               
    def begin_test_bd(self):
        # print('开始转台标定')
        self.show_message_dis1_list.append('{} 开始转台标定'.format(self.normal_time))
        bd_count = 0
        inside_location = 0
        outside_location = 0
        inside_speed = 0
        outside_speed = 0
        inside_acceleration = 20
        outside_acceleration = 20
        
        rec_tt_out_count = 0
        out_time_show_flag = True
        # config_speed = self.config
        waittime = 2
        rule_count =0
        # 等待命令标志位
        send_check=True
        # 可以开始测试标志位
        self.serial_test_begin_flag = False
        begin_time = time.time()
        last_mode = None
        # 读取规则文件
        bd_rulename = './{}/{}.txt'.format('标定规则',self.comboBox_turntable_rule.currentText())
        try:
            rule_file = pd.read_csv(bd_rulename,header=None,skiprows=2,encoding='gb2312',sep='\\s+')
        except:
            rule_file = pd.read_csv(bd_rulename,header=None,skiprows=2,encoding='utf-8',sep='\\s+')
        # print(rule_file)
        com_port = self.comboBox_turntable_com.currentText()
        try:
            turntable_serial = serial.Serial(com_port, 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        except Exception as e:
            self.debug_list_1.append('{} 第一次开启转台串口错误:{}'.format(self.normal_time,e))
            time.sleep(1)
            try:
                turntable_serial = serial.Serial(com_port, 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
            except Exception as e:
                self.debug_list_1.append('{} 第二次开启转台串口错误:{}'.format(self.normal_time,e))


        # 创建保存log文件夹
        now = datetime.now()
        file_path = './测试数据/{}{}/{}/'.format(int2str(now.year),int2str(now.month),int2str(now.day))
        commands = b''
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        # print('转台开启')
        turntable = Turntable_class()
        while (rule_count<len(rule_file)) & self.plan_threading_flag:
            time.sleep(0.5)
            try:
                wait = turntable_serial.in_waiting
                if wait>52:
                    last_commands = turntable_serial.read(wait)
                    commands+=last_commands
                    rec_tt_out_count = 0
                else:
                    rec_tt_out_count+=1
                    if rec_tt_out_count>20:
                        if out_time_show_flag:
                            out_time_show_flag = False
                            self.show_message_automatic_list.append('{} 转台接收已经超时'.format(self.normal_time))
                            self.debug_list_1.append('{} 转台接收已经超时'.format(self.normal_time))
                        else:
                            rec_tt_out_count -= 120+20
                            self.debug_list_1.append('{} 转台接收已经超时'.format(self.normal_time))

                if commands.startswith(b'\xaa\xaa') & (len(commands)>=52):
                    decode_hex = commands[:52]
                    commands = commands[52:]
                    decode_commands = struct.unpack('<HHHIHHiiHiiHiixxxxxxxxxx',decode_hex)
                    decode_commands = list(decode_commands)
                    decode_commands[6]/=1e4
                    decode_commands[7]/=1e4
                    decode_commands[9]/=1e4
                    decode_commands[10]/=1e4
                    i_status = conver_turntable_status(decode_commands[5])
                    o_status = conver_turntable_status(decode_commands[8])
                    turntable_message = '{} 转台解算成功:{}\n\t{}\n\t{}'.format(self.normal_time,decode_commands,i_status,o_status)
                    # self.debug_list_1.append(turntable_message) 
                    try:
                        with open(file_path+'运行记录_转台解算.txt','a+') as f:
                            f.write(turntable_message)
                    except Exception as e:
                        self.debug_list_4.append('{} 写入文件失败 {}'.format(self.normal_time,e))
                    self.inside_location = decode_commands[6]
                    self.inside_speed = decode_commands[7]
                    self.outside_location = decode_commands[9]
                    self.outside_speed = decode_commands[10]
                    self.turntable_i_status = i_status    # 转台运动状态
                    self.turntable_o_status = o_status    # 转台运动状态
            except:
                self.debug_list_2.append('{} 解算失败:{} {}'.format(self.normal_time,decode_hex.hex(),e))
            # '''
            i=rule_count
            if send_check:
                # print(rule_file[:][i])
                send_check=False
                try:
                    bd_count = int(rule_file[0][i])
                    self.bd_count = bd_count
                    inside_location=float(rule_file[1][i])
                    outside_location=float(rule_file[2][i])
                    inside_speed=float(rule_file[3][i])
                    outside_speed=float(rule_file[4][i])
                    test_time = int(rule_file[5][i])
                except Exception as e:
                    self.debug_list_1.append('{} 读取转台转台标定文件错误：{}'.format(self.normal_time,bd_rulename))
                last_mode = 'spd'
                if (inside_speed==0)&(outside_speed==0):
                    # 转台固定 方位模式
                    turntable.inside_location(inside_location,self.config_in_spd,self.config_in_acc)
                    turntable.outside_location(outside_location,self.config_out_spd,self.config_out_acc)
                    last_mode = 'loc'
                elif (outside_speed==0):
                    # 内框旋转模式
                    turntable.inside_speed(inside_speed,self.config_in_acc)
                    turntable.outside_location(outside_location,self.config_out_spd,self.config_out_acc)
                elif (inside_speed==0):
                    # 外框旋转模式
                    turntable.inside_location(inside_location,self.config_in_spd,self.config_in_acc)
                    turntable.outside_speed(outside_speed,self.config_out_acc)
                else:
                    # 内外旋转
                    turntable.inside_speed(inside_speed,self.config_in_acc)
                    turntable.outside_speed(outside_location,self.config_out_acc)
                    
                self.bd_test_flag = '{}[{}_{}_{}_{}]'.format(last_mode,inside_location,outside_location,inside_speed,outside_speed)
                self.show_message_dis1_list.append('{} {}:{}'.format(self.normal_time,bd_count,self.bd_test_flag))
                message = turntable.get_command()
                turntable_serial.write(bytes.fromhex(message))
                # 转动等待时间
                waittime = test_time+1
            # 转台到位开始收数判断
            if (time.time()-begin_time>self.config_hold_time)& (not self.serial_test_begin_flag):
                if self.config_turntable_check_status:
                    turntable_readt_list = [
                        abs(inside_location-decode_commands[6])<1,
                        abs(inside_speed-decode_commands[7])<1,
                        abs(outside_location-decode_commands[8])<1,
                        abs(outside_speed-decode_commands[9])<1,
                    ]
                    if (False not in turntable_readt_list) & ('到位' in i_status) &('到位' in o_status):
                        self.debug_list_1.append('{} 转台到位'.format(self.normal_time))
                        self.serial_test_begin_flag = True
                        self.turntable_ready = True
                        self.show_message_dis2_list.append('{} 开始陀螺收数'.format(self.normal_time))
                        self.turntable_will_turn = False
                        self.bd_calib_flag = 0
                    else:
                        if ('到位' in i_status) &('到位' in o_status):
                            self.debug_list_1.append('{} 转台提示到位但与指令不符，尝试重新发送指令 {}'.format(self.normal_time,self.bd_test_flag))
                            turntable_serial.write(bytes.fromhex(message))
                            time.sleep(0.5)
                        else:
                            self.debug_list_1.append('{} 转台未到位 继续等待中...'.format(self.normal_time))
                            time.sleep(1)
                else:
                    self.serial_test_begin_flag = True
                    self.turntable_ready = True
                    self.show_message_dis2_list.append('{} 转台已稳定 开始收数中...'.format(self.normal_time))
                    self.turntable_will_turn = False
                    self.bd_calib_flag = 0
            # 即将转位标志位 用于calib生成
            if (time.time()-begin_time>waittime+self.config_hold_time-1)&(rule_count<len(rule_file)-1):
                self.turntable_will_turn = True
                self.bd_calib_flag = 1
            if time.time()-begin_time>waittime+self.config_hold_time:
                # print('一组测试结束')
                # 刹车指令
                if self.config_turntable_check_status:
                    message = 'aaaa555538000100800000000000000000000000008000000000000000000000000000000000000000000000000000ff000000ffffffff34'
                    if ('停止' in i_status) &('停止' in o_status):
                        self.show_message_dis2_list.append('{} 刹车已稳定 进行下一步...'.format(self.normal_time))
                        begin_time = time.time()
                        send_check = True
                        rule_count+=1
                    elif (time.time()-begin_time ) < (waittime+ 2*self.config_hold_time):
                        self.show_message_dis2_list.append('{} 测试已结束 自动刹车中...'.format(self.normal_time))
                        turntable_serial.write(bytes.fromhex(message))
                        time.sleep(1)
                        turntable_serial.write(bytes.fromhex(message))
                        time.sleep(self.config_hold_time)
                    else:
                        self.show_message_dis2_list.append('{} 刹车未稳定 继续刹车中...'.format(self.normal_time))
                        turntable_serial.write(bytes.fromhex(message))
                        time.sleep(1)
                        

                #     try:
                #         commands = turntable_serial.readlines()
                #         decode_commands = struct.unpack('>HHHIHHiiHiiHiixxxxxxxxxx',commands)
                #         self.show_message_dis1_list.append('解算成功:{}'.format(decode_commands))
                #     except:
                #         self.show_message_dis1_list.append('解算失败:{}'.format(commands))
                #         continue
                #     self.show_message_dis1_list.append(str(decode_commands))
                #     in_status = bin(decode_commands[5])[2:].rjust(16,'0')[6]
                #     ou_status = bin(decode_commands[8])[2:].rjust(16,'0')[6]
                #     self.show_message_dis1_list.append('内环状态:{} 外环状态:{}'.format(in_status,ou_status))
                #     if (str(in_status)=='1')&(str(ou_status)=='1'):
                #         time.sleep(1)
                #         begin_time = time.time()
                #         send_check = True
                #         rule_count+=1
                #     else:
                #         continue
                    
                else:
                    self.show_message_dis2_list.append('{} 测试已结束 自动刹车中...'.format(self.normal_time))
                    self.serial_test_begin_flag = False
                    message = 'aaaa555538000100800000000000000000000000008000000000000000000000000000000000000000000000000000ff000000ffffffff34'
                    turntable_serial.write(bytes.fromhex(message))
                    time.sleep(1)
                    turntable_serial.write(bytes.fromhex(message))
                    time.sleep(self.config_hold_time+1)
                    begin_time = time.time()
                    send_check = True
                    rule_count+=1
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
# 根据转台状态字返回对应内容 待更新
def conver_turntable_status(hex_data):
    status_list1 = ['位置','速率','摇摆','阶跃','仿真','方波','三角','梯形','找零','停车']
    status_list2 = ['停止','运动']
    status_list3 = ['未闭','闭环']
    status_list4 = ['未到','到位']
    status_list5 = ['正常','异常']
    status_list6 = ['锁紧','跟随','超速','驱动','限位','使能']
    status_list7 = ['远控','未控']
    status_list8 = ['校验','未校']
    status_list = [status_list1,status_list2,status_list3,status_list4,status_list5,status_list6,status_list7,status_list8]

    try:
        bin_data = format(hex_data,'016b')
        result_list = []
        for i in range(8):
            if i==0:
                beg = -4
                end = None
            else:
                beg = -4-i
                end = beg+1
            # print('status_list%s,'%(i+1),end='')
            try:
                counts = int(bin_data[beg:end],2)
                # print(status_list[i][counts])
                result_list.append(status_list[i][counts])
            except Exception as e:
                result_list.append('未知')
                self.debug_list_1.append('{} 解算转台状态错误{} {}'.format(self.normal_time,hex_data,e))
        
        return ' '.join(result_list)

    except Exception as e:
        self.debug_list_1.append('{} conver_turntable_status函数错误{} {}'.format(self.normal_time,hex_data,e))
        return 'conver_error: {} {}'.format(hex_data,'未知')
def lat_lon2str(float_data):
    float_data = float(float_data)
    int_data = int(float_data)
    frac_data = float_data - int_data
    return (int_data+frac_data*0.6)*100
    
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
def calculate_xorsum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum & 0xFF 
# 按规则列表转换十六进制原始数
def decode_hex_frame_list(frame,decode_rule_list,decode_save_list,decode_para_list,decode_sort_list,decode_edia_list,config_sum_check=None):
    decode_data_list = []
    decode_struct_tolegth = 0
    try:
        if config_sum_check is not None:
            checks = calculate_checksum(frame[config_sum_check[1],config_sum_check[2]])
            if checks==frame[config_sum_check[0]][0]:
                sum_check_result = 1
            else:
                sum_check_result = 0
        else:
            sum_check_result = 1
    except Exception as e:
        sum_check_result = 0
        print('校验失败:{}'.format(e))
    for i in range(len(decode_edia_list)):
        decode_bit_list = []
        decode_struct = decode_edia_list[i]+''.join(decode_rule_list[i])
        decode_struct_length =struct.calcsize(decode_struct)
        # decode_tuple = list(struct.unpack(decode_struct,frame[decode_struct_tolegth:decode_struct_length]))
        try:
            decode_tuple = list(struct.unpack(decode_struct,frame[decode_struct_tolegth:decode_struct_tolegth+decode_struct_length]))
            # for errors in decode_tuple:
            #     if float(errors)>100000000:
            #         print(errors)
            #         print(frame[decode_struct_tolegth:decode_struct_tolegth+decode_struct_length].hex())
            #         print(decode_struct)
        except:
            print('decode_struct:{}'.format(decode_struct))
            print('decode_struct_length:{}'.format(decode_struct_length))
            print('decode_hex_frame_list')
            print(decode_struct)
            print(frame.hex())
            print('decode_struct_tolegth:{}  decode_struct_length:{}'.format(decode_struct_tolegth,decode_struct_length))
            print(frame[decode_struct_tolegth:decode_struct_length])
        decode_struct_tolegth += decode_struct_length
        for j in range(len(decode_tuple)):
            try:
                decode_sort_num = decode_sort_list[i].index(str(j))
            except:
                print('decode_hex_frame_list:排序序号超出列表长度')
                print('decode_tuple:{}'.format(decode_tuple))
                print('decode_sort_list[i]:{} index:{}'.format(decode_sort_list[i],j))
                continue
            if decode_save_list[i][decode_sort_num]=='1':
                decode_para_num = decode_para_list[i][decode_sort_num]
                # if (decode_para_num=='1')|(decode_para_num==1)|(round(float(decode_para_num),2)==1):
                if round(float(decode_para_num),12)==1:
                    decode_bit_list.append(decode_tuple[decode_sort_num])
                else:
                    decode_bit_list.append(decode_tuple[decode_sort_num]*float(decode_para_num))
        decode_data_list+=decode_bit_list
    return decode_data_list,sum_check_result
def try_split_power_command(strings):
    if ('on' in strings)|('off' in strings):
        if ':' in strings:
            try: return int(strings.split(':')[1])
            except: return 'all'
        elif '：' in strings:
            try: return int(strings.split('：')[1])
            except: return 'all'
        else:
            return 'all'
    else:
        return 'all'

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
