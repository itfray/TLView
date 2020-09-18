from operator import itemgetter
import psutil
import socket
import struct
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex, Slot
from PySide2.QtGui import QColor

ZERO_IPV4 = bytes([0] * 4)
ZERO_IPV6 = bytes([0] * 16)

def nameTransportProtocol(family: socket.AddressFamily, type: socket.SocketKind)-> str:
    """ Return str representation name transport protocol """
    if type == socket.SOCK_STREAM:
        ans = "TCP"
    else:
        ans = "UDP"
    if family == socket.AF_INET6:
        ans += "V6"
    return ans

def ipToDomainName(addr: str)-> str:
    try:
        return socket.gethostbyaddr(addr)[0]
    except (socket.herror, socket.gaierror):
        return addr

def portToServiceName(port: int, type: socket.SocketKind)-> str:
    try:
        return socket.getservbyport(port, 'tcp' if type == socket.SOCK_STREAM else 'udp')
    except OSError:
        return str(port)

def isZeroIPAddress(addr: bytes, family: socket.AddressFamily)-> bool:
    return addr == (ZERO_IPV4 if family != socket.AF_INET6 else ZERO_IPV6)

def statusToViewStr(val: str) -> str:
    return '' if val == "NONE" else val

def psutilAddrToIPAndPort(paddr, pfamily: socket.AddressFamily)-> tuple:      # -> tuple(bytes, int)
    """ Correct result network address of psutil.net_connections() """
    if type(paddr) != tuple:
        ip, port = paddr.ip, paddr.port
    else:
        ip, port = ('::', 0) if pfamily == socket.AF_INET6 else ('0.0.0.0', 0)
    return socket.inet_pton(pfamily, ip), port

def psutilConnectionToList(connection: psutil._common.sconn)-> list:
    """ transfer psutil._common.sconn to list """
    try:
        process = psutil.Process(connection.pid)
        return [process.name(), connection.pid, (connection.family, connection.type),
               *psutilAddrToIPAndPort(connection.laddr, connection.family),
               *psutilAddrToIPAndPort(connection.raddr, connection.family), connection.status]
    except psutil.NoSuchProcess:
        return []

# class TLTableModel is model table for work with host's network connections on transport layer
class TLTableModel(QAbstractTableModel):
    # All main headers in TLTableModel
    TABLE_HEADERS = ("Process", "PID", "Protocol", "Local Address", "Local Port",
                     "Remote Address", "Remote Port", "Status")

    def __init__(self):
        super().__init__()
        self.net_connections = []   # main model table
        self.domainNameMode = False # return numeric address or domain name?
        # self.cacheDomainNames = {}
        self.serviceNameMode = True # return numeric port  or service name?
        self.sortColumn = 0         # sorted column number
        self.sortASC = False        # ascending sort?
        # create function for count the number of rows status == STATUS_VALUES[1]
        self.countEstablished = self.__generateCountValueInTable(7, "ESTABLISHED")
        self.countListen = self.__generateCountValueInTable(7, "LISTEN")
        self.countCloseWait = self.__generateCountValueInTable(7, "CLOSE_WAIT")
        self.countTimeWait = self.__generateCountValueInTable(7, "TIME_WAIT")
        # load system data in self.net_connections
        self.updateData()

    def __generateCountValueInTable(self, column, value):
        """ This method creates a function-method for TLTableModel that counts the number of rows
            that have a specific value in a particular column """
        def countValueInTable():
            count = 0
            for row in self.net_connections:
                if row[column] == value:
                    count += 1
            return count
        return countValueInTable

    @Slot()
    def updateData(self):
        """ load system data about all network connections on taransport layer and
            create data table """
        # notify the view of the begin of a radical change in data
        self.beginResetModel()
        net_connections = []
        # create data table
        for connection in psutil.net_connections():
            row = psutilConnectionToList(connection)
            if len(row) > 0:
                net_connections.append(row)

        # def listsIsDifferent(list1, list2, *indexes):
        #     """ The function checks the differences of lists at the specified indices. """
        #     if len(list1) != len(list2):
        #         raise ValueError("Lists should have same length!!!")
        #     count = 0
        #     for index in indexes:
        #         if list1[index] != list2[index]:
        #             count += 1
        #     return count > 0

        # def tablesDifference(table1: list, table2: list, *columns)-> list:
        #     """ The function searches for rows of the first table that are not in the second table. """
        #     answer = []
        #     for i in range(len(table1)):
        #         count = 0
        #         for j in range(len(table2)):
        #             if listsIsDifferent(table1[i], table2[j], *columns):
        #                 count += 1
        #         if count == len(table2):
        #             answer.append(table1[i])
        #     return answer

        # def updatedRows(old_table: list, new_table: list, indexes_id: tuple, indexes_cmp: tuple)-> list:
        #     """ The function сhecks the rows of the old table that are updated in the new table.
        #         * old_table - old table; new_table - new table;
        #           indexes_id - indexes identifying a row in a table;
        #           indexes_cmp - data indexes in which to compare. These are the indices of the elements
        #           for which the data could be updated;"""
        #     answer = []
        #     for i in range(len(old_table)):
        #         for j in range(len(new_table)):
        #             if not listsIsDifferent(old_table[i], new_table[j], *indexes_id) and \
        #                     listsIsDifferent(old_table[i], new_table[j], *indexes_cmp):
        #                 answer.append(old_table[i])
        #
        # deleted = tablesDifference(self.net_connections, net_connections, 2, 3, 4, 5, 6)
        # created = tablesDifference(net_connections, self.net_connections, 2, 3, 4, 5, 6)
        # updated = updatedRows(self.net_connections, net_connections, (1, 2, 3, 4, 5, 6), (7,))

        self.net_connections = net_connections
        self.sortData()
        # notify the view of the end of a radical change in data
        self.endResetModel()

    def setDomainNameMode(self, flag: bool):
        """ numeric address or domain name? """
        self.domainNameMode = flag

    def setServiceNameMode(self, flag: bool):
        """ numeric port or service name? """
        self.serviceNameMode = flag

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
        """ return every column header """
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.TABLE_HEADERS[section]
        else:
            return f'{section}'

    def data(self, index, role=Qt.DisplayRole):
        """ need for get data of model """
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            if row >= 0 and row < self.rowCount() \
                    and column >= 0 and column < self.columnCount():
                if column == 2:
                    return nameTransportProtocol(*self.net_connections[row][column])
                elif column == 3 or column == 5:
                    if column == 5:
                        if isZeroIPAddress(self.net_connections[row][column], self.net_connections[row][2][0]) and \
                                self.net_connections[row][2][1] == socket.SOCK_DGRAM:
                            return '*'
                    addr = socket.inet_ntop(self.net_connections[row][2][0], self.net_connections[row][column])
                    if self.domainNameMode:
                        return ipToDomainName(addr)
                    return addr
                elif column == 4 or column == 6:
                    if column == 6:
                        if self.net_connections[row][column] == 0 and \
                                self.net_connections[row][2][1] == socket.SOCK_DGRAM:
                            return '*'
                    if self.serviceNameMode:
                        return portToServiceName(self.net_connections[row][column], self.net_connections[row][2][1])
                    return str(self.net_connections[row][column])
                elif column == 7:
                    return statusToViewStr(self.net_connections[row][column])
                return str(self.net_connections[row][column])
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight
        return None

    def realData(self, row: int, column: int):
        """ get real data of model """
        if row < 0 or row >= self.rowCount() \
                or column < 0 or column >= self.columnCount():
            return None
        return self.net_connections[row][column]

    def countEndpoints(self):
        return self.rowCount()

    def process(self, row: int):
        return self.realData(row, 0)

    def pid(self, row: int):
        return self.realData(row, 1)

    def protocol(self, row: int):
        return self.realData(row, 2)

    def localAddress(self, row: int):
        return self.realData(row, 3)

    def localPort(self, row: int):
        return self.realData(row, 4)

    def remoteAddress(self, row: int):
        return self.realData(row, 5)

    def remotePort(self, row: int):
        return self.realData(row, 6)

    def status(self, row: int):
        return self.realData(row, 7)