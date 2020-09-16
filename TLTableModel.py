from operator import itemgetter
import psutil
import socket
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex, Slot
from PySide2.QtGui import QColor

def nameTransportProtocol(family: socket.AddressFamily, type: socket.SocketKind)-> str:
    if type == socket.SOCK_STREAM:
        ans = "TCP"
    elif type == socket.SOCK_DGRAM:
        ans = "UDP"
    if family == socket.AF_INET6:
        ans += "V6"
    return ans

# All main headers in TLTableModel
TABLE_HEADERS = ("Process", "PID", "Protocol", "Local Address", "Local Port",
                 "Remote Address", "Remote Port", "State")

# class TLTableModel is model table for work with host's network connections on transport layer
class TLTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.net_connections = []
        self.sortColumn = 1         # sorted column number
        self.sortASC = False  # ascending sort?
        self.updateData()

    @Slot()
    def updateData(self):
        """
         * 1. load system data about all network connections on taransport layer
         * 2. create data table
        """
        psutilAddrToIPAndPort = lambda paddr: (paddr.ip, paddr.port)\
            if type(paddr) != tuple else ('*', '*')
        statusBadValToGoodVal = lambda val: '' if val == 'NONE' else val
        self.net_connections = []
        # create data table
        for connection in psutil.net_connections():
            process = psutil.Process(connection.pid)
            row = [process.name(), connection.pid,
                   nameTransportProtocol(connection.family, connection.type),
                   *psutilAddrToIPAndPort(connection.laddr),
                   *psutilAddrToIPAndPort(connection.raddr),
                   statusBadValToGoodVal(connection.status)]
            self.net_connections.append(row)
        self.sortData()

    @Slot()
    def sortData(self):
        """ sorts model data """
        self.net_connections = sorted(self.net_connections, key=itemgetter(self.sortColumn), reverse=self.sortASC)

    def setSortColumn(self, column: int):
        """ set sorted column number"""
        if column > 0 or column < self.columnCount():
            self.sortColumn = column
        else:
            self.sortColumn = 0

    def setAscendingSort(self, flag: bool):
        """set ascending sort? """
        self.sortASC = flag

    def rowCount(self, parent = QModelIndex()):
        return len(self.net_connections)

    def columnCount(self, parent = QModelIndex()):
        if len(self.net_connections) == 0:
            return 0
        return len(self.net_connections[0])

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return TABLE_HEADERS[section]
        else:
            return f'{section}'

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            if row >= 0 and row < self.rowCount() \
                    and column >= 0 and column < self.columnCount():
                    return str(self.net_connections[row][column])
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight
        return None