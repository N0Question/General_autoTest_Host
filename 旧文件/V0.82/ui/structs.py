import struct 
import ctypes
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets, QtGui, QtCore







# 结构体 通用装订规则
class struct_general_bind:
    def __init__(self):
        self.struct_path = './'
        self.struct_name = 'general_bind'
        self.struct_format = '<'
        self.struct_packRule = ''
        self.struct_len = 0
        self.struct_dataList = []
        self.struct_packList = []
        self.struct_paraList = []
        self.struct_titlList = []
        self.struct_sumCheck = []
        self.struct_orcCheck = []
        self.struct_debugList = []
        self.struct_debugFlag = False
    def read_struct_file(self,struct_file):
        print('struct_general_bind初始化\nread_struct_file运行')
        print(struct_file[:100])
        # with open(struct_file,'r') as f:
        #     self.struct_data = f.read(self.struct_len)
        #     self.struct_unpack = struct.unpack(self.struct_fmt,self.struct_data)
        #     self.struct_dict = {self.struct_name:self.struct_unpack}
        # return self.struct_dict
      
      
        
class struct_tab_setting:
    def __init__(self,mw,tab=1):
        self.tab = tab  
        self.com = mw.findChild( QtWidgets.QComboBox,'combox_set_com_{}'.format(tab) )
        self.baund = mw.findChild( QtWidgets.QComboBox,'combox_set_baund_{}'.format(tab) )
        self.check = mw.findChild( QtWidgets.QComboBox,'comboBox_set_check_{}'.format(tab) )
        self.stop = mw.findChild( QtWidgets.QComboBox,'comboBox_stopbit_{}'.format(tab) )
        self.open = mw.findChild( QtWidgets.QPushButton,'pushButton_com_open_{}'.format(tab) )
        self.name = mw.findChild( QtWidgets.QLineEdit,'lineEdit_file_names_{}'.format(tab) )
        self.plan = mw.findChild( QtWidgets.QLineEdit,'lineEdit_plan_names_{}'.format(tab) )
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