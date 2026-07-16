# 各类逻辑事件
class MainWindowLogic:
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow
        
        self.logic_recforward()

    
    def logic_recforward(self):
        self.mainWindow.textEdit_recforward_msg.textChanged.connect(self.mainWindow.events.changeEvent_recforward)
        self.mainWindow.checkBox_recforward_all.clicked.connect(self.mainWindow.events.clkEvent_recforward_all)
