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
from TLTableView import TLTableView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(779, 563)
        self.actionEndpoints = QAction(MainWindow)
        self.actionEndpoints.setObjectName(u"actionEndpoints")
        self.actionEstablished = QAction(MainWindow)
        self.actionEstablished.setObjectName(u"actionEstablished")
        self.actionListen = QAction(MainWindow)
        self.actionListen.setObjectName(u"actionListen")
        self.actionTime_Wait = QAction(MainWindow)
        self.actionTime_Wait.setObjectName(u"actionTime_Wait")
        self.actionClose_Wait = QAction(MainWindow)
        self.actionClose_Wait.setObjectName(u"actionClose_Wait")
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableView = TLTableView(self.centralWidget)
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
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.BottomToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionEndpoints)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionEstablished)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionListen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTime_Wait)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClose_Wait)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"TLView", None))
        self.actionEndpoints.setText(QCoreApplication.translate("MainWindow", u"Endpoints: 0", None))
        self.actionEstablished.setText(QCoreApplication.translate("MainWindow", u"Established: 0", None))
        self.actionListen.setText(QCoreApplication.translate("MainWindow", u"Listen: 0", None))
        self.actionTime_Wait.setText(QCoreApplication.translate("MainWindow", u"Time Wait: 0", None))
        self.actionClose_Wait.setText(QCoreApplication.translate("MainWindow", u"Close Wait: 0", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

