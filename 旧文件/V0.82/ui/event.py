import os
# 各类点击事件
class MainWindowEvent:
    def __init__(self,mainWindow):
        self.debug_flag_event = False
        self.mw = mainWindow


# ------------------接收转发/卫导数据接收&转发 开发中--------------
    def clkEvent_recforward_all(self):
        checked = self.mw.checkBox_recforward_all.isChecked()
        for checkbox in self.mw.init_ui.recforward_check_list:
            checkbox.setChecked(checked)

    def changeEvent_recforward(self):
        recforward_text = self.mw.textEdit_recforward_msg.toPlainText()
        print(recforward_text)
        rf_list = recforward_text.split(',')



# ------------------通用装订逻辑事件 开发中--------------
    # 更新装订规则事件
    def changeEvent_general_rule(self):
        # print('changeEvent_general_rule事件：{}'.format(self.mw.comboBox_general_rule.currentText()))
        try:
            filename = './装订规则/{}.txt'.format(self.mw.comboBox_general_rule.currentText())
            if os.path.exists(filename):
                with open(filename,'r+') as f:
                    bind_rule_file = f.read()
                self.mw.struct_general_bind.read_struct_file(filename)
                return True
            else:
                return False
        except Exception as e:
            # print('更新装订规则失败:{}'.format(e))
            return False
        # self.mainWindow.read_binding()
        

# -----------------12路设置模块事件-----------------
    # com口更新逻辑 涉及com定时更新逻辑 若加入同步，逻辑不清晰 废弃中
    def changeEvent_com_update_all(self):
        pass
        # setting = self.mw.constants.structList_12tab[0].com.currentIndex()
        # for i in range(12):
        #     self.mw.constants.structList_12tab[i+1].set_baund(setting)
    def changeEvent_baund_update_all(self):
        setting = self.mw.constants.structList_12tab[0].baund.currentText()
        for i in range(12):
            self.mw.constants.structList_12tab[i+1].set_baund(setting)
    def changeEvent_check_update_all(self):
        setting = self.mw.constants.structList_12tab[0].check.currentText()
        for i in range(12):
            self.mw.constants.structList_12tab[i+1].set_check(setting)
    def changeEvent_stop_update_all(self):
        setting = self.mw.constants.structList_12tab[0].stop.currentText()
        for i in range(12):
            self.mw.constants.structList_12tab[i+1].set_stop(setting)
    def changeEvent_open_update_all(self):
        setting = self.mw.constants.structList_12tab[0].open.text()
        for i in range(12):
            self.mw.constants.structList_12tab[i+1].set_open(setting)
    def changeEvent_plan_update_all(self):
        setting = self.mw.constants.structList_12tab[0].plan.text()
        for i in range(12):
            self.mw.constants.structList_12tab[i+1].set_plan(setting)
    def changeEvent_open_switch(self,tab):
        self.mw.constants.structList_12tab[tab].switch_open()
    # 主控串口设定同步更新总控
    def changeEvent_baund_update_main(self):
        self.mw.constants.structList_12tab[0].set_baund(self.mw.comboBox_protocal_baund.currentText())
    def changeEvent_check_update_main(self):
        self.mw.constants.structList_12tab[0].set_check(self.mw.comboBox_protocal_check.currentText())
            
            
# ---------------卫导接收事件-----------------
    def changeEvent_auxsate_com(self):
        self.mw.combox_set_com_13.setCurrentText(self.mw.comboBox_ascii_com.currentText())
    def changeEvent_auxsate_baund(self):
        self.mw.combox_set_baund_13.setCurrentText(self.mw.comboBox_ascii_baund.currentText())
    def changeEvent_auxsate_check(self):
        self.mw.comboBox_set_check_13.setCurrentText(self.mw.comboBox_ascii_check.currentText())