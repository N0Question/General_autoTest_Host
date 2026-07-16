# 初始化显示信息列表
global_msg = '''处理标定数据：
0.（可选）点击<载入路径>，选择 [路径]，查看 [路径] 下的所有文件
    右侧实时点击的图片、表格、文字信息
1.在{基础处理_参数}中设置正则表达式及各项参数
    正则：预览及处理文件时匹配的正则表达式
    序号：陀螺、加表、温度代表的列序号(从0开始)
    系数：陀螺、加表、温度处理时的系数，计算时单位：°/h、m/s²、℃
    平均：平均时取整数圈
    转换：格式转换时将平均值重复行数
    精度：保存文件时小数点后位数
    排序：拟合时使用list[0]分隔，list[1]排序
    标度：定值温度点时不同速率点的拟合阶数
    全温：全温温度点时定值标度的拟合阶数
2.点击<数据处理>，选择 [选择路径]/[测试项目]/[测试文件]，如：
    [当前路径] / [[BD_-40]......[BD_60]] / [loc1_s.txt......spd10_hz,txt]
    对所有文件取使用参数均值，保存到 [选择路径]/[all_ave]/ 文件夹中
    对所有文件计算零片稳定性，保存到 [选择路径]/[all_std]/ 文件夹中
3.点击<格式转换>，选择路径同上，适配matlab处理
    对所有[all_ave]文件夹中的文件进行格式转换，重复多行，后续使用matlab处理
    保存到 [选择路径]/[all_format]/ 文件夹中
4.点击<计算参数>，选择路径同上，计算标定参数
    对所有[all_format]文件夹中的文件进行参数计算
    保存到 [选择路径]/[all_para]/ 文件夹中
    零位、正负G、正负标度、非线性度、非正交角、温度
5、点击<拟合曲线>，选择路径同上，拟合标定曲线
    对所有[all_para]文件夹中的文件进行全温曲线拟合
    保存到 [选择路径]/[all_polyfit]/ 文件夹中
    输出：拟合曲线图、拟合参数、拟合误差
—————————————————————————
'''
class MainWindowInitShowMsg:
    def __init__(self, mw):
        self.mw = mw
        self.mw.showMsgList_devide = []
        self.init_showMsg_process()
    # 流程简介信息
    def init_showMsg_process(self):
        msg = global_msg
        self.mw.textBrowser_tools_bd3x_msgShow.setText(msg)
        # 第一行加粗
        cursor = self.mw.textBrowser_tools_bd3x_msgShow.textCursor()
        cursor.movePosition(cursor.Start)
        cursor.select(cursor.LineUnderCursor)
        fmt = cursor.charFormat()
        fmt.setFontWeight(75)  # 75表示加粗
        cursor.setCharFormat(fmt)
        cursor.clearSelection()
        self.mw.textBrowser_tools_bd3x_msgShow.setTextCursor(cursor)
        # self.mw.textBrowser_tools_bd3x_msgShow.moveCursor(cursor.Start)
        