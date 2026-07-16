# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Automated_testing_sample.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLCDNumber, QLabel, QLayout,
    QLineEdit, QMainWindow, QPushButton, QRadioButton,
    QSizePolicy, QTabWidget, QTextBrowser, QTextEdit,
    QVBoxLayout, QWidget)

from pyqtgraph import GraphicsLayoutWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1268, 1032)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_5 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setSpacing(7)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(self.widget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.widget1 = QWidget(self.groupBox_2)
        self.widget1.setObjectName(u"widget1")
        sizePolicy1.setHeightForWidth(self.widget1.sizePolicy().hasHeightForWidth())
        self.widget1.setSizePolicy(sizePolicy1)
        self.horizontalLayout_2 = QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.comboBox_protocal_com = QComboBox(self.widget1)
        self.comboBox_protocal_com.addItem("")
        self.comboBox_protocal_com.addItem("")
        self.comboBox_protocal_com.setObjectName(u"comboBox_protocal_com")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBox_protocal_com.sizePolicy().hasHeightForWidth())
        self.comboBox_protocal_com.setSizePolicy(sizePolicy2)
        self.comboBox_protocal_com.setMinimumSize(QSize(0, 25))
        self.comboBox_protocal_com.setEditable(True)

        self.horizontalLayout_2.addWidget(self.comboBox_protocal_com)

        self.comboBox_protocal_baund = QComboBox(self.widget1)
        self.comboBox_protocal_baund.addItem("")
        self.comboBox_protocal_baund.addItem("")
        self.comboBox_protocal_baund.addItem("")
        self.comboBox_protocal_baund.addItem("")
        self.comboBox_protocal_baund.setObjectName(u"comboBox_protocal_baund")
        self.comboBox_protocal_baund.setMinimumSize(QSize(0, 25))
        self.comboBox_protocal_baund.setEditable(True)

        self.horizontalLayout_2.addWidget(self.comboBox_protocal_baund)

        self.comboBox_protocal_check = QComboBox(self.widget1)
        self.comboBox_protocal_check.addItem("")
        self.comboBox_protocal_check.addItem("")
        self.comboBox_protocal_check.addItem("")
        self.comboBox_protocal_check.setObjectName(u"comboBox_protocal_check")
        self.comboBox_protocal_check.setMinimumSize(QSize(0, 25))
        self.comboBox_protocal_check.setEditable(False)

        self.horizontalLayout_2.addWidget(self.comboBox_protocal_check)


        self.verticalLayout_2.addWidget(self.widget1)

        self.widget2 = QWidget(self.groupBox_2)
        self.widget2.setObjectName(u"widget2")
        sizePolicy1.setHeightForWidth(self.widget2.sizePolicy().hasHeightForWidth())
        self.widget2.setSizePolicy(sizePolicy1)
        self.horizontalLayout_3 = QHBoxLayout(self.widget2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.widget2)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_11)

        self.comboBox_protocal_rule = QComboBox(self.widget2)
        self.comboBox_protocal_rule.addItem("")
        self.comboBox_protocal_rule.setObjectName(u"comboBox_protocal_rule")
        self.comboBox_protocal_rule.setEditable(True)

        self.horizontalLayout_3.addWidget(self.comboBox_protocal_rule)


        self.verticalLayout_2.addWidget(self.widget2)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.widget3 = QWidget(self.groupBox)
        self.widget3.setObjectName(u"widget3")
        self.horizontalLayout = QHBoxLayout(self.widget3)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.comboBox_turntable_com = QComboBox(self.widget3)
        self.comboBox_turntable_com.addItem("")
        self.comboBox_turntable_com.addItem("")
        self.comboBox_turntable_com.addItem("")
        self.comboBox_turntable_com.addItem("")
        self.comboBox_turntable_com.addItem("")
        self.comboBox_turntable_com.setObjectName(u"comboBox_turntable_com")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBox_turntable_com.sizePolicy().hasHeightForWidth())
        self.comboBox_turntable_com.setSizePolicy(sizePolicy3)
        self.comboBox_turntable_com.setEditable(True)

        self.horizontalLayout.addWidget(self.comboBox_turntable_com)

        self.pushButton_turntable_open = QPushButton(self.widget3)
        self.pushButton_turntable_open.setObjectName(u"pushButton_turntable_open")
        sizePolicy4 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButton_turntable_open.sizePolicy().hasHeightForWidth())
        self.pushButton_turntable_open.setSizePolicy(sizePolicy4)

        self.horizontalLayout.addWidget(self.pushButton_turntable_open)

        self.pushButton_turntable_close = QPushButton(self.widget3)
        self.pushButton_turntable_close.setObjectName(u"pushButton_turntable_close")
        sizePolicy4.setHeightForWidth(self.pushButton_turntable_close.sizePolicy().hasHeightForWidth())
        self.pushButton_turntable_close.setSizePolicy(sizePolicy4)

        self.horizontalLayout.addWidget(self.pushButton_turntable_close)


        self.verticalLayout.addWidget(self.widget3)

        self.widget_3 = QWidget(self.groupBox)
        self.widget_3.setObjectName(u"widget_3")
        self.gridLayout = QGridLayout(self.widget_3)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_outside_location = QLineEdit(self.widget_3)
        self.lineEdit_outside_location.setObjectName(u"lineEdit_outside_location")
        sizePolicy4.setHeightForWidth(self.lineEdit_outside_location.sizePolicy().hasHeightForWidth())
        self.lineEdit_outside_location.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.lineEdit_outside_location, 3, 3, 1, 1)

        self.lineEdit_outside_acceleration = QLineEdit(self.widget_3)
        self.lineEdit_outside_acceleration.setObjectName(u"lineEdit_outside_acceleration")
        sizePolicy4.setHeightForWidth(self.lineEdit_outside_acceleration.sizePolicy().hasHeightForWidth())
        self.lineEdit_outside_acceleration.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.lineEdit_outside_acceleration, 5, 3, 1, 1)

        self.lineEdit_outside_speed = QLineEdit(self.widget_3)
        self.lineEdit_outside_speed.setObjectName(u"lineEdit_outside_speed")
        sizePolicy4.setHeightForWidth(self.lineEdit_outside_speed.sizePolicy().hasHeightForWidth())
        self.lineEdit_outside_speed.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.lineEdit_outside_speed, 4, 3, 1, 1)

        self.pushButton_inside_reset = QPushButton(self.widget_3)
        self.pushButton_inside_reset.setObjectName(u"pushButton_inside_reset")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.pushButton_inside_reset.sizePolicy().hasHeightForWidth())
        self.pushButton_inside_reset.setSizePolicy(sizePolicy5)
        self.pushButton_inside_reset.setMinimumSize(QSize(40, 0))

        self.gridLayout.addWidget(self.pushButton_inside_reset, 6, 0, 1, 1)

        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)

        self.label_6 = QLabel(self.widget_3)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 2, 1, 1)

        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_8 = QLabel(self.widget_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)

        self.lcdNumber_inside_location = QLCDNumber(self.widget_3)
        self.lcdNumber_inside_location.setObjectName(u"lcdNumber_inside_location")
        sizePolicy6 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.lcdNumber_inside_location.sizePolicy().hasHeightForWidth())
        self.lcdNumber_inside_location.setSizePolicy(sizePolicy6)
        self.lcdNumber_inside_location.setMinimumSize(QSize(0, 26))
        self.lcdNumber_inside_location.setSmallDecimalPoint(True)
        self.lcdNumber_inside_location.setDigitCount(5)
        self.lcdNumber_inside_location.setMode(QLCDNumber.Dec)
        self.lcdNumber_inside_location.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_inside_location.setProperty("value", 0.100000000000000)

        self.gridLayout.addWidget(self.lcdNumber_inside_location, 1, 1, 1, 1)

        self.pushButton_outside_reset = QPushButton(self.widget_3)
        self.pushButton_outside_reset.setObjectName(u"pushButton_outside_reset")
        sizePolicy1.setHeightForWidth(self.pushButton_outside_reset.sizePolicy().hasHeightForWidth())
        self.pushButton_outside_reset.setSizePolicy(sizePolicy1)
        self.pushButton_outside_reset.setMinimumSize(QSize(40, 0))

        self.gridLayout.addWidget(self.pushButton_outside_reset, 6, 2, 1, 1)

        self.lcdNumber_outside_location = QLCDNumber(self.widget_3)
        self.lcdNumber_outside_location.setObjectName(u"lcdNumber_outside_location")
        sizePolicy6.setHeightForWidth(self.lcdNumber_outside_location.sizePolicy().hasHeightForWidth())
        self.lcdNumber_outside_location.setSizePolicy(sizePolicy6)
        self.lcdNumber_outside_location.setMinimumSize(QSize(0, 26))
        self.lcdNumber_outside_location.setSmallDecimalPoint(True)
        self.lcdNumber_outside_location.setDigitCount(5)
        self.lcdNumber_outside_location.setMode(QLCDNumber.Dec)
        self.lcdNumber_outside_location.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_outside_location.setProperty("value", 0.100000000000000)

        self.gridLayout.addWidget(self.lcdNumber_outside_location, 1, 3, 1, 1)

        self.lcdNumber_inside_speed = QLCDNumber(self.widget_3)
        self.lcdNumber_inside_speed.setObjectName(u"lcdNumber_inside_speed")
        sizePolicy6.setHeightForWidth(self.lcdNumber_inside_speed.sizePolicy().hasHeightForWidth())
        self.lcdNumber_inside_speed.setSizePolicy(sizePolicy6)
        self.lcdNumber_inside_speed.setMinimumSize(QSize(0, 26))
        self.lcdNumber_inside_speed.setSmallDecimalPoint(True)
        self.lcdNumber_inside_speed.setDigitCount(5)
        self.lcdNumber_inside_speed.setMode(QLCDNumber.Dec)
        self.lcdNumber_inside_speed.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_inside_speed.setProperty("value", 0.100000000000000)

        self.gridLayout.addWidget(self.lcdNumber_inside_speed, 2, 1, 1, 1)

        self.label_9 = QLabel(self.widget_3)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_9, 0, 1, 1, 1)

        self.lineEdit_inside_location = QLineEdit(self.widget_3)
        self.lineEdit_inside_location.setObjectName(u"lineEdit_inside_location")
        sizePolicy4.setHeightForWidth(self.lineEdit_inside_location.sizePolicy().hasHeightForWidth())
        self.lineEdit_inside_location.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.lineEdit_inside_location, 3, 1, 1, 1)

        self.pushButton_start_location = QPushButton(self.widget_3)
        self.pushButton_start_location.setObjectName(u"pushButton_start_location")

        self.gridLayout.addWidget(self.pushButton_start_location, 6, 1, 1, 1)

        self.label_7 = QLabel(self.widget_3)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 3, 2, 1, 1)

        self.pushButton_start_speed = QPushButton(self.widget_3)
        self.pushButton_start_speed.setObjectName(u"pushButton_start_speed")

        self.gridLayout.addWidget(self.pushButton_start_speed, 6, 3, 1, 1)

        self.label_10 = QLabel(self.widget_3)
        self.label_10.setObjectName(u"label_10")
        sizePolicy1.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy1)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_10, 0, 3, 1, 1)

        self.label_12 = QLabel(self.widget_3)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 5, 0, 1, 1)

        self.lineEdit_inside_speed = QLineEdit(self.widget_3)
        self.lineEdit_inside_speed.setObjectName(u"lineEdit_inside_speed")
        sizePolicy4.setHeightForWidth(self.lineEdit_inside_speed.sizePolicy().hasHeightForWidth())
        self.lineEdit_inside_speed.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.lineEdit_inside_speed, 4, 1, 1, 1)

        self.lcdNumber_outside_speed = QLCDNumber(self.widget_3)
        self.lcdNumber_outside_speed.setObjectName(u"lcdNumber_outside_speed")
        sizePolicy6.setHeightForWidth(self.lcdNumber_outside_speed.sizePolicy().hasHeightForWidth())
        self.lcdNumber_outside_speed.setSizePolicy(sizePolicy6)
        self.lcdNumber_outside_speed.setMinimumSize(QSize(0, 26))
        self.lcdNumber_outside_speed.setSmallDecimalPoint(True)
        self.lcdNumber_outside_speed.setDigitCount(5)
        self.lcdNumber_outside_speed.setMode(QLCDNumber.Dec)
        self.lcdNumber_outside_speed.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_outside_speed.setProperty("value", 359.000000000000000)
        self.lcdNumber_outside_speed.setProperty("intValue", 359)

        self.gridLayout.addWidget(self.lcdNumber_outside_speed, 2, 3, 1, 1)

        self.label_5 = QLabel(self.widget_3)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.lineEdit_inside_acceleration = QLineEdit(self.widget_3)
        self.lineEdit_inside_acceleration.setObjectName(u"lineEdit_inside_acceleration")
        sizePolicy4.setHeightForWidth(self.lineEdit_inside_acceleration.sizePolicy().hasHeightForWidth())
        self.lineEdit_inside_acceleration.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.lineEdit_inside_acceleration, 5, 1, 1, 1)

        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)

        self.label_13 = QLabel(self.widget_3)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 5, 2, 1, 1)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget4 = QWidget(self.groupBox)
        self.widget4.setObjectName(u"widget4")
        self.horizontalLayout_8 = QHBoxLayout(self.widget4)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_30 = QLabel(self.widget4)
        self.label_30.setObjectName(u"label_30")
        sizePolicy.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.label_30)

        self.comboBox_turntable_rule = QComboBox(self.widget4)
        self.comboBox_turntable_rule.addItem("")
        self.comboBox_turntable_rule.setObjectName(u"comboBox_turntable_rule")
        sizePolicy2.setHeightForWidth(self.comboBox_turntable_rule.sizePolicy().hasHeightForWidth())
        self.comboBox_turntable_rule.setSizePolicy(sizePolicy2)
        self.comboBox_turntable_rule.setEditable(True)

        self.horizontalLayout_8.addWidget(self.comboBox_turntable_rule)


        self.verticalLayout.addWidget(self.widget4)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.widget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy1.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy1)
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.radioButton_power_flag = QRadioButton(self.groupBox_3)
        self.radioButton_power_flag.setObjectName(u"radioButton_power_flag")
        self.radioButton_power_flag.setEnabled(False)
        sizePolicy7 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.radioButton_power_flag.sizePolicy().hasHeightForWidth())
        self.radioButton_power_flag.setSizePolicy(sizePolicy7)
        self.radioButton_power_flag.setMouseTracking(True)
        self.radioButton_power_flag.setAcceptDrops(False)
        self.radioButton_power_flag.setCheckable(True)
        self.radioButton_power_flag.setChecked(False)
        self.radioButton_power_flag.setAutoExclusive(False)

        self.horizontalLayout_4.addWidget(self.radioButton_power_flag)

        self.comboBox_power_com = QComboBox(self.groupBox_3)
        self.comboBox_power_com.addItem("")
        self.comboBox_power_com.addItem("")
        self.comboBox_power_com.addItem("")
        self.comboBox_power_com.addItem("")
        self.comboBox_power_com.addItem("")
        self.comboBox_power_com.setObjectName(u"comboBox_power_com")
        sizePolicy3.setHeightForWidth(self.comboBox_power_com.sizePolicy().hasHeightForWidth())
        self.comboBox_power_com.setSizePolicy(sizePolicy3)
        self.comboBox_power_com.setEditable(True)

        self.horizontalLayout_4.addWidget(self.comboBox_power_com)

        self.pushButton_power_open = QPushButton(self.groupBox_3)
        self.pushButton_power_open.setObjectName(u"pushButton_power_open")
        sizePolicy4.setHeightForWidth(self.pushButton_power_open.sizePolicy().hasHeightForWidth())
        self.pushButton_power_open.setSizePolicy(sizePolicy4)

        self.horizontalLayout_4.addWidget(self.pushButton_power_open)

        self.pushButton_power_close = QPushButton(self.groupBox_3)
        self.pushButton_power_close.setObjectName(u"pushButton_power_close")
        sizePolicy4.setHeightForWidth(self.pushButton_power_close.sizePolicy().hasHeightForWidth())
        self.pushButton_power_close.setSizePolicy(sizePolicy4)

        self.horizontalLayout_4.addWidget(self.pushButton_power_close)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.widget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy1.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy1)
        self.gridLayout_3 = QGridLayout(self.groupBox_4)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.comboBox_tempbox_com = QComboBox(self.groupBox_4)
        self.comboBox_tempbox_com.addItem("")
        self.comboBox_tempbox_com.addItem("")
        self.comboBox_tempbox_com.addItem("")
        self.comboBox_tempbox_com.addItem("")
        self.comboBox_tempbox_com.addItem("")
        self.comboBox_tempbox_com.setObjectName(u"comboBox_tempbox_com")
        sizePolicy3.setHeightForWidth(self.comboBox_tempbox_com.sizePolicy().hasHeightForWidth())
        self.comboBox_tempbox_com.setSizePolicy(sizePolicy3)
        self.comboBox_tempbox_com.setMinimumSize(QSize(0, 0))
        self.comboBox_tempbox_com.setEditable(True)

        self.gridLayout_3.addWidget(self.comboBox_tempbox_com, 0, 0, 1, 1)

        self.lcdNumber_tempbox_temp = QLCDNumber(self.groupBox_4)
        self.lcdNumber_tempbox_temp.setObjectName(u"lcdNumber_tempbox_temp")
        self.lcdNumber_tempbox_temp.setMinimumSize(QSize(0, 25))
        self.lcdNumber_tempbox_temp.setSmallDecimalPoint(True)
        self.lcdNumber_tempbox_temp.setDigitCount(4)
        self.lcdNumber_tempbox_temp.setMode(QLCDNumber.Dec)
        self.lcdNumber_tempbox_temp.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_tempbox_temp.setProperty("value", 0.000000000000000)

        self.gridLayout_3.addWidget(self.lcdNumber_tempbox_temp, 0, 2, 1, 1)

        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")
        sizePolicy8 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy8)
        self.label_14.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_14, 0, 3, 1, 1)

        self.lcdNumber_tempbox_setting = QLCDNumber(self.groupBox_4)
        self.lcdNumber_tempbox_setting.setObjectName(u"lcdNumber_tempbox_setting")
        self.lcdNumber_tempbox_setting.setMinimumSize(QSize(0, 25))
        self.lcdNumber_tempbox_setting.setSmallDecimalPoint(True)
        self.lcdNumber_tempbox_setting.setDigitCount(4)
        self.lcdNumber_tempbox_setting.setMode(QLCDNumber.Dec)
        self.lcdNumber_tempbox_setting.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_tempbox_setting.setProperty("value", 0.000000000000000)
        self.lcdNumber_tempbox_setting.setProperty("intValue", 0)

        self.gridLayout_3.addWidget(self.lcdNumber_tempbox_setting, 0, 4, 1, 1)

        self.label_34 = QLabel(self.groupBox_4)
        self.label_34.setObjectName(u"label_34")
        sizePolicy8.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy8)
        self.label_34.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_34, 0, 1, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_4)

        self.groupBox_6 = QGroupBox(self.widget)
        self.groupBox_6.setObjectName(u"groupBox_6")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy9)
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(6, 6, 6, 6)
        self.widget5 = QWidget(self.groupBox_6)
        self.widget5.setObjectName(u"widget5")
        self.horizontalLayout_9 = QHBoxLayout(self.widget5)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.comboBox_binding_com = QComboBox(self.widget5)
        self.comboBox_binding_com.addItem("")
        self.comboBox_binding_com.addItem("")
        self.comboBox_binding_com.addItem("")
        self.comboBox_binding_com.addItem("")
        self.comboBox_binding_com.addItem("")
        self.comboBox_binding_com.setObjectName(u"comboBox_binding_com")
        sizePolicy10 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.comboBox_binding_com.sizePolicy().hasHeightForWidth())
        self.comboBox_binding_com.setSizePolicy(sizePolicy10)
        self.comboBox_binding_com.setEditable(True)

        self.horizontalLayout_9.addWidget(self.comboBox_binding_com)

        self.pushButton_binding_send = QPushButton(self.widget5)
        self.pushButton_binding_send.setObjectName(u"pushButton_binding_send")
        sizePolicy4.setHeightForWidth(self.pushButton_binding_send.sizePolicy().hasHeightForWidth())
        self.pushButton_binding_send.setSizePolicy(sizePolicy4)

        self.horizontalLayout_9.addWidget(self.pushButton_binding_send)


        self.verticalLayout_6.addWidget(self.widget5)

        self.widget6 = QWidget(self.groupBox_6)
        self.widget6.setObjectName(u"widget6")
        self.horizontalLayout_10 = QHBoxLayout(self.widget6)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_31 = QLabel(self.widget6)
        self.label_31.setObjectName(u"label_31")
        sizePolicy8.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy8)

        self.horizontalLayout_10.addWidget(self.label_31)

        self.lineEdit_binding_longitude = QLineEdit(self.widget6)
        self.lineEdit_binding_longitude.setObjectName(u"lineEdit_binding_longitude")
        sizePolicy4.setHeightForWidth(self.lineEdit_binding_longitude.sizePolicy().hasHeightForWidth())
        self.lineEdit_binding_longitude.setSizePolicy(sizePolicy4)

        self.horizontalLayout_10.addWidget(self.lineEdit_binding_longitude)

        self.label_32 = QLabel(self.widget6)
        self.label_32.setObjectName(u"label_32")
        sizePolicy8.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy8)

        self.horizontalLayout_10.addWidget(self.label_32)

        self.lineEdit_binding_latitude = QLineEdit(self.widget6)
        self.lineEdit_binding_latitude.setObjectName(u"lineEdit_binding_latitude")
        sizePolicy4.setHeightForWidth(self.lineEdit_binding_latitude.sizePolicy().hasHeightForWidth())
        self.lineEdit_binding_latitude.setSizePolicy(sizePolicy4)

        self.horizontalLayout_10.addWidget(self.lineEdit_binding_latitude)


        self.verticalLayout_6.addWidget(self.widget6)

        self.widget7 = QWidget(self.groupBox_6)
        self.widget7.setObjectName(u"widget7")
        self.horizontalLayout_14 = QHBoxLayout(self.widget7)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.label_33 = QLabel(self.widget7)
        self.label_33.setObjectName(u"label_33")
        sizePolicy8.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy8)

        self.horizontalLayout_14.addWidget(self.label_33)

        self.lineEdit_binding_height = QLineEdit(self.widget7)
        self.lineEdit_binding_height.setObjectName(u"lineEdit_binding_height")
        sizePolicy4.setHeightForWidth(self.lineEdit_binding_height.sizePolicy().hasHeightForWidth())
        self.lineEdit_binding_height.setSizePolicy(sizePolicy4)

        self.horizontalLayout_14.addWidget(self.lineEdit_binding_height)

        self.label_43 = QLabel(self.widget7)
        self.label_43.setObjectName(u"label_43")
        sizePolicy8.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy8)

        self.horizontalLayout_14.addWidget(self.label_43)

        self.lineEdit_binding_time = QLineEdit(self.widget7)
        self.lineEdit_binding_time.setObjectName(u"lineEdit_binding_time")
        sizePolicy4.setHeightForWidth(self.lineEdit_binding_time.sizePolicy().hasHeightForWidth())
        self.lineEdit_binding_time.setSizePolicy(sizePolicy4)

        self.horizontalLayout_14.addWidget(self.lineEdit_binding_time)


        self.verticalLayout_6.addWidget(self.widget7)

        self.lineEdit_binding_command = QLineEdit(self.groupBox_6)
        self.lineEdit_binding_command.setObjectName(u"lineEdit_binding_command")

        self.verticalLayout_6.addWidget(self.lineEdit_binding_command)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_36 = QLabel(self.groupBox_6)
        self.label_36.setObjectName(u"label_36")
        sizePolicy.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy)

        self.horizontalLayout_11.addWidget(self.label_36)

        self.comboBox_binding_rule = QComboBox(self.groupBox_6)
        self.comboBox_binding_rule.addItem("")
        self.comboBox_binding_rule.setObjectName(u"comboBox_binding_rule")
        sizePolicy10.setHeightForWidth(self.comboBox_binding_rule.sizePolicy().hasHeightForWidth())
        self.comboBox_binding_rule.setSizePolicy(sizePolicy10)
        self.comboBox_binding_rule.setEditable(True)

        self.horizontalLayout_11.addWidget(self.comboBox_binding_rule)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)


        self.verticalLayout_4.addWidget(self.groupBox_6)

        self.groupBox_5 = QGroupBox(self.widget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy2.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy2)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.widget_2 = QWidget(self.groupBox_5)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_13 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_automatic_mode = QLineEdit(self.widget_2)
        self.lineEdit_automatic_mode.setObjectName(u"lineEdit_automatic_mode")

        self.horizontalLayout_13.addWidget(self.lineEdit_automatic_mode)

        self.lcdNumber_automatic_time = QLCDNumber(self.widget_2)
        self.lcdNumber_automatic_time.setObjectName(u"lcdNumber_automatic_time")
        sizePolicy11 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.lcdNumber_automatic_time.sizePolicy().hasHeightForWidth())
        self.lcdNumber_automatic_time.setSizePolicy(sizePolicy11)
        self.lcdNumber_automatic_time.setMinimumSize(QSize(0, 0))
        self.lcdNumber_automatic_time.setSmallDecimalPoint(True)
        self.lcdNumber_automatic_time.setDigitCount(6)
        self.lcdNumber_automatic_time.setMode(QLCDNumber.Dec)
        self.lcdNumber_automatic_time.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_automatic_time.setProperty("value", 999999.000000000000000)
        self.lcdNumber_automatic_time.setProperty("intValue", 999999)

        self.horizontalLayout_13.addWidget(self.lcdNumber_automatic_time)


        self.verticalLayout_5.addWidget(self.widget_2)

        self.textBrowser_automatic_ruleline = QTextBrowser(self.groupBox_5)
        self.textBrowser_automatic_ruleline.setObjectName(u"textBrowser_automatic_ruleline")
        sizePolicy12 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.textBrowser_automatic_ruleline.sizePolicy().hasHeightForWidth())
        self.textBrowser_automatic_ruleline.setSizePolicy(sizePolicy12)
        self.textBrowser_automatic_ruleline.setMinimumSize(QSize(0, 0))
        self.textBrowser_automatic_ruleline.setMaximumSize(QSize(16777215, 16777215))
        self.textBrowser_automatic_ruleline.setSizeIncrement(QSize(0, 0))
        self.textBrowser_automatic_ruleline.setLineWrapMode(QTextEdit.NoWrap)
        self.textBrowser_automatic_ruleline.setReadOnly(False)
        self.textBrowser_automatic_ruleline.setOverwriteMode(False)
        self.textBrowser_automatic_ruleline.setAcceptRichText(True)

        self.verticalLayout_5.addWidget(self.textBrowser_automatic_ruleline)

        self.horizontalWidget_2 = QWidget(self.groupBox_5)
        self.horizontalWidget_2.setObjectName(u"horizontalWidget_2")
        sizePolicy5.setHeightForWidth(self.horizontalWidget_2.sizePolicy().hasHeightForWidth())
        self.horizontalWidget_2.setSizePolicy(sizePolicy5)
        self.horizontalWidget_2.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_6 = QHBoxLayout(self.horizontalWidget_2)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_41 = QLabel(self.horizontalWidget_2)
        self.label_41.setObjectName(u"label_41")
        sizePolicy.setHeightForWidth(self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.label_41)

        self.comboBox_automatic_rule = QComboBox(self.horizontalWidget_2)
        self.comboBox_automatic_rule.addItem("")
        self.comboBox_automatic_rule.setObjectName(u"comboBox_automatic_rule")
        sizePolicy3.setHeightForWidth(self.comboBox_automatic_rule.sizePolicy().hasHeightForWidth())
        self.comboBox_automatic_rule.setSizePolicy(sizePolicy3)
        self.comboBox_automatic_rule.setEditable(True)

        self.horizontalLayout_6.addWidget(self.comboBox_automatic_rule)


        self.verticalLayout_5.addWidget(self.horizontalWidget_2)

        self.widget_21 = QWidget(self.groupBox_5)
        self.widget_21.setObjectName(u"widget_21")
        sizePolicy9.setHeightForWidth(self.widget_21.sizePolicy().hasHeightForWidth())
        self.widget_21.setSizePolicy(sizePolicy9)
        self.widget_21.setLayoutDirection(Qt.LeftToRight)
        self.horizontalLayout_7 = QHBoxLayout(self.widget_21)
        self.horizontalLayout_7.setSpacing(7)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_load_data = QPushButton(self.widget_21)
        self.pushButton_load_data.setObjectName(u"pushButton_load_data")
        sizePolicy7.setHeightForWidth(self.pushButton_load_data.sizePolicy().hasHeightForWidth())
        self.pushButton_load_data.setSizePolicy(sizePolicy7)
        self.pushButton_load_data.setMinimumSize(QSize(0, 60))
        self.pushButton_load_data.setStyleSheet(u"font: 75 10pt \"Adobe Arabic\";")

        self.horizontalLayout_7.addWidget(self.pushButton_load_data)

        self.pushButton_begin_test = QPushButton(self.widget_21)
        self.pushButton_begin_test.setObjectName(u"pushButton_begin_test")
        sizePolicy7.setHeightForWidth(self.pushButton_begin_test.sizePolicy().hasHeightForWidth())
        self.pushButton_begin_test.setSizePolicy(sizePolicy7)
        self.pushButton_begin_test.setMinimumSize(QSize(0, 60))
        self.pushButton_begin_test.setStyleSheet(u"font: 75 10pt \"Adobe Arabic\";")

        self.horizontalLayout_7.addWidget(self.pushButton_begin_test)

        self.pushButton_stop_test = QPushButton(self.widget_21)
        self.pushButton_stop_test.setObjectName(u"pushButton_stop_test")
        sizePolicy7.setHeightForWidth(self.pushButton_stop_test.sizePolicy().hasHeightForWidth())
        self.pushButton_stop_test.setSizePolicy(sizePolicy7)
        self.pushButton_stop_test.setMinimumSize(QSize(0, 60))
        self.pushButton_stop_test.setStyleSheet(u"font: 75 10pt \"Adobe Arabic\";")

        self.horizontalLayout_7.addWidget(self.pushButton_stop_test)


        self.verticalLayout_5.addWidget(self.widget_21)


        self.verticalLayout_4.addWidget(self.groupBox_5)


        self.horizontalLayout_5.addWidget(self.widget)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy13 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy13)
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_9 = QGridLayout(self.tab_6)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(7)
        self.gridLayout_9.setVerticalSpacing(0)
        self.graphicsView_gyr_X = GraphicsLayoutWidget(self.tab_6)
        self.graphicsView_gyr_X.setObjectName(u"graphicsView_gyr_X")

        self.gridLayout_9.addWidget(self.graphicsView_gyr_X, 0, 0, 1, 1)

        self.graphicsView_gyr_Y = GraphicsLayoutWidget(self.tab_6)
        self.graphicsView_gyr_Y.setObjectName(u"graphicsView_gyr_Y")

        self.gridLayout_9.addWidget(self.graphicsView_gyr_Y, 1, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_26 = QLabel(self.tab_6)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_5.addWidget(self.label_26, 0, 2, 1, 1)

        self.label_15 = QLabel(self.tab_6)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_5.addWidget(self.label_15, 0, 4, 1, 1)

        self.label_18 = QLabel(self.tab_6)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_5.addWidget(self.label_18, 2, 10, 1, 1)

        self.lineEdit_inside_location_13 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_13.setObjectName(u"lineEdit_inside_location_13")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_13, 1, 11, 1, 1)

        self.lineEdit_inside_location_14 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_14.setObjectName(u"lineEdit_inside_location_14")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_14, 2, 11, 1, 1)

        self.lineEdit_inside_location_10 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_10.setObjectName(u"lineEdit_inside_location_10")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_10, 1, 7, 1, 1)

        self.lineEdit_inside_location_8 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_8.setObjectName(u"lineEdit_inside_location_8")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_8, 2, 5, 1, 1)

        self.lineEdit_inside_location_3 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_3.setObjectName(u"lineEdit_inside_location_3")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_3, 1, 5, 1, 1)

        self.label_21 = QLabel(self.tab_6)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_5.addWidget(self.label_21, 1, 2, 1, 1)

        self.label_22 = QLabel(self.tab_6)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_5.addWidget(self.label_22, 1, 4, 1, 1)

        self.label_25 = QLabel(self.tab_6)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_5.addWidget(self.label_25, 2, 4, 1, 1)

        self.lineEdit_inside_location_7 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_7.setObjectName(u"lineEdit_inside_location_7")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_7, 2, 9, 1, 1)

        self.lineEdit_inside_location_15 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_15.setObjectName(u"lineEdit_inside_location_15")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_15, 0, 7, 1, 1)

        self.label_17 = QLabel(self.tab_6)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_5.addWidget(self.label_17, 1, 6, 1, 1)

        self.label_28 = QLabel(self.tab_6)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_5.addWidget(self.label_28, 1, 8, 1, 1)

        self.lineEdit_inside_location_9 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_9.setObjectName(u"lineEdit_inside_location_9")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_9, 0, 11, 1, 1)

        self.label_27 = QLabel(self.tab_6)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_5.addWidget(self.label_27, 2, 6, 1, 1)

        self.label_19 = QLabel(self.tab_6)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_5.addWidget(self.label_19, 0, 8, 1, 1)

        self.label_23 = QLabel(self.tab_6)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_5.addWidget(self.label_23, 1, 10, 1, 1)

        self.lineEdit_inside_location_11 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_11.setObjectName(u"lineEdit_inside_location_11")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_11, 1, 3, 1, 1)

        self.lineEdit_inside_location_6 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_6.setObjectName(u"lineEdit_inside_location_6")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_6, 1, 9, 1, 1)

        self.comboBox_rulename_4 = QComboBox(self.tab_6)
        self.comboBox_rulename_4.addItem("")
        self.comboBox_rulename_4.setObjectName(u"comboBox_rulename_4")
        self.comboBox_rulename_4.setEditable(True)

        self.gridLayout_5.addWidget(self.comboBox_rulename_4, 0, 3, 1, 1)

        self.lineEdit_inside_location_4 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_4.setObjectName(u"lineEdit_inside_location_4")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_4, 0, 9, 1, 1)

        self.lineEdit_inside_location_5 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_5.setObjectName(u"lineEdit_inside_location_5")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_5, 0, 5, 1, 1)

        self.label_24 = QLabel(self.tab_6)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_5.addWidget(self.label_24, 2, 8, 1, 1)

        self.label_29 = QLabel(self.tab_6)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_5.addWidget(self.label_29, 0, 10, 1, 1)

        self.label_20 = QLabel(self.tab_6)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_5.addWidget(self.label_20, 0, 6, 1, 1)

        self.lineEdit_inside_location_12 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_12.setObjectName(u"lineEdit_inside_location_12")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_12, 2, 3, 1, 1)

        self.lineEdit_inside_location_16 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_16.setObjectName(u"lineEdit_inside_location_16")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_16, 2, 7, 1, 1)

        self.label_16 = QLabel(self.tab_6)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_5.addWidget(self.label_16, 2, 2, 1, 1)

        self.lineEdit_inside_location_17 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_17.setObjectName(u"lineEdit_inside_location_17")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_17, 2, 1, 1, 1)

        self.label_40 = QLabel(self.tab_6)
        self.label_40.setObjectName(u"label_40")

        self.gridLayout_5.addWidget(self.label_40, 2, 0, 1, 1)

        self.comboBox_multiple_choice = QComboBox(self.tab_6)
        self.comboBox_multiple_choice.addItem("")
        self.comboBox_multiple_choice.setObjectName(u"comboBox_multiple_choice")
        sizePolicy14 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.comboBox_multiple_choice.sizePolicy().hasHeightForWidth())
        self.comboBox_multiple_choice.setSizePolicy(sizePolicy14)
        self.comboBox_multiple_choice.setEditable(True)

        self.gridLayout_5.addWidget(self.comboBox_multiple_choice, 0, 1, 1, 1)

        self.lineEdit_inside_location_18 = QLineEdit(self.tab_6)
        self.lineEdit_inside_location_18.setObjectName(u"lineEdit_inside_location_18")

        self.gridLayout_5.addWidget(self.lineEdit_inside_location_18, 1, 1, 1, 1)

        self.label_37 = QLabel(self.tab_6)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_5.addWidget(self.label_37, 1, 0, 1, 1)

        self.label_35 = QLabel(self.tab_6)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_5.addWidget(self.label_35, 0, 0, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_5, 5, 0, 1, 1)

        self.textBrowser_single_test = QTextBrowser(self.tab_6)
        self.textBrowser_single_test.setObjectName(u"textBrowser_single_test")

        self.gridLayout_9.addWidget(self.textBrowser_single_test, 3, 0, 1, 1)

        self.graphicsView_gyr_Z = GraphicsLayoutWidget(self.tab_6)
        self.graphicsView_gyr_Z.setObjectName(u"graphicsView_gyr_Z")
        self.graphicsView_gyr_Z.setAcceptDrops(False)
        self.graphicsView_gyr_Z.setAutoFillBackground(False)

        self.gridLayout_9.addWidget(self.graphicsView_gyr_Z, 2, 0, 1, 1)

        self.tabWidget.addTab(self.tab_6, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_21 = QGroupBox(self.tab_2)
        self.groupBox_21.setObjectName(u"groupBox_21")
        sizePolicy2.setHeightForWidth(self.groupBox_21.sizePolicy().hasHeightForWidth())
        self.groupBox_21.setSizePolicy(sizePolicy2)
        self.groupBox_21.setMinimumSize(QSize(0, 25))
        self.gridLayout_4 = QGridLayout(self.groupBox_21)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(2)
        self.gridLayout_4.setContentsMargins(-1, -1, -1, 1)
        self.combox_set_baund_2 = QComboBox(self.groupBox_21)
        self.combox_set_baund_2.addItem("")
        self.combox_set_baund_2.addItem("")
        self.combox_set_baund_2.addItem("")
        self.combox_set_baund_2.addItem("")
        self.combox_set_baund_2.addItem("")
        self.combox_set_baund_2.setObjectName(u"combox_set_baund_2")
        self.combox_set_baund_2.setMinimumSize(QSize(0, 30))
        self.combox_set_baund_2.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_2, 1, 2, 1, 1)

        self.pushButton_com_open_11 = QPushButton(self.groupBox_21)
        self.pushButton_com_open_11.setObjectName(u"pushButton_com_open_11")
        self.pushButton_com_open_11.setMinimumSize(QSize(0, 30))
        self.pushButton_com_open_11.setAutoDefault(False)
        self.pushButton_com_open_11.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_11, 10, 5, 1, 1)

        self.combox_set_com_6 = QComboBox(self.groupBox_21)
        self.combox_set_com_6.addItem("")
        self.combox_set_com_6.addItem("")
        self.combox_set_com_6.addItem("")
        self.combox_set_com_6.addItem("")
        self.combox_set_com_6.addItem("")
        self.combox_set_com_6.setObjectName(u"combox_set_com_6")
        self.combox_set_com_6.setMinimumSize(QSize(0, 30))
        self.combox_set_com_6.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_com_6, 5, 1, 1, 1)

        self.label_39 = QLabel(self.groupBox_21)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.label_39, 1, 0, 1, 1)

        self.comboBox_set_check_12 = QComboBox(self.groupBox_21)
        self.comboBox_set_check_12.addItem("")
        self.comboBox_set_check_12.addItem("")
        self.comboBox_set_check_12.addItem("")
        self.comboBox_set_check_12.setObjectName(u"comboBox_set_check_12")
        self.comboBox_set_check_12.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_set_check_12, 11, 3, 1, 1)

        self.combox_set_com_1 = QComboBox(self.groupBox_21)
        self.combox_set_com_1.addItem("")
        self.combox_set_com_1.addItem("")
        self.combox_set_com_1.addItem("")
        self.combox_set_com_1.addItem("")
        self.combox_set_com_1.addItem("")
        self.combox_set_com_1.setObjectName(u"combox_set_com_1")
        self.combox_set_com_1.setMinimumSize(QSize(90, 30))
        self.combox_set_com_1.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_com_1, 0, 1, 1, 1)

        self.comboBox_set_check_8 = QComboBox(self.groupBox_21)
        self.comboBox_set_check_8.addItem("")
        self.comboBox_set_check_8.addItem("")
        self.comboBox_set_check_8.addItem("")
        self.comboBox_set_check_8.setObjectName(u"comboBox_set_check_8")
        self.comboBox_set_check_8.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_set_check_8, 7, 3, 1, 1)

        self.label_84 = QLabel(self.groupBox_21)
        self.label_84.setObjectName(u"label_84")
        self.label_84.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.label_84, 10, 0, 1, 1)

        self.comboBox_stopbit_4 = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_4.addItem("")
        self.comboBox_stopbit_4.addItem("")
        self.comboBox_stopbit_4.setObjectName(u"comboBox_stopbit_4")
        self.comboBox_stopbit_4.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_4, 3, 4, 1, 1)

        self.lineEdit_file_names_11 = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_11.setObjectName(u"lineEdit_file_names_11")
        self.lineEdit_file_names_11.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_11, 10, 6, 1, 1)

        self.lineEdit_file_names_all = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_all.setObjectName(u"lineEdit_file_names_all")
        sizePolicy15 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.lineEdit_file_names_all.sizePolicy().hasHeightForWidth())
        self.lineEdit_file_names_all.setSizePolicy(sizePolicy15)
        self.lineEdit_file_names_all.setMinimumSize(QSize(0, 28))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_all, 12, 6, 1, 1)

        self.comboBox_set_check_10 = QComboBox(self.groupBox_21)
        self.comboBox_set_check_10.addItem("")
        self.comboBox_set_check_10.addItem("")
        self.comboBox_set_check_10.addItem("")
        self.comboBox_set_check_10.setObjectName(u"comboBox_set_check_10")
        self.comboBox_set_check_10.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_set_check_10, 9, 3, 1, 1)

        self.lineEdit_file_names_10 = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_10.setObjectName(u"lineEdit_file_names_10")
        self.lineEdit_file_names_10.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_10, 9, 6, 1, 1)

        self.combox_set_com_12 = QComboBox(self.groupBox_21)
        self.combox_set_com_12.addItem("")
        self.combox_set_com_12.addItem("")
        self.combox_set_com_12.addItem("")
        self.combox_set_com_12.addItem("")
        self.combox_set_com_12.addItem("")
        self.combox_set_com_12.setObjectName(u"combox_set_com_12")
        self.combox_set_com_12.setMinimumSize(QSize(0, 30))
        self.combox_set_com_12.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_com_12, 11, 1, 1, 1)

        self.combox_set_com_4 = QComboBox(self.groupBox_21)
        self.combox_set_com_4.addItem("")
        self.combox_set_com_4.addItem("")
        self.combox_set_com_4.addItem("")
        self.combox_set_com_4.addItem("")
        self.combox_set_com_4.addItem("")
        self.combox_set_com_4.setObjectName(u"combox_set_com_4")
        self.combox_set_com_4.setMinimumSize(QSize(0, 30))
        self.combox_set_com_4.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_com_4, 3, 1, 1, 1)

        self.label_80 = QLabel(self.groupBox_21)
        self.label_80.setObjectName(u"label_80")
        self.label_80.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.label_80, 8, 0, 1, 1)

        self.combox_set_baund_9 = QComboBox(self.groupBox_21)
        self.combox_set_baund_9.addItem("")
        self.combox_set_baund_9.addItem("")
        self.combox_set_baund_9.addItem("")
        self.combox_set_baund_9.addItem("")
        self.combox_set_baund_9.addItem("")
        self.combox_set_baund_9.setObjectName(u"combox_set_baund_9")
        self.combox_set_baund_9.setMinimumSize(QSize(0, 30))
        self.combox_set_baund_9.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_9, 8, 2, 1, 1)

        self.comboBox_stopbit_2 = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_2.addItem("")
        self.comboBox_stopbit_2.addItem("")
        self.comboBox_stopbit_2.setObjectName(u"comboBox_stopbit_2")
        self.comboBox_stopbit_2.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_2, 1, 4, 1, 1)

        self.comboBox_set_check_1 = QComboBox(self.groupBox_21)
        self.comboBox_set_check_1.addItem("")
        self.comboBox_set_check_1.addItem("")
        self.comboBox_set_check_1.addItem("")
        self.comboBox_set_check_1.setObjectName(u"comboBox_set_check_1")
        self.comboBox_set_check_1.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_set_check_1, 0, 3, 1, 1)

        self.comboBox_stopbit_6 = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_6.addItem("")
        self.comboBox_stopbit_6.addItem("")
        self.comboBox_stopbit_6.setObjectName(u"comboBox_stopbit_6")
        self.comboBox_stopbit_6.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_6, 5, 4, 1, 1)

        self.comboBox_stopbit_8 = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_8.addItem("")
        self.comboBox_stopbit_8.addItem("")
        self.comboBox_stopbit_8.setObjectName(u"comboBox_stopbit_8")
        self.comboBox_stopbit_8.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_8, 7, 4, 1, 1)

        self.combox_set_baund_all = QComboBox(self.groupBox_21)
        self.combox_set_baund_all.addItem("")
        self.combox_set_baund_all.addItem("")
        self.combox_set_baund_all.addItem("")
        self.combox_set_baund_all.addItem("")
        self.combox_set_baund_all.addItem("")
        self.combox_set_baund_all.setObjectName(u"combox_set_baund_all")
        sizePolicy9.setHeightForWidth(self.combox_set_baund_all.sizePolicy().hasHeightForWidth())
        self.combox_set_baund_all.setSizePolicy(sizePolicy9)
        self.combox_set_baund_all.setMinimumSize(QSize(0, 28))
        self.combox_set_baund_all.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_all, 12, 2, 1, 1)

        self.comboBox_stopbit_9 = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_9.addItem("")
        self.comboBox_stopbit_9.addItem("")
        self.comboBox_stopbit_9.setObjectName(u"comboBox_stopbit_9")
        self.comboBox_stopbit_9.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_9, 8, 4, 1, 1)

        self.comboBox_set_check_3 = QComboBox(self.groupBox_21)
        self.comboBox_set_check_3.addItem("")
        self.comboBox_set_check_3.addItem("")
        self.comboBox_set_check_3.addItem("")
        self.comboBox_set_check_3.setObjectName(u"comboBox_set_check_3")
        self.comboBox_set_check_3.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_set_check_3, 2, 3, 1, 1)

        self.lineEdit_file_names_8 = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_8.setObjectName(u"lineEdit_file_names_8")
        self.lineEdit_file_names_8.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_8, 7, 6, 1, 1)

        self.combox_set_baund_1 = QComboBox(self.groupBox_21)
        self.combox_set_baund_1.addItem("")
        self.combox_set_baund_1.addItem("")
        self.combox_set_baund_1.addItem("")
        self.combox_set_baund_1.addItem("")
        self.combox_set_baund_1.addItem("")
        self.combox_set_baund_1.setObjectName(u"combox_set_baund_1")
        self.combox_set_baund_1.setMinimumSize(QSize(0, 30))
        self.combox_set_baund_1.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_1, 0, 2, 1, 1)

        self.comboBox_set_check_2 = QComboBox(self.groupBox_21)
        self.comboBox_set_check_2.addItem("")
        self.comboBox_set_check_2.addItem("")
        self.comboBox_set_check_2.addItem("")
        self.comboBox_set_check_2.setObjectName(u"comboBox_set_check_2")
        self.comboBox_set_check_2.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_set_check_2, 1, 3, 1, 1)

        self.combox_set_baund_7 = QComboBox(self.groupBox_21)
        self.combox_set_baund_7.addItem("")
        self.combox_set_baund_7.addItem("")
        self.combox_set_baund_7.addItem("")
        self.combox_set_baund_7.addItem("")
        self.combox_set_baund_7.addItem("")
        self.combox_set_baund_7.setObjectName(u"combox_set_baund_7")
        self.combox_set_baund_7.setMinimumSize(QSize(0, 30))
        self.combox_set_baund_7.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_7, 6, 2, 1, 1)

        self.lineEdit_file_names_1 = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_1.setObjectName(u"lineEdit_file_names_1")
        self.lineEdit_file_names_1.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_1, 0, 6, 1, 1)

        self.combox_set_com_9 = QComboBox(self.groupBox_21)
        self.combox_set_com_9.addItem("")
        self.combox_set_com_9.addItem("")
        self.combox_set_com_9.addItem("")
        self.combox_set_com_9.addItem("")
        self.combox_set_com_9.addItem("")
        self.combox_set_com_9.setObjectName(u"combox_set_com_9")
        self.combox_set_com_9.setMinimumSize(QSize(0, 30))
        self.combox_set_com_9.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_com_9, 8, 1, 1, 1)

        self.combox_set_baund_12 = QComboBox(self.groupBox_21)
        self.combox_set_baund_12.addItem("")
        self.combox_set_baund_12.addItem("")
        self.combox_set_baund_12.addItem("")
        self.combox_set_baund_12.addItem("")
        self.combox_set_baund_12.addItem("")
        self.combox_set_baund_12.setObjectName(u"combox_set_baund_12")
        self.combox_set_baund_12.setMinimumSize(QSize(0, 30))
        self.combox_set_baund_12.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_12, 11, 2, 1, 1)

        self.pushButton_com_open_4 = QPushButton(self.groupBox_21)
        self.pushButton_com_open_4.setObjectName(u"pushButton_com_open_4")
        self.pushButton_com_open_4.setMinimumSize(QSize(0, 30))
        self.pushButton_com_open_4.setAutoDefault(False)
        self.pushButton_com_open_4.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_4, 3, 5, 1, 1)

        self.pushButton_com_open_8 = QPushButton(self.groupBox_21)
        self.pushButton_com_open_8.setObjectName(u"pushButton_com_open_8")
        self.pushButton_com_open_8.setMinimumSize(QSize(0, 30))
        self.pushButton_com_open_8.setAutoDefault(False)
        self.pushButton_com_open_8.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_8, 7, 5, 1, 1)

        self.pushButton_com_open_7 = QPushButton(self.groupBox_21)
        self.pushButton_com_open_7.setObjectName(u"pushButton_com_open_7")
        self.pushButton_com_open_7.setMinimumSize(QSize(0, 30))
        self.pushButton_com_open_7.setAutoDefault(False)
        self.pushButton_com_open_7.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_7, 6, 5, 1, 1)

        self.label_86 = QLabel(self.groupBox_21)
        self.label_86.setObjectName(u"label_86")
        self.label_86.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.label_86, 11, 0, 1, 1)

        self.pushButton_com_open_6 = QPushButton(self.groupBox_21)
        self.pushButton_com_open_6.setObjectName(u"pushButton_com_open_6")
        self.pushButton_com_open_6.setMinimumSize(QSize(0, 30))
        self.pushButton_com_open_6.setAutoDefault(False)
        self.pushButton_com_open_6.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_6, 5, 5, 1, 1)

        self.comboBox_stopbit_10 = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_10.addItem("")
        self.comboBox_stopbit_10.addItem("")
        self.comboBox_stopbit_10.setObjectName(u"comboBox_stopbit_10")
        self.comboBox_stopbit_10.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_10, 9, 4, 1, 1)

        self.label_82 = QLabel(self.groupBox_21)
        self.label_82.setObjectName(u"label_82")
        self.label_82.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.label_82, 9, 0, 1, 1)

        self.label_42 = QLabel(self.groupBox_21)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.label_42, 2, 0, 1, 1)

        self.combox_set_baund_5 = QComboBox(self.groupBox_21)
        self.combox_set_baund_5.addItem("")
        self.combox_set_baund_5.addItem("")
        self.combox_set_baund_5.addItem("")
        self.combox_set_baund_5.addItem("")
        self.combox_set_baund_5.addItem("")
        self.combox_set_baund_5.setObjectName(u"combox_set_baund_5")
        self.combox_set_baund_5.setMinimumSize(QSize(0, 30))
        self.combox_set_baund_5.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_5, 4, 2, 1, 1)

        self.combox_set_com_11 = QComboBox(self.groupBox_21)
        self.combox_set_com_11.addItem("")
        self.combox_set_com_11.addItem("")
        self.combox_set_com_11.addItem("")
        self.combox_set_com_11.addItem("")
        self.combox_set_com_11.addItem("")
        self.combox_set_com_11.setObjectName(u"combox_set_com_11")
        self.combox_set_com_11.setMinimumSize(QSize(0, 30))
        self.combox_set_com_11.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_com_11, 10, 1, 1, 1)

        self.combox_set_baund_8 = QComboBox(self.groupBox_21)
        self.combox_set_baund_8.addItem("")
        self.combox_set_baund_8.addItem("")
        self.combox_set_baund_8.addItem("")
        self.combox_set_baund_8.addItem("")
        self.combox_set_baund_8.addItem("")
        self.combox_set_baund_8.setObjectName(u"combox_set_baund_8")
        self.combox_set_baund_8.setMinimumSize(QSize(0, 30))
        self.combox_set_baund_8.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_8, 7, 2, 1, 1)

        self.comboBox_set_check_6 = QComboBox(self.groupBox_21)
        self.comboBox_set_check_6.addItem("")
        self.comboBox_set_check_6.addItem("")
        self.comboBox_set_check_6.addItem("")
        self.comboBox_set_check_6.setObjectName(u"comboBox_set_check_6")
        self.comboBox_set_check_6.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_set_check_6, 5, 3, 1, 1)

        self.pushButton_com_open_5 = QPushButton(self.groupBox_21)
        self.pushButton_com_open_5.setObjectName(u"pushButton_com_open_5")
        self.pushButton_com_open_5.setMinimumSize(QSize(0, 30))
        self.pushButton_com_open_5.setAutoDefault(False)
        self.pushButton_com_open_5.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_5, 4, 5, 1, 1)

        self.combox_set_com_3 = QComboBox(self.groupBox_21)
        self.combox_set_com_3.addItem("")
        self.combox_set_com_3.addItem("")
        self.combox_set_com_3.addItem("")
        self.combox_set_com_3.addItem("")
        self.combox_set_com_3.addItem("")
        self.combox_set_com_3.setObjectName(u"combox_set_com_3")
        self.combox_set_com_3.setMinimumSize(QSize(0, 30))
        self.combox_set_com_3.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_com_3, 2, 1, 1, 1)

        self.comboBox_set_check_7 = QComboBox(self.groupBox_21)
        self.comboBox_set_check_7.addItem("")
        self.comboBox_set_check_7.addItem("")
        self.comboBox_set_check_7.addItem("")
        self.comboBox_set_check_7.setObjectName(u"comboBox_set_check_7")
        self.comboBox_set_check_7.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_set_check_7, 6, 3, 1, 1)

        self.comboBox_stopbit_1 = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_1.addItem("")
        self.comboBox_stopbit_1.addItem("")
        self.comboBox_stopbit_1.setObjectName(u"comboBox_stopbit_1")
        self.comboBox_stopbit_1.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_1, 0, 4, 1, 1)

        self.pushButton_com_open_1 = QPushButton(self.groupBox_21)
        self.pushButton_com_open_1.setObjectName(u"pushButton_com_open_1")
        self.pushButton_com_open_1.setMinimumSize(QSize(0, 30))
        self.pushButton_com_open_1.setAutoDefault(False)
        self.pushButton_com_open_1.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_1, 0, 5, 1, 1)

        self.label_49 = QLabel(self.groupBox_21)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.label_49, 5, 0, 1, 1)

        self.lineEdit_file_names_6 = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_6.setObjectName(u"lineEdit_file_names_6")
        self.lineEdit_file_names_6.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_6, 5, 6, 1, 1)

        self.lineEdit_file_names_4 = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_4.setObjectName(u"lineEdit_file_names_4")
        self.lineEdit_file_names_4.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_4, 3, 6, 1, 1)

        self.combox_set_com_2 = QComboBox(self.groupBox_21)
        self.combox_set_com_2.addItem("")
        self.combox_set_com_2.addItem("")
        self.combox_set_com_2.addItem("")
        self.combox_set_com_2.addItem("")
        self.combox_set_com_2.addItem("")
        self.combox_set_com_2.setObjectName(u"combox_set_com_2")
        self.combox_set_com_2.setMinimumSize(QSize(0, 30))
        self.combox_set_com_2.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_com_2, 1, 1, 1, 1)

        self.lineEdit_file_names_5 = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_5.setObjectName(u"lineEdit_file_names_5")
        self.lineEdit_file_names_5.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_5, 4, 6, 1, 1)

        self.label_53 = QLabel(self.groupBox_21)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.label_53, 7, 0, 1, 1)

        self.comboBox_stopbit_11 = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_11.addItem("")
        self.comboBox_stopbit_11.addItem("")
        self.comboBox_stopbit_11.setObjectName(u"comboBox_stopbit_11")
        self.comboBox_stopbit_11.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_11, 10, 4, 1, 1)

        self.pushButton_com_open_3 = QPushButton(self.groupBox_21)
        self.pushButton_com_open_3.setObjectName(u"pushButton_com_open_3")
        self.pushButton_com_open_3.setMinimumSize(QSize(0, 30))
        self.pushButton_com_open_3.setAutoDefault(False)
        self.pushButton_com_open_3.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_3, 2, 5, 1, 1)

        self.comboBox_stopbit_3 = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_3.addItem("")
        self.comboBox_stopbit_3.addItem("")
        self.comboBox_stopbit_3.setObjectName(u"comboBox_stopbit_3")
        self.comboBox_stopbit_3.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_3, 2, 4, 1, 1)

        self.pushButton_com_open_2 = QPushButton(self.groupBox_21)
        self.pushButton_com_open_2.setObjectName(u"pushButton_com_open_2")
        self.pushButton_com_open_2.setMinimumSize(QSize(0, 30))
        self.pushButton_com_open_2.setCheckable(False)
        self.pushButton_com_open_2.setAutoDefault(False)
        self.pushButton_com_open_2.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_2, 1, 5, 1, 1)

        self.comboBox_stopbit_all = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_all.addItem("")
        self.comboBox_stopbit_all.addItem("")
        self.comboBox_stopbit_all.setObjectName(u"comboBox_stopbit_all")
        sizePolicy9.setHeightForWidth(self.comboBox_stopbit_all.sizePolicy().hasHeightForWidth())
        self.comboBox_stopbit_all.setSizePolicy(sizePolicy9)
        self.comboBox_stopbit_all.setMinimumSize(QSize(0, 28))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_all, 12, 4, 1, 1)

        self.comboBox_set_check_5 = QComboBox(self.groupBox_21)
        self.comboBox_set_check_5.addItem("")
        self.comboBox_set_check_5.addItem("")
        self.comboBox_set_check_5.addItem("")
        self.comboBox_set_check_5.setObjectName(u"comboBox_set_check_5")
        self.comboBox_set_check_5.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_set_check_5, 4, 3, 1, 1)

        self.comboBox_set_check_9 = QComboBox(self.groupBox_21)
        self.comboBox_set_check_9.addItem("")
        self.comboBox_set_check_9.addItem("")
        self.comboBox_set_check_9.addItem("")
        self.comboBox_set_check_9.setObjectName(u"comboBox_set_check_9")
        self.comboBox_set_check_9.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_set_check_9, 8, 3, 1, 1)

        self.pushButton_com_open_9 = QPushButton(self.groupBox_21)
        self.pushButton_com_open_9.setObjectName(u"pushButton_com_open_9")
        self.pushButton_com_open_9.setMinimumSize(QSize(0, 30))
        self.pushButton_com_open_9.setAutoDefault(False)
        self.pushButton_com_open_9.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_9, 8, 5, 1, 1)

        self.lineEdit_file_names_2 = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_2.setObjectName(u"lineEdit_file_names_2")
        self.lineEdit_file_names_2.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_2, 1, 6, 1, 1)

        self.comboBox_set_check_4 = QComboBox(self.groupBox_21)
        self.comboBox_set_check_4.addItem("")
        self.comboBox_set_check_4.addItem("")
        self.comboBox_set_check_4.addItem("")
        self.comboBox_set_check_4.setObjectName(u"comboBox_set_check_4")
        self.comboBox_set_check_4.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_set_check_4, 3, 3, 1, 1)

        self.comboBox_stopbit_7 = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_7.addItem("")
        self.comboBox_stopbit_7.addItem("")
        self.comboBox_stopbit_7.setObjectName(u"comboBox_stopbit_7")
        self.comboBox_stopbit_7.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_7, 6, 4, 1, 1)

        self.label_44 = QLabel(self.groupBox_21)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.label_44, 3, 0, 1, 1)

        self.label_46 = QLabel(self.groupBox_21)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.label_46, 4, 0, 1, 1)

        self.pushButton_com_open_all = QPushButton(self.groupBox_21)
        self.pushButton_com_open_all.setObjectName(u"pushButton_com_open_all")
        sizePolicy16 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy16.setHorizontalStretch(0)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.pushButton_com_open_all.sizePolicy().hasHeightForWidth())
        self.pushButton_com_open_all.setSizePolicy(sizePolicy16)
        self.pushButton_com_open_all.setMinimumSize(QSize(0, 28))
        self.pushButton_com_open_all.setAutoDefault(False)
        self.pushButton_com_open_all.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_all, 12, 5, 1, 1)

        self.label_38 = QLabel(self.groupBox_21)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.label_38, 0, 0, 1, 1)

        self.combox_set_com_all = QComboBox(self.groupBox_21)
        self.combox_set_com_all.addItem("")
        self.combox_set_com_all.addItem("")
        self.combox_set_com_all.addItem("")
        self.combox_set_com_all.addItem("")
        self.combox_set_com_all.addItem("")
        self.combox_set_com_all.setObjectName(u"combox_set_com_all")
        sizePolicy9.setHeightForWidth(self.combox_set_com_all.sizePolicy().hasHeightForWidth())
        self.combox_set_com_all.setSizePolicy(sizePolicy9)
        self.combox_set_com_all.setMinimumSize(QSize(0, 28))

        self.gridLayout_4.addWidget(self.combox_set_com_all, 12, 1, 1, 1)

        self.label_51 = QLabel(self.groupBox_21)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.label_51, 6, 0, 1, 1)

        self.combox_set_com_10 = QComboBox(self.groupBox_21)
        self.combox_set_com_10.addItem("")
        self.combox_set_com_10.addItem("")
        self.combox_set_com_10.addItem("")
        self.combox_set_com_10.addItem("")
        self.combox_set_com_10.addItem("")
        self.combox_set_com_10.setObjectName(u"combox_set_com_10")
        self.combox_set_com_10.setMinimumSize(QSize(0, 30))
        self.combox_set_com_10.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_com_10, 9, 1, 1, 1)

        self.combox_set_com_5 = QComboBox(self.groupBox_21)
        self.combox_set_com_5.addItem("")
        self.combox_set_com_5.addItem("")
        self.combox_set_com_5.addItem("")
        self.combox_set_com_5.addItem("")
        self.combox_set_com_5.addItem("")
        self.combox_set_com_5.setObjectName(u"combox_set_com_5")
        self.combox_set_com_5.setMinimumSize(QSize(0, 30))
        self.combox_set_com_5.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_com_5, 4, 1, 1, 1)

        self.lineEdit_file_names_3 = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_3.setObjectName(u"lineEdit_file_names_3")
        self.lineEdit_file_names_3.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_3, 2, 6, 1, 1)

        self.combox_set_baund_3 = QComboBox(self.groupBox_21)
        self.combox_set_baund_3.addItem("")
        self.combox_set_baund_3.addItem("")
        self.combox_set_baund_3.addItem("")
        self.combox_set_baund_3.addItem("")
        self.combox_set_baund_3.addItem("")
        self.combox_set_baund_3.setObjectName(u"combox_set_baund_3")
        self.combox_set_baund_3.setMinimumSize(QSize(0, 30))
        self.combox_set_baund_3.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_3, 2, 2, 1, 1)

        self.pushButton_com_open_10 = QPushButton(self.groupBox_21)
        self.pushButton_com_open_10.setObjectName(u"pushButton_com_open_10")
        self.pushButton_com_open_10.setMinimumSize(QSize(0, 30))
        self.pushButton_com_open_10.setAutoDefault(False)
        self.pushButton_com_open_10.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_10, 9, 5, 1, 1)

        self.combox_set_baund_6 = QComboBox(self.groupBox_21)
        self.combox_set_baund_6.addItem("")
        self.combox_set_baund_6.addItem("")
        self.combox_set_baund_6.addItem("")
        self.combox_set_baund_6.addItem("")
        self.combox_set_baund_6.addItem("")
        self.combox_set_baund_6.setObjectName(u"combox_set_baund_6")
        self.combox_set_baund_6.setMinimumSize(QSize(0, 30))
        self.combox_set_baund_6.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_6, 5, 2, 1, 1)

        self.comboBox_set_check_all = QComboBox(self.groupBox_21)
        self.comboBox_set_check_all.addItem("")
        self.comboBox_set_check_all.addItem("")
        self.comboBox_set_check_all.addItem("")
        self.comboBox_set_check_all.setObjectName(u"comboBox_set_check_all")
        sizePolicy9.setHeightForWidth(self.comboBox_set_check_all.sizePolicy().hasHeightForWidth())
        self.comboBox_set_check_all.setSizePolicy(sizePolicy9)
        self.comboBox_set_check_all.setMinimumSize(QSize(0, 28))

        self.gridLayout_4.addWidget(self.comboBox_set_check_all, 12, 3, 1, 1)

        self.comboBox_stopbit_12 = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_12.addItem("")
        self.comboBox_stopbit_12.addItem("")
        self.comboBox_stopbit_12.setObjectName(u"comboBox_stopbit_12")
        self.comboBox_stopbit_12.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_12, 11, 4, 1, 1)

        self.combox_set_com_7 = QComboBox(self.groupBox_21)
        self.combox_set_com_7.addItem("")
        self.combox_set_com_7.addItem("")
        self.combox_set_com_7.addItem("")
        self.combox_set_com_7.addItem("")
        self.combox_set_com_7.addItem("")
        self.combox_set_com_7.setObjectName(u"combox_set_com_7")
        self.combox_set_com_7.setMinimumSize(QSize(0, 30))
        self.combox_set_com_7.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_com_7, 6, 1, 1, 1)

        self.lineEdit_file_names_12 = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_12.setObjectName(u"lineEdit_file_names_12")
        self.lineEdit_file_names_12.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_12, 11, 6, 1, 1)

        self.comboBox_set_check_11 = QComboBox(self.groupBox_21)
        self.comboBox_set_check_11.addItem("")
        self.comboBox_set_check_11.addItem("")
        self.comboBox_set_check_11.addItem("")
        self.comboBox_set_check_11.setObjectName(u"comboBox_set_check_11")
        self.comboBox_set_check_11.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_set_check_11, 10, 3, 1, 1)

        self.label_78 = QLabel(self.groupBox_21)
        self.label_78.setObjectName(u"label_78")
        sizePolicy9.setHeightForWidth(self.label_78.sizePolicy().hasHeightForWidth())
        self.label_78.setSizePolicy(sizePolicy9)
        self.label_78.setMinimumSize(QSize(0, 20))

        self.gridLayout_4.addWidget(self.label_78, 12, 0, 1, 1)

        self.pushButton_com_open_12 = QPushButton(self.groupBox_21)
        self.pushButton_com_open_12.setObjectName(u"pushButton_com_open_12")
        self.pushButton_com_open_12.setMinimumSize(QSize(0, 30))
        self.pushButton_com_open_12.setAutoDefault(False)
        self.pushButton_com_open_12.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_com_open_12, 11, 5, 1, 1)

        self.combox_set_com_8 = QComboBox(self.groupBox_21)
        self.combox_set_com_8.addItem("")
        self.combox_set_com_8.addItem("")
        self.combox_set_com_8.addItem("")
        self.combox_set_com_8.addItem("")
        self.combox_set_com_8.addItem("")
        self.combox_set_com_8.setObjectName(u"combox_set_com_8")
        self.combox_set_com_8.setMinimumSize(QSize(0, 30))
        self.combox_set_com_8.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_com_8, 7, 1, 1, 1)

        self.lineEdit_file_names_9 = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_9.setObjectName(u"lineEdit_file_names_9")
        self.lineEdit_file_names_9.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_9, 8, 6, 1, 1)

        self.combox_set_baund_10 = QComboBox(self.groupBox_21)
        self.combox_set_baund_10.addItem("")
        self.combox_set_baund_10.addItem("")
        self.combox_set_baund_10.addItem("")
        self.combox_set_baund_10.addItem("")
        self.combox_set_baund_10.addItem("")
        self.combox_set_baund_10.setObjectName(u"combox_set_baund_10")
        self.combox_set_baund_10.setMinimumSize(QSize(0, 30))
        self.combox_set_baund_10.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_10, 9, 2, 1, 1)

        self.lineEdit_file_names_7 = QLineEdit(self.groupBox_21)
        self.lineEdit_file_names_7.setObjectName(u"lineEdit_file_names_7")
        self.lineEdit_file_names_7.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEdit_file_names_7, 6, 6, 1, 1)

        self.combox_set_baund_11 = QComboBox(self.groupBox_21)
        self.combox_set_baund_11.addItem("")
        self.combox_set_baund_11.addItem("")
        self.combox_set_baund_11.addItem("")
        self.combox_set_baund_11.addItem("")
        self.combox_set_baund_11.addItem("")
        self.combox_set_baund_11.setObjectName(u"combox_set_baund_11")
        self.combox_set_baund_11.setMinimumSize(QSize(0, 30))
        self.combox_set_baund_11.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_11, 10, 2, 1, 1)

        self.comboBox_stopbit_5 = QComboBox(self.groupBox_21)
        self.comboBox_stopbit_5.addItem("")
        self.comboBox_stopbit_5.addItem("")
        self.comboBox_stopbit_5.setObjectName(u"comboBox_stopbit_5")
        self.comboBox_stopbit_5.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.comboBox_stopbit_5, 4, 4, 1, 1)

        self.combox_set_baund_4 = QComboBox(self.groupBox_21)
        self.combox_set_baund_4.addItem("")
        self.combox_set_baund_4.addItem("")
        self.combox_set_baund_4.addItem("")
        self.combox_set_baund_4.addItem("")
        self.combox_set_baund_4.addItem("")
        self.combox_set_baund_4.setObjectName(u"combox_set_baund_4")
        self.combox_set_baund_4.setMinimumSize(QSize(0, 30))
        self.combox_set_baund_4.setEditable(True)

        self.gridLayout_4.addWidget(self.combox_set_baund_4, 3, 2, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_21)

        self.groupBox_9 = QGroupBox(self.tab_2)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.textBrowser_progress_display1 = QTextBrowser(self.groupBox_9)
        self.textBrowser_progress_display1.setObjectName(u"textBrowser_progress_display1")

        self.verticalLayout_8.addWidget(self.textBrowser_progress_display1)

        self.textBrowser_progress_display2 = QTextBrowser(self.groupBox_9)
        self.textBrowser_progress_display2.setObjectName(u"textBrowser_progress_display2")

        self.verticalLayout_8.addWidget(self.textBrowser_progress_display2)


        self.verticalLayout_3.addWidget(self.groupBox_9)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_2 = QGridLayout(self.tab)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.textBrowser_3 = QTextBrowser(self.tab)
        self.textBrowser_3.setObjectName(u"textBrowser_3")

        self.gridLayout_2.addWidget(self.textBrowser_3, 2, 0, 1, 1)

        self.textBrowser_4 = QTextBrowser(self.tab)
        self.textBrowser_4.setObjectName(u"textBrowser_4")

        self.gridLayout_2.addWidget(self.textBrowser_4, 3, 0, 1, 1)

        self.textBrowser_2 = QTextBrowser(self.tab)
        self.textBrowser_2.setObjectName(u"textBrowser_2")

        self.gridLayout_2.addWidget(self.textBrowser_2, 1, 0, 1, 1)

        self.textBrowser_5 = QTextBrowser(self.tab)
        self.textBrowser_5.setObjectName(u"textBrowser_5")

        self.gridLayout_2.addWidget(self.textBrowser_5, 4, 0, 1, 1)

        self.textBrowser_1 = QTextBrowser(self.tab)
        self.textBrowser_1.setObjectName(u"textBrowser_1")

        self.gridLayout_2.addWidget(self.textBrowser_1, 0, 0, 1, 1)

        self.textBrowser_6 = QTextBrowser(self.tab)
        self.textBrowser_6.setObjectName(u"textBrowser_6")

        self.gridLayout_2.addWidget(self.textBrowser_6, 5, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_7 = QVBoxLayout(self.tab_4)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.textBrowser_7 = QTextBrowser(self.tab_4)
        self.textBrowser_7.setObjectName(u"textBrowser_7")

        self.verticalLayout_7.addWidget(self.textBrowser_7)

        self.textBrowser_8 = QTextBrowser(self.tab_4)
        self.textBrowser_8.setObjectName(u"textBrowser_8")

        self.verticalLayout_7.addWidget(self.textBrowser_8)

        self.textBrowser_9 = QTextBrowser(self.tab_4)
        self.textBrowser_9.setObjectName(u"textBrowser_9")

        self.verticalLayout_7.addWidget(self.textBrowser_9)

        self.textBrowser_10 = QTextBrowser(self.tab_4)
        self.textBrowser_10.setObjectName(u"textBrowser_10")

        self.verticalLayout_7.addWidget(self.textBrowser_10)

        self.textBrowser_11 = QTextBrowser(self.tab_4)
        self.textBrowser_11.setObjectName(u"textBrowser_11")

        self.verticalLayout_7.addWidget(self.textBrowser_11)

        self.textBrowser_12 = QTextBrowser(self.tab_4)
        self.textBrowser_12.setObjectName(u"textBrowser_12")

        self.verticalLayout_7.addWidget(self.textBrowser_12)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.groupBox_7 = QGroupBox(self.tab_3)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(10, 10, 871, 281))
        self.gridLayout_7 = QGridLayout(self.groupBox_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.graphicsView_gyr_X_3 = GraphicsLayoutWidget(self.groupBox_7)
        self.graphicsView_gyr_X_3.setObjectName(u"graphicsView_gyr_X_3")

        self.gridLayout_7.addWidget(self.graphicsView_gyr_X_3, 0, 0, 1, 1)

        self.groupBox_8 = QGroupBox(self.tab_3)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setGeometry(QRect(10, 300, 881, 271))
        self.gridLayout_8 = QGridLayout(self.groupBox_8)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.graphicsView_gyr_X_4 = GraphicsLayoutWidget(self.groupBox_8)
        self.graphicsView_gyr_X_4.setObjectName(u"graphicsView_gyr_X_4")

        self.gridLayout_8.addWidget(self.graphicsView_gyr_X_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")

        self.horizontalLayout_5.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.pushButton_com_open_11.setDefault(False)
        self.pushButton_com_open_4.setDefault(False)
        self.pushButton_com_open_8.setDefault(False)
        self.pushButton_com_open_7.setDefault(False)
        self.pushButton_com_open_6.setDefault(False)
        self.pushButton_com_open_5.setDefault(False)
        self.pushButton_com_open_1.setDefault(False)
        self.pushButton_com_open_3.setDefault(False)
        self.pushButton_com_open_2.setDefault(False)
        self.pushButton_com_open_9.setDefault(False)
        self.pushButton_com_open_all.setDefault(False)
        self.pushButton_com_open_10.setDefault(False)
        self.pushButton_com_open_12.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u901a\u8baf\u534f\u8bae\u6a21\u5757", None))
        self.comboBox_protocal_com.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.comboBox_protocal_com.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))

        self.comboBox_protocal_baund.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.comboBox_protocal_baund.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.comboBox_protocal_baund.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.comboBox_protocal_baund.setItemText(3, QCoreApplication.translate("MainWindow", u"921600", None))

        self.comboBox_protocal_check.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_protocal_check.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_protocal_check.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u534f\u8bae:", None))
        self.comboBox_protocal_rule.setItemText(0, QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u534f\u8bae", None))

        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8f6c\u53f0\u63a7\u5236\u6a21\u5757", None))
        self.comboBox_turntable_com.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.comboBox_turntable_com.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.comboBox_turntable_com.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.comboBox_turntable_com.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.comboBox_turntable_com.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.comboBox_turntable_com.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_turntable_open.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f\u901a\u8baf", None))
        self.pushButton_turntable_close.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u901a\u8baf", None))
        self.lineEdit_outside_location.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineEdit_outside_acceleration.setText(QCoreApplication.translate("MainWindow", u"24", None))
        self.lineEdit_outside_speed.setText(QCoreApplication.translate("MainWindow", u"24", None))
        self.pushButton_inside_reset.setText(QCoreApplication.translate("MainWindow", u"\u5f52\u96f6", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u4f4d\u7f6e", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u901f\u7387", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u901f\u7387", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u4f4d\u7f6e", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u4f4d\u7f6e", None))
        self.pushButton_outside_reset.setText(QCoreApplication.translate("MainWindow", u"\u5f52\u96f6", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u5185\u6846", None))
        self.lineEdit_inside_location.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.pushButton_start_location.setText(QCoreApplication.translate("MainWindow", u"\u4f4d\u7f6e\u8f6c\u52a8", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u4f4d\u7f6e", None))
        self.pushButton_start_speed.setText(QCoreApplication.translate("MainWindow", u"\u901f\u5ea6\u8f6c\u52a8", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u5916\u6846", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u901f", None))
        self.lineEdit_inside_speed.setText(QCoreApplication.translate("MainWindow", u"36", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u901f\u7387", None))
        self.lineEdit_inside_acceleration.setText(QCoreApplication.translate("MainWindow", u"36", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u901f\u7387", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u901f", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"\u6807\u5b9a:", None))
        self.comboBox_turntable_rule.setItemText(0, QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u534f\u8bae", None))

        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u7535\u6e90\u63a7\u5236\u6a21\u5757", None))
        self.radioButton_power_flag.setText("")
        self.comboBox_power_com.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.comboBox_power_com.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.comboBox_power_com.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.comboBox_power_com.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.comboBox_power_com.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.comboBox_power_com.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_power_open.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f\u7535\u6e90", None))
        self.pushButton_power_close.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u7535\u6e90", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u6e29\u7bb1\u63a7\u5236\u6a21\u5757", None))
        self.comboBox_tempbox_com.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.comboBox_tempbox_com.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.comboBox_tempbox_com.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.comboBox_tempbox_com.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.comboBox_tempbox_com.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.comboBox_tempbox_com.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u5b9a", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"\u5b9e\u65f6", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"\u60ef\u5bfc\u88c5\u8ba2\u6a21\u5757", None))
        self.comboBox_binding_com.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.comboBox_binding_com.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.comboBox_binding_com.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.comboBox_binding_com.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.comboBox_binding_com.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.comboBox_binding_com.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_binding_send.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u88c5\u8ba2", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"\u7ecf\u5ea6", None))
        self.lineEdit_binding_longitude.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"\u7eac\u5ea6", None))
        self.lineEdit_binding_latitude.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"\u9ad8\u5ea6", None))
        self.lineEdit_binding_height.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"\u5bf9\u51c6", None))
        self.lineEdit_binding_time.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"\u534f\u8bae:", None))
        self.comboBox_binding_rule.setItemText(0, QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u534f\u8bae", None))

        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u6d4b\u8bd5\u6a21\u5757", None))
        self.textBrowser_automatic_ruleline.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"\u534f\u8bae:", None))
        self.comboBox_automatic_rule.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))

        self.pushButton_load_data.setText(QCoreApplication.translate("MainWindow", u"\u8f7d\u5165\n"
"\u6570\u636e", None))
        self.pushButton_begin_test.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\n"
"\u6d4b\u8bd5", None))
        self.pushButton_stop_test.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\n"
"\u6d4b\u8bd5", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"\u8d77\u59cb", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"X\u8f74", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u6807\u51c6\u5dee", None))
        self.lineEdit_inside_location_13.setText("")
        self.lineEdit_inside_location_14.setText("")
        self.lineEdit_inside_location_10.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.lineEdit_inside_location_8.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.lineEdit_inside_location_3.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"\u5e73\u6ed1", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Y\u8f74", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Z\u8f74", None))
        self.lineEdit_inside_location_7.setText("")
        self.lineEdit_inside_location_15.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u7cfb\u6570", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"\u5747\u503c", None))
        self.lineEdit_inside_location_9.setText("")
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"\u7cfb\u6570", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"\u5747\u503c", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"\u6807\u51c6\u5dee", None))
        self.lineEdit_inside_location_11.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.lineEdit_inside_location_6.setText("")
        self.comboBox_rulename_4.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))

        self.lineEdit_inside_location_4.setText("")
        self.lineEdit_inside_location_5.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"\u5747\u503c", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"\u6807\u51c6\u5dee", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"\u7cfb\u6570", None))
        self.lineEdit_inside_location_12.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineEdit_inside_location_16.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\u8df3\u8fc7", None))
        self.lineEdit_inside_location_17.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"\u5907\u7528", None))
        self.comboBox_multiple_choice.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))

        self.lineEdit_inside_location_18.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"\u5907\u7528", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"\u591a\u8def", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"\u5355\u8def", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("MainWindow", u"\u591a\u8def\u8bbe\u7f6e\u6a21\u5757", None))
        self.combox_set_baund_2.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_2.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_2.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_2.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_2.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_2.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_com_open_11.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.combox_set_com_6.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_6.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_6.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_6.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_6.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_6.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Tab_2", None))
        self.comboBox_set_check_12.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_12.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_12.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.combox_set_com_1.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_1.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_1.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_1.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_1.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_1.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_set_check_8.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_8.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_8.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.label_84.setText(QCoreApplication.translate("MainWindow", u"Tab_11", None))
        self.comboBox_stopbit_4.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_4.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.lineEdit_file_names_11.setText(QCoreApplication.translate("MainWindow", u"autosave11", None))
        self.lineEdit_file_names_all.setText(QCoreApplication.translate("MainWindow", u"autosave", None))
        self.comboBox_set_check_10.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_10.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_10.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.lineEdit_file_names_10.setText(QCoreApplication.translate("MainWindow", u"autosave10", None))
        self.combox_set_com_12.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_12.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_12.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_12.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_12.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_12.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.combox_set_com_4.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_4.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_4.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_4.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_4.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_4.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_80.setText(QCoreApplication.translate("MainWindow", u"Tab_9", None))
        self.combox_set_baund_9.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_9.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_9.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_9.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_9.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_9.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_stopbit_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_2.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.comboBox_set_check_1.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_1.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_1.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.comboBox_stopbit_6.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_6.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.comboBox_stopbit_8.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_8.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.combox_set_baund_all.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_all.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_all.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_all.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_all.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_all.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_stopbit_9.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_9.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.comboBox_set_check_3.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_3.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_3.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.lineEdit_file_names_8.setText(QCoreApplication.translate("MainWindow", u"autosave8", None))
        self.combox_set_baund_1.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_1.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_1.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_1.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_1.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_1.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_set_check_2.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_2.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_2.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.combox_set_baund_7.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_7.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_7.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_7.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_7.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_7.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_file_names_1.setText(QCoreApplication.translate("MainWindow", u"autosave1", None))
        self.combox_set_com_9.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_9.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_9.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_9.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_9.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_9.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.combox_set_baund_12.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_12.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_12.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_12.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_12.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_12.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_com_open_4.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.pushButton_com_open_8.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.pushButton_com_open_7.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.label_86.setText(QCoreApplication.translate("MainWindow", u"Tab_12", None))
        self.pushButton_com_open_6.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.comboBox_stopbit_10.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_10.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.label_82.setText(QCoreApplication.translate("MainWindow", u"Tab_10", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Tab_3", None))
        self.combox_set_baund_5.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_5.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_5.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_5.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_5.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_5.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.combox_set_com_11.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_11.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_11.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_11.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_11.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_11.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.combox_set_baund_8.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_8.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_8.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_8.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_8.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_8.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_set_check_6.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_6.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_6.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.pushButton_com_open_5.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.combox_set_com_3.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_3.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_3.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_3.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_3.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_3.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_set_check_7.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_7.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_7.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.comboBox_stopbit_1.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_1.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.pushButton_com_open_1.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Tab_6", None))
        self.lineEdit_file_names_6.setText(QCoreApplication.translate("MainWindow", u"autosave6", None))
        self.lineEdit_file_names_4.setText(QCoreApplication.translate("MainWindow", u"autosave4", None))
        self.combox_set_com_2.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_2.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_2.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_2.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_2.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_2.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_file_names_5.setText(QCoreApplication.translate("MainWindow", u"autosave5", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"Tab_8", None))
        self.comboBox_stopbit_11.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_11.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.pushButton_com_open_3.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.comboBox_stopbit_3.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_3.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.pushButton_com_open_2.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.comboBox_stopbit_all.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_all.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.comboBox_set_check_5.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_5.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_5.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.comboBox_set_check_9.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_9.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_9.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.pushButton_com_open_9.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.lineEdit_file_names_2.setText(QCoreApplication.translate("MainWindow", u"autosave2", None))
        self.comboBox_set_check_4.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_4.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_4.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.comboBox_stopbit_7.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_7.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Tab_4", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Tab_5", None))
        self.pushButton_com_open_all.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Tab_1", None))
        self.combox_set_com_all.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_all.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_all.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_all.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_all.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_all.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Tab_7", None))
        self.combox_set_com_10.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_10.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_10.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_10.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_10.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_10.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.combox_set_com_5.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_5.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_5.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_5.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_5.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_5.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_file_names_3.setText(QCoreApplication.translate("MainWindow", u"autosave3", None))
        self.combox_set_baund_3.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_3.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_3.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_3.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_3.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_3.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_com_open_10.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.combox_set_baund_6.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_6.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_6.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_6.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_6.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_6.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_set_check_all.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_all.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_all.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.comboBox_stopbit_12.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_12.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.combox_set_com_7.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_7.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_7.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_7.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_7.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_7.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_file_names_12.setText(QCoreApplication.translate("MainWindow", u"autosave12", None))
        self.comboBox_set_check_11.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u6821\u9a8c", None))
        self.comboBox_set_check_11.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5076\u6821\u9a8c", None))
        self.comboBox_set_check_11.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5947\u6821\u9a8c", None))

        self.label_78.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">\u603b\u63a7</span></p></body></html>", None))
        self.pushButton_com_open_12.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.combox_set_com_8.setItemText(0, QCoreApplication.translate("MainWindow", u"COM1", None))
        self.combox_set_com_8.setItemText(1, QCoreApplication.translate("MainWindow", u"COM2", None))
        self.combox_set_com_8.setItemText(2, QCoreApplication.translate("MainWindow", u"COM3", None))
        self.combox_set_com_8.setItemText(3, QCoreApplication.translate("MainWindow", u"COM4", None))
        self.combox_set_com_8.setItemText(4, QCoreApplication.translate("MainWindow", u"COM5", None))

#if QT_CONFIG(tooltip)
        self.combox_set_com_8.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4e32\u53e3</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_file_names_9.setText(QCoreApplication.translate("MainWindow", u"autosave9", None))
        self.combox_set_baund_10.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_10.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_10.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_10.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_10.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_10.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_file_names_7.setText(QCoreApplication.translate("MainWindow", u"autosave7", None))
        self.combox_set_baund_11.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_11.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_11.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_11.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_11.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_11.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_stopbit_5.setItemText(0, QCoreApplication.translate("MainWindow", u"Stop1", None))
        self.comboBox_stopbit_5.setItemText(1, QCoreApplication.translate("MainWindow", u"Stop2", None))

        self.combox_set_baund_4.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.combox_set_baund_4.setItemText(1, QCoreApplication.translate("MainWindow", u"230400", None))
        self.combox_set_baund_4.setItemText(2, QCoreApplication.translate("MainWindow", u"460800", None))
        self.combox_set_baund_4.setItemText(3, QCoreApplication.translate("MainWindow", u"614400", None))
        self.combox_set_baund_4.setItemText(4, QCoreApplication.translate("MainWindow", u"921600", None))

#if QT_CONFIG(tooltip)
        self.combox_set_baund_4.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u6ce2\u7279\u7387</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"\u8fdb\u5ea6\u663e\u793a\u6a21\u5757", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u591a\u8def", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"1-6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"7-12", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"\u901f\u5ea6", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"\u4f4d\u7f6e", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u60ef\u5bfc", None))
    # retranslateUi

