from PySide2.QtWidgets import QMainWindow, QMenu, QAction, QMessageBox
from ui_mainwindow import Ui_MainWindow
from tltablemodel import TLTableModel
from PySide2.QtCore import QTimer, Slot, Signal, QThread, Qt
import psutil


TIMER_VALUES = (1000, 3000, 5000)


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
        self.ui.tableView.customContextMenuRequested.connect(self.displayCustomContextMenu)

    @Slot()
    def updateInfoInDownToolBar(self):
        """ update info in down tool bar """
        self.ui.actionEndpoints.setText(f'Endpoints: {self.tableModel.countEndpoints()}')
        self.ui.actionEstablished.setText(f'Established: {self.tableModel.countEstablished()}')
        self.ui.actionListen.setText(f'Listen: {self.tableModel.countListen()}')
        self.ui.actionTime_Wait.setText(f'Time wait: {self.tableModel.countTimeWait()}')
        self.ui.actionClose_Wait.setText(f'Close wait: {self.tableModel.countCloseWait()}')

    @Slot()
    def displayCustomContextMenu(self, pos):
        """ Display contex menu on screen """
        # create menu object
        menu = QMenu(self)
        # create action for process termination
        terminateAction = QAction("End process...", self)
        menu.addAction(terminateAction)
        terminateAction.triggered.connect(self.slot_terminate_process)
        # display context menu
        menu.popup(self.ui.tableView.viewport().mapToGlobal(pos))

    @Slot()
    def slot_terminate_process(self):
        """ Handle for process termination"""
        selected_inds = self.ui.tableView.selectedIndexes()
        if len(selected_inds) == 0:
            return
        self.timer.stop()                                       # stop updating data on the window
        selected_row = selected_inds[0].row()
        process_name = self.tableModel.process(selected_row)    # get process name selected process
        # create message box for confirmation process termination
        ans = QMessageBox.warning(self, "Process termination", f"Terminate the process <{process_name}>?",
                                  QMessageBox.Yes, QMessageBox.No)
        if ans == QMessageBox.No:
            self.timer.start()
            return
        flag_error = False                              # flag_error == True if there were exceptions
        pid = int(self.tableModel.pid(selected_row))    # get pid selected process
        try:
            process = psutil.Process(pid)               # get process handle
            process.terminate()
        except psutil.NoSuchProcess:
            QMessageBox.information(self, "Process termination", "The process has already been terminated!!!",
                                    QMessageBox.Ok)
            flag_error = True
        except psutil.AccessDenied:
            QMessageBox.critical(self, "Process termination", "Access is denied. You need administrator rights!!!",
                                    QMessageBox.Ok)
            flag_error = True
        if not flag_error:
            QMessageBox.information(self, "Process termination", "The process was completed successfully!!!",
                                 QMessageBox.Ok)
        self.timer.start()
