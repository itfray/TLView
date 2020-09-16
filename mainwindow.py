from PySide2.QtWidgets import QMainWindow
from ui_mainwindow import Ui_MainWindow
from TLTableModel import TLTableModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # link model with view
        self.tlTableModel = TLTableModel()
        self.ui.tableView.setModel(self.tlTableModel)