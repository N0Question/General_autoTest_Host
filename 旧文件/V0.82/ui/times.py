from PyQt5.QtCore import QThread, pyqtSignal, QTimer

class MainWindowTimes:
    def __init__(self,mainWindow):
        self.mw = mainWindow
        
        self.test_count = 0
        self.update_test_time()
        
    def update_test_time(self):
        self.test_time = QTimer(self.mw)
        self.test_time.timeout.connect(self.timeEvent_test)
        self.test_time.start(1000)
        
        
        
    def timeEvent_test(self):
        self.test_count+=1
        # print('test:{}'.format(self.test_count))
        pass