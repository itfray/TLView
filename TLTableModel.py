from operator import itemgetter
import psutil
import socket
import struct
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex, Slot
from PySide2.QtGui import QColor


def nameTransportProtocol(family: socket.AddressFamily, type: socket.SocketKind)-> str:
    if type == socket.SOCK_STREAM:
        ans = "TCP"
    else:
        ans = "UDP"
    if family == socket.AF_INET6:
        ans += "V6"
    return ans

def psutilAddrToIPAndPort(paddr, pfamily)-> tuple:      # -> tuple(bytes, int)
    """
        Correct result network address of psutil.net_connections()
    """
    if type(paddr) != tuple:
        ip, port = paddr.ip, paddr.port
    else:
        ip, port = ('::', 0) if pfamily == socket.AF_INET6 else ('0.0.0.0', 0)
    return socket.inet_pton(pfamily, ip), port


def IPToViewStr(ip: bytes, family: socket.AddressFamily, type: socket.SocketKind)-> str:
    zero_ip = bytes([0]*4) if family != socket.AF_INET6 else bytes([0]*16)
    if ip == zero_ip:
        if type == socket.SOCK_DGRAM:
            return "*"
    return socket.inet_ntop(family, ip)

def portToViewStr(port: int, type: socket.SocketKind)-> str:
    if port == 0:
        if type == socket.SOCK_DGRAM:
            return "*"
    return str(port)

statusToViewStr = lambda val: '' if val == "NONE" else val

def generateCountValueInTable(table, column, value):
    """
        creates a function that counts the number of rows
        that have a specific value in a particular column
    """
    def countValueInTable():
        count = 0
        for row in table:
            if row[column] == value:
                count += 1
        return count
    return countValueInTable

# All main headers in TLTableModel
TABLE_HEADERS = ("Process", "PID", "Protocol", "Local Address", "Local Port",
                 "Remote Address", "Remote Port", "State")

# class TLTableModel is model table for work with host's network connections on transport layer
class TLTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.net_connections = []
        self.sortColumn = 0         # sorted column number
        self.sortASC = False        # ascending sort?
        self.countEstablished = generateCountValueInTable(self.net_connections, 7, "ESTABLISHED")
        self.countListen = generateCountValueInTable(self.net_connections, 7, "LISTEN")
        self.countCloseWait = generateCountValueInTable(self.net_connections, 7, "CLOSE_WAIT")
        self.countTimeWait = generateCountValueInTable(self.net_connections, 7, "TIME_WAIT")
        self.updateData()


    @Slot()
    def updateData(self):
        """
            load system data about all network connections on taransport layer and
            create data table
        """
        # notify the view of the begin of a radical change in data
        self.beginResetModel()
        self.net_connections = []
        # create data table
        for connection in psutil.net_connections():
            try:
                process = psutil.Process(connection.pid)
            except psutil.NoSuchProcess:
                continue
            row = [process.name(), connection.pid, (connection.family, connection.type),
                   *psutilAddrToIPAndPort(connection.laddr, connection.family),
                   *psutilAddrToIPAndPort(connection.raddr, connection.family), connection.status]
            self.net_connections.append(row)
        self.sortData()
        # notify the view of the end of a radical change in data
        self.endResetModel()

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
                if column == 2:
                    return nameTransportProtocol(*self.net_connections[row][column])
                elif column == 3 or column == 5:
                    return IPToViewStr(self.net_connections[row][column], *self.net_connections[row][2])
                elif column == 6:
                    return portToViewStr(self.net_connections[row][column], self.net_connections[row][2][1])
                elif column == 7:
                    return statusToViewStr(self.net_connections[row][column])
                return str(self.net_connections[row][column])
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight
        return None

    def countEndpoints(self):
        return self.rowCount()