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
        self.my_medicines_list_view = QListView(self.centralwidget)
        self.my_medicines_list_view.setObjectName(u"my_medicines_list_view")
        self.my_medicines_list_view.setGeometry(QRect(750, 300, 461, 171))
        self.my_medicines_list_view.setDragEnabled(True)
        self.quit_button = QPushButton(self.centralwidget)
        self.quit_button.setObjectName(u"quit_button")
        self.quit_button.setGeometry(QRect(1230, 160, 151, 121))
        self.add_medicine_button = QPushButton(self.centralwidget)
        self.add_medicine_button.setObjectName(u"add_medicine_button")
        self.add_medicine_button.setGeometry(QRect(1230, 20, 151, 121))
        self.dur_data_scroll_area = QScrollArea(self.centralwidget)
        self.dur_data_scroll_area.setObjectName(u"dur_data_scroll_area")
        self.dur_data_scroll_area.setGeometry(QRect(20, 530, 1361, 271))
        self.dur_data_scroll_area.setWidgetResizable(True)
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
        self.dur_table_view = QTableView(self.scrollAreaWidgetContents)
        self.dur_table_view.setObjectName(u"dur_table_view")
        self.dur_table_view.setGeometry(QRect(20, 40, 1321, 211))
        self.dur_data_scroll_area.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(750, 50, 461, 211))
        self.current_text_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.current_text_layout.setObjectName(u"current_text_layout")
        self.current_text_layout.setContentsMargins(0, 0, 0, 0)
        self.ocr_result_label = QLabel(self.verticalLayoutWidget)
        self.ocr_result_label.setObjectName(u"ocr_result_label")
        self.ocr_result_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.ocr_result_label.setMargin(16)

        self.current_text_layout.addWidget(self.ocr_result_label)

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
        self.camera_view = QLabel(self.verticalLayoutWidget_2)
        self.camera_view.setObjectName(u"camera_view")

        self.verticalLayout.addWidget(self.camera_view)

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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Medicine Interaction Checker", None))
        self.quit_button.setText(QCoreApplication.translate("MainWindow", u"QUIT", None))
        self.add_medicine_button.setText(QCoreApplication.translate("MainWindow", u"ADD", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Ingredient", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Side Effects", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.ocr_result_label.setText(QCoreApplication.translate("MainWindow", u"Pill name will be displayed here.", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Current Text", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Camera View", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"DUR Search Results", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Currently Taking", None))
        self.camera_view.setText("")
        self.label_8.setText("")
        self.menuMedicine_Manager.setTitle(QCoreApplication.translate("MainWindow", u"Medicine Manager", None))
    # retranslateUi

