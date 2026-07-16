from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
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
        self.debug_name_list = ['constants','logic','event','struct','setting','times']
        for debug_name in self.debug_name_list:
            self.struct_debug_list.append(struct_debug(self.mw,debug_name))
    
    
    def debug_message_1s(self):
        for struct_debug in self.struct_debug_list:
            struct_debug.update_ui_msg()
            struct_debug.ui_lcd_count.display(struct_debug.debug_count)
    def debug_test(self):
        try:
            self.mw.textEdit_tools_fileShow.hide()
            pixmap = QPixmap('D:\\Data\\50惯导\\20250729#50GD_2501003\\50惯导全温冷启静态_20250729084322__G.png')
            self.mw.label_tools_imgShow.setPixmap(pixmap)
        except:
            pass
    
    
class struct_debug:
    def __init__(self,mw,debugname):
        self.mw = mw
        # 标志位
        self.debug_name = debugname
        # 结构体初始化完成标志位
        self.init_ready = False
        # 输出调试内容
        self.debug_checkOut = False
        # 每秒输出时仅输出最后一条调试信息，用于大容量调试输出时防止卡顿
        self.debug_onlyLast = False
        # 调试信息
        self.debug_msgList = []
        self.debug_count = 0
        # 全部UI
        self.ui_list = []
        # 单个UI
        self.ui_tbrowser_out = None
        self.ui_check_out = None
        self.ui_check_last = None
        self.ui_lcd_count = None
        # 初始化UI
        self.update_ui_link()
        
        
    def update_ui_link(self):
        try:
            self.init_ready = True
            debugname = self.debug_name
            self.ui_tbrowser_out = self.mw.findChild(QtWidgets.QTextBrowser,'textBrowser_debugMode_{}'.format(debugname))
            self.ui_check_out = self.mw.findChild(QtWidgets.QCheckBox,'checkBox_debugMode_{}'.format(debugname))
            self.ui_check_last = self.mw.findChild(QtWidgets.QCheckBox,'checkBox_debugMode_{}'.format(debugname))
            self.ui_lcd_count = self.mw.findChild(QtWidgets.QLCDNumber,'lcdNumber_debugMode_{}'.format(debugname))
            self.update_ui_list()
            for ui in self.ui_list:
                if not ui :
                    self.init_ready = False
                    self.ui_tbrowser_out.append('fun:<update_ui_link>,<{}>初始化失败:{}'.format(debugname,'UI链接失败'))
            self.ui_tbrowser_out.append('fun:<update_ui_link>,<{}>初始化:<{}>'.format(debugname,self.init_ready))
        except Exception as e:
            self.init_ready = False
            if self.ui_tbrowser_out:
                try:
                    self.ui_tbrowser_out.append('fun:<update_ui_link>,<{}>初始化失败:{}'.format(debugname,e))
                except Exception as e2:
                    print('fun:<update_ui_link>,初始化失败:{}\n显示失败:{}'.format(e,e2)) 
    def update_ui_list(self):
        # 若初始化正常
        if self.init_ready:
            self.ui_list = []
            self.ui_list.append(self.ui_tbrowser_out)
            self.ui_list.append(self.ui_check_out)
            self.ui_list.append(self.ui_check_last)
            self.ui_list.append(self.ui_lcd_count)
        else:
            self.ui_tbrowser_out.append('fun:<update_ui_list>,<{}>初始化失败'.format(self.debug_name))
            
    def get_check_out(self):
        if self.init_ready:
            self.debug_checkOut = self.ui_check_out.isChecked()
        else:
            self.debug_checkOut = False
        return self.debug_checkOut
    def get_check_last(self):
        if self.init_ready:
            self.debug_onlyLast = self.ui_check_last.isChecked()
        else:
            self.debug_onlyLast = False
        return self.debug_onlyLast
    
    def update_ui_msg(self):
        if len(self.debug_msgList)==0:
            return
        if self.get_check_out():
            if self.get_check_last():
                self.ui_tbrowser_out.clear()
            for msg in self.debug_msgList:
                self.ui_tbrowser_out.append(msg)
                self.debug_count += 1
            
    def append_ui_msg(self,msg):
        print(msg)
        # 若msg类型为string
        if isinstance(msg,str):
            self.debug_msgList.append(msg)
        elif isinstance(msg,list):
            for m in msg:
                self.debug_msgList.append(m)
        elif isinstance(msg,dict):
            for m in msg:
                self.debug_msgList.append('{}:{}'.format(m,msg[m]))
        else:
            self.debug_msgList.append('fun:<append_ui_msg>,msg类型错误:<{}>'.format(type(msg)))