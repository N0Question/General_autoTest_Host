# 各类点击事件
class MainWindowEvent:
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow
        # self.mainWindow.pushButton_debug_2.clicked.connect(self.clkEvent_pushbutton2)
        # self.event_clk_count = 0


# ------------------接收转发/卫导数据接收&转发--------------
    


    # def clkEvent_pushbutton2(self):
    #     self.event_clk_count+=1
    #     self.mainWindow.textBrowser_debug_4.append('{} {} click enent'.format( self.mainWindow.normal_time ,'clkEvent_pushbutton2' ))
    #     self.mainWindow.clk_couts+=1
    #     self.mainWindow.new_constants.append(self.event_clk_count)
    #     print('{} {}'.format( self.mainWindow.clk_couts,self.mainWindow.new_constants ))




# ------------------接收转发/卫导数据接收&转发--------------
    def clkEvent_recforward_all(self):
        checked = self.mainWindow.checkBox_recforward_all.isChecked()
        for checkbox in self.mainWindow.init_ui.recforward_check_list:
            checkbox.setChecked(checked)

    def changeEvent_recforward(self):
        recforward_text = self.mainWindow.textEdit_recforward_msg.toPlainText()
        print(recforward_text)
        rf_list = recforward_text.split(',')
