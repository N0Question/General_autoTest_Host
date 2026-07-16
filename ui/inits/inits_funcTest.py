import configparser
import uuid
import hashlib
from pathlib import Path
from PyQt5.QtWidgets import QGroupBox,QApplication,QWidget,QComboBox
class MainWindowInitFuncTest:
    def __init__(self,mainWindow):
        self.mw = mainWindow
        self.filepath = './配置文件/functest_config.ini'
        self.vip_dict = {}
        self.uuid = self.get_uuid()
        self.init_load_setting()
        self.load_config()
        self.clickLogic_bykey()
        
    def get_uuid(self):
        mac = uuid.getnode()
        return ':'.join(('%012X'%mac)[i:i+2] for i in range(0,12,2))
    def load_config(self):
        config = configparser.ConfigParser()
        config.optionxform = str  # 保留大小写
        try:
            with open(self.filepath, encoding="gb2312") as f:
                config.read_file(f)
        except UnicodeDecodeError:
            try:
                with open(self.filepath, encoding="utf-8", errors="ignore") as f:
                    config.read_file(f)
            except Exception as e:
                return False
        if 'groupBox' in config:
            self.vip_dict = config.items('groupBox')
    def clickLogic_bykey(self):
        list_logic_groupbox = [
            'groupBox_tools_bd3x_test',
            'groupBox_tools_bd3x_allpara',
        ]
        list_logic_combobox = [
            'comboBox_tools_bd3x_preset'
        ]
         # 初始化所有groupbox不可用
        for groupname in list_logic_groupbox:
            groupbox = self.mw.findChild(QGroupBox, groupname)
            if groupbox:
                # key = hashlib.md5((groupname + self.uuid + 'yhc2025hashkey').encode("utf-8")).hexdigest()
                # if (groupname in dict(self.vip_dict)) & (key == dict(self.vip_dict)[groupname]):
                groupbox.toggled.connect(self.clickEvent_childHidden)
                groupbox.setEnabled(True)
                groupbox.setChecked(False)
                # else:
                #     groupbox.setEnabled(False)
                #     groupbox.setChecked(False)
                #     self.groupbox_child_hidden(groupbox,False)
            else:
                print('clickLogic_bykey 没有找到界面ID:{}'.format(groupname))
        # 初始化所有combobox不可用
        for comboname in list_logic_combobox:
            combobox = self.mw.findChild(QComboBox, comboname)
            if combobox:
                # key = hashlib.md5((comboname + self.uuid + 'yhc2025hashkey').encode("utf-8")).hexdigest()
                # if (comboname in dict(self.vip_dict)) & (key == dict(self.vip_dict)[comboname]):
                combobox.setEnabled(True)
                # else:
                #     combobox.setEnabled(False)
            else:
                print('clickLogic_bykey 没有找到界面ID:{}'.format(comboname))
            
    
    def clickEvent_childHidden(self,checked):
        sender = self.mw.sender()
        for child in sender.findChildren(QWidget):
            if child is not sender:
                child.setVisible(checked)
    def groupbox_child_hidden(self,groupbox:QGroupBox,checked:bool):
        for child in groupbox.findChildren(QWidget):
            if child is not groupbox:
                child.setVisible(checked)            
    
    # 初始化是否显示某些界面 root开放
    def init_load_setting(self):
        mac_uuid = self.get_uuid()
        self.mw.lineEdit_debug_6.setText('UUID:{}'.format( mac_uuid ))
        tabwidget1 = self.mw.tabWidget
        tabwidget_show_list1 = [
            self.mw.tab_para,
            self.mw.tab_debug2
        ]
        tabwidget2 = self.mw.tabWidget_2
        tabwidget_show_list2 = [
            self.mw.tab_navBinding_old
        ]
        flag_show_tab = mac_uuid not in [
            'AE:DC:28:8F:A9:D8',
            '40:EC:99:76:18:CC',
            '40:EC:99:76:18:CF'
        ]
        flag_debug_path = './配置文件/debug_mode.ini'
        flag_debug_mode = not Path(flag_debug_path).is_file()
        if flag_show_tab and flag_debug_mode:   
            for tab in tabwidget_show_list1:
                index = tabwidget1.indexOf(tab)
                if index!=-1:
                    tabwidget1.setTabVisible(index,False)
            for tab in tabwidget_show_list2:
                index = tabwidget2.indexOf(tab)
                if index!=-1:
                    tabwidget2.removeTab(index)
            
        else:
            self.mw.root_mode = True
            print('开发者模式')
            
# # 生成加密密钥
# list_groupbox = [
#     'groupBox_tools_bd3x_test',
#     'groupBox_tools_bd3x_allpara'
# ]
# for i in list_groupbox:
#     key = hashlib.md5(( i + uuids + 'yhc2025hashkey').encode("utf-8")).hexdigest()
#     print('界面ID:{}, key:{}'.format(i,key))