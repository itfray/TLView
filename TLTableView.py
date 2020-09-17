from PySide2.QtWidgets import QTableView, QAbstractItemView


class TLTableView(QTableView):
    def __init__(self, parent = None):
        super().__init__(parent)
        # set only row selection mode
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # set only single row selection mode
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAutoScroll(False)
        self.selectedRow = -1        # selected row number

    def storeSelectedRowNum(self):
        selected_indexes = self.selectedIndexes()
        if len(selected_indexes) > 0:
            self.selectedRow = self.selectedIndexes()[0].row()

    def restoreSelectedRowNum(self):
        self.selectRow(self.selectedRow)