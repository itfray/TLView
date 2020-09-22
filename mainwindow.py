from PySide2.QtWidgets import QMainWindow, QMenu, QAction, QMessageBox, QFileDialog
from ui_mainwindow import Ui_MainWindow
from tltablemodel import TLTableModel
from PySide2.QtCore import QTimer, Slot, Signal, Qt
import psutil


TIMER_VALUES = (1000, 2000, 5000)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.filename_save = ""

        # link model with view
        self.tableModel = TLTableModel()
        self.ui.tableView.setModel(self.tableModel)
        self.tableModel.modelAboutToBeReset.connect(self.ui.tableView.storeSelectedRowNum)
        self.tableModel.modelReset.connect(self.ui.tableView.restoreSelectedRowNum)
        # link view headers with model sorting
        header = self.ui.tableView.horizontalHeader()
        header.sectionClicked.connect(self.tableModel.sortDataByColumn)

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

        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionResolve_Addresses.triggered.connect(self.tableModel.setDomainNameMode)
        self.ui.actionResolve_Addresses.triggered.connect(self.tableModel.setServiceNameMode)

        check_action1 = MainWindow.gen_check_for_checkable_action(self.ui.action1_seconds,
                                                       self.ui.action2_seconds, self.ui.action3_seconds)
        check_action2 = MainWindow.gen_check_for_checkable_action(self.ui.action2_seconds,
                                                       self.ui.action1_seconds, self.ui.action3_seconds)
        check_action3 = MainWindow.gen_check_for_checkable_action(self.ui.action3_seconds,
                                                       self.ui.action1_seconds, self.ui.action2_seconds)
        self.ui.action1_seconds.triggered.connect(check_action1)
        self.ui.action2_seconds.triggered.connect(check_action2)
        self.ui.action3_seconds.triggered.connect(check_action3)
        self.ui.action1_seconds.triggered.connect(self.slot_action1_seconds)
        self.ui.action2_seconds.triggered.connect(self.slot_action2_seconds)
        self.ui.action3_seconds.triggered.connect(self.slot_action5_seconds)
        self.ui.actionAbout.triggered.connect(self.slot_about)
        self.ui.actionSave.triggered.connect(self.slot_save)
        self.ui.actionSave_as.triggered.connect(self.slot_save_as)

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
        # create message box for confirmation process termination
        ans = QMessageBox.warning(self, "Process termination",
                                  f"Terminate the process <{self.tableModel.process(selected_row)}>?",
                                  QMessageBox.Yes, QMessageBox.No)
        if ans == QMessageBox.Yes:
            pid = int(self.tableModel.pid(selected_row))    # get pid selected process
            try:
                process = psutil.Process(pid)               # get process handle
                process.terminate()
                QMessageBox.information(self, "Process termination", "The process was completed successfully!!!",
                                        QMessageBox.Ok)
            except psutil.NoSuchProcess:
                QMessageBox.information(self, "Process termination", "The process has already been terminated!!!",
                                        QMessageBox.Ok)
            except psutil.AccessDenied:
                QMessageBox.critical(self, "Process termination", "Access is denied. You need administrator rights!!!",
                                        QMessageBox.Ok)
        self.timer.start()

    @staticmethod
    def gen_check_for_checkable_action(act, *acts):
        """ Function generate check function for
            checkable actions """

        @Slot(bool)
        def check(value: bool):
            if value:
                # if one action checked, then other made unchecked
                for a in acts:
                    a.setChecked(False)
            else:
                # all actions can't be unchecked
                act.setChecked(True)

        return check

    @Slot()
    def slot_action1_seconds(self):
        self.timer.setInterval(TIMER_VALUES[0])

    @Slot()
    def slot_action2_seconds(self):
        self.timer.setInterval(TIMER_VALUES[1])

    @Slot()
    def slot_action5_seconds(self):
        self.timer.setInterval(TIMER_VALUES[2])

    @Slot()
    def slot_about(self):
        pass

    @Slot()
    def slot_save(self):
        if self.filename_save == '':
            self.save_table_dialog()
        if self.filename_save != '':
            print("file created!!!")
            self.tableModel.writeDataInFile()

    @Slot()
    def slot_save_as(self):
        self.save_table_dialog()
        if self.filename_save != '':
            print("file created!!!")
            self.tableModel.writeDataInFile()

    @Slot()
    def save_table_dialog(self):
        filename = f"/home/{self.tableModel.filename()}"
        filter = f"Text files (*.{TLTableModel.DEFAULT_EXTANSIONS[0]} *.{TLTableModel.DEFAULT_EXTANSIONS[1]})"
        self.filename_save = QFileDialog.getSaveFileName(self, "Save file", filename, filter)[0]
        self.tableModel.setFilename(self.filename_save)
