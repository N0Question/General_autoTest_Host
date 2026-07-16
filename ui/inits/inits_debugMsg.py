# 初始化调试信息结构体
class MainWindowInitDebugMsg:
    def __init__(self, mw):
        self.mw = mw
        # 调试信息列表_多设备控制
        self.mw.debugMsgList_devide = []
        self.init_debugMsg_list()
        
    def init_debugMsg_list(self):
        self.mw.debugMsgList_devide.append('调试信息:多设备控制')