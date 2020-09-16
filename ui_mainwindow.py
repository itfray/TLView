# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(779, 563)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableView = QTableView(self.centralWidget)
        self.tableView.setObjectName(u"tableView")

        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 779, 26))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QToolBar(MainWindow)
        self.mainToolBar.setObjectName(u"mainToolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"TLView", None))
    # retranslateUi

