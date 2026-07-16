from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
class MainWindowDebug:
    def __init__(self,mainWindow):
        self.mw = mainWindow
        
        self.debug_time_init()
        self.debug_struct_init()
        
        
    
    def debug_time_init(self):
        # 初始化1s调试事件
        self.debug_counts_1s = 0
        self.debug_qtimer_1s = QTimer(self.mw)
        self.debug_qtimer_1s.timeout.connect(self.debug_message_1s)
        self.debug_qtimer_1s.start(1000)
            
    def debug_struct_init(self):
        self.struct_debug_list = []
        self.debug_name_list = ['constants','logic','event','struct']
        for debug_name in self.debug_name_list:
            self.struct_debug_list.append(struct_debug(self.mw,debug_name))
    
    
    def debug_message_1s(self):
        pass
    
    
class struct_debug:
    def __init__(self,mw,debugname):
        # 标志位
        self.debug_name = debugname
        self.init_ready = False
        self.debug_checkOut = False
        self.debug_onlyLast = False
        self.debug_msgList = []
        self.debug_count = 0
        # ui
        self.ui_tbrowser_out = None
        self.ui_check_out = None
        self.ui_check_last = None
        self.ui_lcd_count = None
        self.update_ui_link()
        self.update_ui_list()
        
        
    def update_ui_link(self):
        try:
            self.init_ready = True
            self.ui_tbrowser_out = mw.findChild(QtWidgets.QTextBrowser,'textBrowser_debugMode_{}'.format(debugname))
            self.ui_check_out = mw.findChild(QtWidgets.QCheckBox,'checkBox_debugMode_{}'.format(debugname))
            self.ui_check_last = mw.findChild(QtWidgets.QCheckBox,'checkBox_debugMode_{}'.format(debugname))
            self.ui_lcd_count = mw.findChild(QtWidgets.QLCDNumber,'lcdNumber_debugMode_{}'.format(debugname))
            for ui in self.ui_list:
                if not ui :
                    self.init_ready = False
        except Exception as e:
            self.init_ready = False
            if self.ui_tbrowser_out:
                try:
                    self.ui_tbrowser_out.append('fun:<struct_debug>,初始化失败:{}'.format(e))
                except Exception as e2:
                    print('fun:<struct_debug>,初始化失败:{}\n显示失败:{}'.format(e,e2)) 
        self.update_ui_list()
    def update_ui_list(self):
        if self.init_ready:
            self.ui_list = []
            self.ui_list.append(self.ui_tbrowser_out)
            self.ui_list.append(self.ui_check_out)
            self.ui_list.append(self.ui_check_last)
            self.ui_list.append(self.ui_lcd_count)
            
    def get_check_out(self):
        if self.init_ready:
            self.debug_checkOut = self.ui_check_out.isChecked()
        else:
            self.debug_checkOut = False
        return self.debug_checkOut
    # def get_check_
            