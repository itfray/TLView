from PySide2.QtWidgets import QMainWindow
from ui_mainwindow import Ui_MainWindow
from TLTableModel import TLTableModel
from PySide2.QtCore import QTimer, Slot


TIMER_VALUES = (1000, 3000, 5000)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # link model with view
        self.tlTableModel = TLTableModel()
        self.ui.tableView.setModel(self.tlTableModel)

        # link model with timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tlTableModel.updateData)
        self.timer.timeout.connect(self.updateStatusBar)
        self.timer.setInterval(TIMER_VALUES[0])
        self.timer.start()

    @Slot()
    def updateStatusBar(self):
        status = f'Endpoints: {self.tlTableModel.countEndpoints()} | Established: {self.tlTableModel.countEstablished()} |'\
                 f'Listen: {self.tlTableModel.countListen()} | Time wait: {self.tlTableModel.countTimeWait()} |'\
                 f'Close wait: {self.tlTableModel.countCloseWait()} |'
        self.statusBar().showMessage(status, TIMER_VALUES[0])