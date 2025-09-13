# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QListView,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QStatusBar, QTableView,
    QVBoxLayout, QWidget)
#import logo


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1403, 849)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.my_medicines = QListView(self.centralwidget)
        self.my_medicines.setObjectName(u"my_medicines")
        self.my_medicines.setGeometry(QRect(750, 300, 461, 171))
        self.my_medicines.setDragEnabled(True)
        self.quit = QPushButton(self.centralwidget)
        self.quit.setObjectName(u"quit")
        self.quit.setGeometry(QRect(1230, 160, 151, 121))
        self.Save_Button = QPushButton(self.centralwidget)
        self.Save_Button.setObjectName(u"Save_Button")
        self.Save_Button.setGeometry(QRect(1230, 20, 151, 121))
        self.DUR_data_box = QScrollArea(self.centralwidget)
        self.DUR_data_box.setObjectName(u"DUR_data_box")
        self.DUR_data_box.setGeometry(QRect(20, 530, 1361, 271))
        self.DUR_data_box.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1359, 269))
        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 0, 161, 31))
        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(460, 0, 121, 31))
        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(220, 10, 108, 24))
        self.DUR_data_table = QTableView(self.scrollAreaWidgetContents)
        self.DUR_data_table.setObjectName(u"DUR_data_table")
        self.DUR_data_table.setGeometry(QRect(20, 40, 1321, 211))
        self.DUR_data_box.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(750, 50, 461, 211))
        self.current_text_box = QVBoxLayout(self.verticalLayoutWidget)
        self.current_text_box.setObjectName(u"current_text_box")
        self.current_text_box.setContentsMargins(0, 0, 0, 0)
        self.current_text = QLabel(self.verticalLayoutWidget)
        self.current_text.setObjectName(u"current_text")
        self.current_text.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.current_text.setMargin(16)

        self.current_text_box.addWidget(self.current_text)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(750, 15, 161, 31))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 191, 31))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 480, 211, 41))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(750, 260, 251, 41))
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(19, 49, 691, 421))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.camera_frame = QLabel(self.verticalLayoutWidget_2)
        self.camera_frame.setObjectName(u"camera_frame")

        self.verticalLayout.addWidget(self.camera_frame)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(1230, 310, 151, 171))
        self.label_8.setPixmap(QPixmap(u":/images/logo.png"))
        self.label_8.setScaledContents(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1403, 22))
        self.menuMedicine_Manager = QMenu(self.menubar)
        self.menuMedicine_Manager.setObjectName(u"menuMedicine_Manager")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMedicine_Manager.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.quit.setText(QCoreApplication.translate("MainWindow", u"QUIT", None))
        self.Save_Button.setText(QCoreApplication.translate("MainWindow", u"SAVE", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\uc131\ubd84\uba85", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\ubd80\uc791\uc6a9", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.current_text.setText(QCoreApplication.translate("MainWindow", u"\uc57d \uc774\ub984\uc774 \uc5ec\uae30 \ub098\ud0c0\ub0a9\ub2c8\ub2e4.", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Current Text", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Camera View", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"DUR \uac80\uc0c9 \uacb0\uacfc", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\ud604\uc7ac \ubcf5\uc6a9\uc911\uc778 \uc57d", None))
        self.camera_frame.setText("")
        self.label_8.setText("")
        self.menuMedicine_Manager.setTitle(QCoreApplication.translate("MainWindow", u"Medicine Manager", None))
    # retranslateUi

