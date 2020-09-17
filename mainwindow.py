from PySide2.QtWidgets import QMainWindow, QMenu, QAction
from ui_mainwindow import Ui_MainWindow
from TLTableModel import TLTableModel
from PySide2.QtCore import QTimer, Slot, Signal, QThread, Qt


TIMER_VALUES = (1000, 3000, 5000)


def slot_kill_process():
    pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # link model with view
        self.tableModel = TLTableModel()
        self.ui.tableView.setModel(self.tableModel)
        self.tableModel.modelAboutToBeReset.connect(self.ui.tableView.storeSelectedRowNum)
        self.tableModel.modelReset.connect(self.ui.tableView.restoreSelectedRowNum)

        self.updateInfoInDownToolBar()

        # link model with timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tableModel.updateData)
        self.timer.timeout.connect(self.updateInfoInDownToolBar)
        self.timer.setInterval(TIMER_VALUES[0])
        self.timer.start()

        # link tableview with context menu
        self.ui.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableView.customContextMenuRequested.connect(self.callCustomContextMenu)

    @Slot()
    def updateInfoInDownToolBar(self):
        """ update info in down tool bar """
        self.ui.actionEndpoints.setText(f'Endpoints: {self.tableModel.countEndpoints()}')
        self.ui.actionEstablished.setText(f'Established: {self.tableModel.countEstablished()}')
        self.ui.actionListen.setText(f'Listen: {self.tableModel.countListen()}')
        self.ui.actionTime_Wait.setText(f'Time wait: {self.tableModel.countTimeWait()}')
        self.ui.actionClose_Wait.setText(f'Close wait: {self.tableModel.countCloseWait()}')

    @Slot()
    def callCustomContextMenu(self, pos):
        menu = QMenu(self)
        killAction = QAction("End process...", self)
        menu.addAction(killAction)
        killAction.triggered.connect(slot_kill_process)
        menu.popup(self.ui.tableView.viewport().mapToGlobal(pos))