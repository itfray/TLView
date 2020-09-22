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
from tltableview import TLTableView


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
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_as = QAction(MainWindow)
        self.actionSave_as.setObjectName(u"actionSave_as")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionResolve_Addresses = QAction(MainWindow)
        self.actionResolve_Addresses.setObjectName(u"actionResolve_Addresses")
        self.actionResolve_Addresses.setCheckable(True)
        self.actionResolve_Addresses.setChecked(True)
        self.action1_seconds = QAction(MainWindow)
        self.action1_seconds.setObjectName(u"action1_seconds")
        self.action1_seconds.setCheckable(True)
        self.action1_seconds.setChecked(True)
        self.action2_seconds = QAction(MainWindow)
        self.action2_seconds.setObjectName(u"action2_seconds")
        self.action2_seconds.setCheckable(True)
        self.action3_seconds = QAction(MainWindow)
        self.action3_seconds.setObjectName(u"action3_seconds")
        self.action3_seconds.setCheckable(True)
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
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuOptions = QMenu(self.menuBar)
        self.menuOptions.setObjectName(u"menuOptions")
        self.menuView = QMenu(self.menuBar)
        self.menuView.setObjectName(u"menuView")
        self.menuUpdate_Speed = QMenu(self.menuView)
        self.menuUpdate_Speed.setObjectName(u"menuUpdate_Speed")
        self.menuAbout = QMenu(self.menuBar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.BottomToolBarArea, self.toolBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuOptions.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuOptions.addAction(self.actionResolve_Addresses)
        self.menuView.addAction(self.menuUpdate_Speed.menuAction())
        self.menuUpdate_Speed.addAction(self.action1_seconds)
        self.menuUpdate_Speed.addAction(self.action2_seconds)
        self.menuUpdate_Speed.addAction(self.action3_seconds)
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
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSave_as.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionResolve_Addresses.setText(QCoreApplication.translate("MainWindow", u"Resolve Addresses", None))
        self.action1_seconds.setText(QCoreApplication.translate("MainWindow", u"1 second", None))
        self.action2_seconds.setText(QCoreApplication.translate("MainWindow", u"2 seconds", None))
        self.action3_seconds.setText(QCoreApplication.translate("MainWindow", u"5 seconds", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuUpdate_Speed.setTitle(QCoreApplication.translate("MainWindow", u"Update Speed", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

