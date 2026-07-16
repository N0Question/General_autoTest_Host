import configparser
from pathlib import Path

class MainWindowInitIni:
    def __init__(self,mainWindow):
        self.mw = mainWindow
        self.list_debug_msg = []
        self.load_ini_debug_mode()
        self.event_load_ini_debug_mode()
        self.load_ini_ui_config()
        
        
    def load_ini_debug_mode(self):
        filepath = './配置文件/debug_mode.ini'
        if not Path(filepath).is_file():
            self.list_debug_msg.append('load_ini_debug_mode 配置文件不存在:{}'.format(filepath))
            self.mw.debug_mode = False
        else:
            self.mw.debug_mode = True
            self.list_debug_msg.append('load_ini_debug_mode 检测到debug_mode配置文件,已启用root模式')
        
    def event_load_ini_debug_mode(self):
        tabwidget1 = self.mw.tabWidget
        tabwidget_show_list1 = [
            self.mw.tab_para,
            self.mw.tab_debug1,
            self.mw.tab_debug2
        ]
        tabwidget2 = self.mw.tabWidget_2
        tabwidget_show_list2 = [
            self.mw.tab_navBinding_old
        ]
        if not self.mw.debug_mode:
            for tab in tabwidget_show_list1:
                index = tabwidget1.indexOf(tab)
                if index!=-1:
                    tabwidget1.setTabVisible(index,False)
            for tab in tabwidget_show_list2:
                index = tabwidget2.indexOf(tab)
                if index!=-1:
                    tabwidget2.removeTab(index)
            
        
    def load_ini_ui_config(self):
        filepath = './配置文件/ui_config.ini'
        if not Path(filepath).is_file():
            self.list_debug_msg.append('load_ini_ui_config 配置文件不存在:{}'.format(filepath))
        try:
            config = configparser.ConfigParser()
            with open(filepath, 'r', encoding='gb2312', errors='ignore') as f:
                config.read_file(f)
        except Exception as e:
            config = None
            self.list_debug_msg.append('load_ini_ui_config 配置文件读取错误:{}'.format(e))
        try: config_ui = config['UI_Display']
        except: config_ui = None
        # 背景颜色
        try: self.config_background_color = config_ui.get('background_color')
        except: self.config_background_color = "#000000"
        # 线条粗细
        try:self.config_line_width = int(config_ui.get('line_width'))
        except: self.config_line_width = 1
        # 主轴颜色
        try:self.config_main_line_color = config_ui.get('main_line_color')
        except: self.config_main_line_color = "#FFFF00"
        # 副轴颜色
        try:self.config_auxiliary_line_color = config_ui.get('auxiliary_line_color')
        except: self.config_auxiliary_line_color = "#00FF00"
        # 网格透明度
        try:self.config_grid_alpha = float(config_ui.get('grid_alpha'))
        except:self.config_grid_alpha = 0.8
        # 标题大小
        try:self.config_title_size = '{}pt'.format(int(config_ui.get('title_size')))
        except:self.config_title_size = '12pt'
        # 标题颜色
        try:self.config_title_color = config_ui.get('title_color')
        except:self.config_title_color = "#FFFFFF"
        # 轨迹视图背景颜色
        try:self.config_trace_background_color = config_ui.get('trace_background_color')
        except:self.config_trace_background_color = "#FFFFFF"
        # 轨迹点颜色
        try:self.config_trace_color = config_ui.get('trace_color')
        except:self.config_trace_color = "#FF0000"
        # 轨迹点大小
        try:self.config_trace_point_size = int(config_ui.get('trace_point_size'))
        except:self.config_trace_point_size = 4
        # 轨迹点透明度
        try:self.config_trace_point_alpha = int(config_ui.get('trace_point_alpha'))
        except:self.config_trace_point_alpha = 180
        # 轨迹终点颜色
        try:self.config_trace_end_color = config_ui.get('trace_end_color')
        except:self.config_trace_end_color = "#FF0000"
        # 轨迹起点颜色
        try:self.config_trace_start_color = config_ui.get('trace_start_color')
        except:self.config_trace_start_color = "#00FF00"
        # 轨迹起终点大小
        try:self.config_trace_endpoint_size = int(config_ui.get('trace_endpoint_size'))
        except:self.config_trace_endpoint_size = 8
        
        