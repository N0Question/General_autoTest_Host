import os
from PyQt5 import QtWidgets, QtGui, QtCore
from funs.fun_locals import *
from PyQt5.QtCore import QThread, pyqtSignal, QTimer


# 周期消息更新、事件处理
class MainWindowTimes:
    def __init__(self,mainWindow):
        self.mw = mainWindow
        # 规则文件更新 【名称】 【ui名称】 【文件夹名称】
        self.test_count = 0
        self.time_autoSend = QTimer(self.mw)
        # self.time_autoSend.timeout.connect(self.timeEvent_update_combobox)
        self.time_autoSend.start(1000)
        self.update_test_time()
        
    def update_test_time(self):
        self.test_time = QTimer(self.mw)
        self.test_time.timeout.connect(self.timeEvent_test)
        # self.test_time.start(1000)
    

        
        
        
    def timeEvent_test(self):
        self.test_count+=1
        # print('test:{}'.format(self.test_count))
        pass
    
    # 更新事件-扫描文件夹路径 更新规则文件
    def timeEvent_update_combobox(self):
        if (self.mw.sender() is None)|(isinstance(self.mw.sender(),QtWidgets.QComboBox)):
            return False
        for counts in range(self.mw.init_ui.list_comboBox_localLength):
            comboBox_path = self.mw.init_ui.list_comboBox_localPaths[counts]
            comboBox_name = self.mw.init_ui.list_comboBox_localFiles[counts]
            if comboBox_name is None:
                self.mw.debug.struct_debug_list[5].append_ui_msg('未找到对应控件：{} comboBox_{}_name'.format(counts,comboBox_name))
                continue
            if comboBox_path is None:
                self.mw.debug.struct_debug_list[5].append_ui_msg('未找到对应控件：{} comboBox_{}_path'.format(counts,comboBox_path))
            
            file_path = self.mw.init_ui.list_localNames[counts]
            if not os.path.exists(file_path):
                continue
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            # 更新文件夹列表
            path_list = []
            for file_name in os.listdir('./'+file_path):
                if os.path.isdir(file_path+'/'+file_name):
                    path_list.append(file_name)
            
            if len(path_list)==0:
                comboBox_path.clear()
                comboBox_path.addItem('')
            else:
                # 缓存当前文件夹路径
                comboBox_file_list = []
                for count in range(comboBox_path.count()):
                    comboBox_file_list.append(comboBox_name.itemText(count))
                if '选择路径' in comboBox_file_list:
                    comboBox_file_list.remove('选择路径')
                if '' in comboBox_file_list:
                    comboBox_file_list.remove('')
                # 如果文件夹列表有变化，更新文件夹列表
                if not (comboBox_file_list==path_list):
                    select_combo = comboBox_path.currentText()
                    comboBox_path.clear()
                    comboBox_path.addItem('选择路径')
                    for path in path_list:
                        comboBox_path.addItem(path)
                    if select_combo in path_list:
                        comboBox_path.setCurrentText(select_combo)
                    else:
                        comboBox_path.setCurrentIndex(0)
            
            select_path_name = comboBox_path.currentText()
            if not (select_path_name=='选择路径')|(select_path_name==''):
                file_path = file_path+'/'+select_path_name
            
            # 更新文件夹下的文件列表
            file_list = []
            for file_name in os.listdir('./'+file_path):
                if os.path.isdir(file_path+'/'+file_name):
                    continue
                file_name = file_name.split('.txt')[0]
                file_list.append(file_name)
            file_list.sort()
            comboBox_file_list = []
            for count in range(comboBox_name.count()):
                comboBox_file_list.append(comboBox_name.itemText(count))
            if '选择协议' in comboBox_file_list:
                comboBox_file_list.remove('选择协议')
            if '' in comboBox_file_list:
                comboBox_file_list.remove('')
            if not (comboBox_file_list==file_list):
                select_combo = comboBox_name.currentText()
                comboBox_name.clear()
                comboBox_name.addItem('选择协议')
                for path in file_list:
                    comboBox_name.addItem(path)
                if select_combo in file_list:
                    comboBox_name.setCurrentText(select_combo)
                else:
                    comboBox_name.setCurrentIndex(0)
            
        