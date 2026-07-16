# 各类逻辑事件
from funs.fun_locals import *
import os
class MainWindowGetUI:
    def __init__(self,mainWindow):
        self.mw = mainWindow

    # 获取当前文件路径
    def get_name_pathCombox(self,mode):
        mode_list = locals_model_list
        if isinstance(mode, str):
            for lists in mode_list:
                if mode in lists:
                    mode_index = lists.index(mode)  
        elif isinstance(mode, int):
            mode_index = mode
        else:
            return False
        try:
            paths = self.mw.init_ui.list_comboBox_localPaths[mode_index].currentText()
            names = self.mw.init_ui.list_comboBox_localFiles[mode_index].currentText()
        except Exception as e:
            self.mw.debug.struct_debug_list[5].append_ui_msg('fun:<get_list_pathCombox>,<{}>初始化失败:{}'.format(mode,e))
            return False
        if (len(paths)==0)|(names=='选择路径')|('none'in names.lower()):
            self.mw.debug.struct_debug_list[5].append_ui_msg('fun:<get_list_pathCombox>,<{}>路径未选择'.format(mode))
            return False
        if (len(paths)==0)|(paths=='选择路径')|('none'in paths.lower()):
            f_name = './{}.txt'.format(names)
        else:
            f_name = './{}/{}.txt'.format(paths,names)
        if not os.path.exists(f_name):
            self.mw.debug.struct_debug_list[5].append_ui_msg('fun:<get_list_pathCombox>,<{}>文件不存在:{}'.format(mode,f_name))
            return False
        return f_name
