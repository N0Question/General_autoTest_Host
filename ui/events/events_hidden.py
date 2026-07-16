from PyQt5.QtWidgets import QApplication,QWidget
class MainWindowEventHidden:
    def __init__(self, mainWindow):
        self.mw = mainWindow
        self.logic_clickHidden()
        self.logic_changeHidden()
        self.init_hidden()
    
    # groupbox 点击隐藏 
    def logic_clickHidden(self):
        groupbox_list = [
            self.mw.groupBox_sate_config,
            self.mw.groupBox_sate_config_2,
            self.mw.groupBox_sate_show,
            self.mw.groupBox_turntable,
            self.mw.groupBox_turntable3x,
            self.mw.groupBox_tools_calibbd_basepara,
            self.mw.groupBox_tools_bd3x_plotSetting,
            self.mw.groupBox_tools_bd3x_previewSetting,
            self.mw.groupBox_sateSimulation_1,
            self.mw.groupBox_sateSimulation_2,
            self.mw.groupBox_sateSimulation_3,
        ]
        for groupbox in groupbox_list:
            groupbox.toggled.connect(self.clickEvent_childHidden)
            
        
        
    def init_hidden(self):
        default_hidden_list = [
            self.mw.groupBox_turntable3x,
            self.mw.groupBox_tools_calibbd_basepara,
            self.mw.groupBox_tools_bd3x_plotSetting,
            self.mw.groupBox_tools_bd3x_previewSetting,
            self.mw.groupBox_sateSimulation_3,
            self.mw.groupBox_sate_config,
            self.mw.groupBox_sate_config_2,
            self.mw.groupBox_sate_show, 
        ]
        for groupbox in default_hidden_list:
            groupbox.setChecked(False)
        
        
    def clickEvent_childHidden(self,checked):
        sender = self.mw.sender()
        for child in sender.findChildren(QWidget):
            if child is not sender:
                child.setVisible(checked)
                
    def logic_changeHidden(self):
        self.mw.comboBox_general_rule.currentTextChanged.connect(self.changeEvent_buttonHidden)
    def changeEvent_buttonHidden(self):
        text = self.mw.comboBox_general_rule.currentText()
        if text in [
            '选择协议','None',''
        ]:
            self.mw.widget_quickButton.setVisible(False)
        else:
            self.mw.widget_quickButton.setVisible(True)
            