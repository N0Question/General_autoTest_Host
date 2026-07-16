# 全局变量控制模块
import os
from datetime import datetime
class MainWindowConstants:
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow

        self.init_load_path()


        self.mainWindow.new_constants = []
        self.mainWindow.clk_couts = 0

    # 初始化载入文件全局变量
    def init_load_path(self):
        now = datetime.now()
        oscwd = os.getcwd()
        file_path = './测试数据/{:02d}{:02d}/{:02d}/'.format(now.year,now.month,now.day)

        if os.path.exists(file_path):
            self.load_filepath = file_path
        else:
            self.load_filepath = os.getcwd()