import psutil
import socket
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex, Slot
from PySide2.QtGui import QColor
from operator import itemgetter
from work_with_list import lists_are_diff, tables_difference, updated_rows
from work_with_netdata import (nameTransportProtocol, ipToDomainName, portToServiceName,
                               isZeroIPAddress, psutilAddrToIPAndPort)

# class TLTableModel is model table for work with host's network connections on transport layer
class TLTableModel(QAbstractTableModel):
    UNIQUE_KEY = tuple(i for i in range(2, 7))         # column numbers that uniquely identify a row in a table
    # All main headers in TLTableModel
    TABLE_HEADERS = ("Process", "PID", "Protocol", "Local Address", "Local Port",
                     "Remote Address", "Remote Port", "Status")

    def __init__(self):
        super().__init__()
        self.net_connections = []               # main model table
        self.domainNameMode = True              # return numeric address or domain name?
        self.cacheDomainNames = {}
        self.serviceNameMode = True             # return numeric port or service name?
        self.sortColumn = 0                     # sorted column number
        self.sortASC = False                    # ascending sort?
        self.deleted_rows = self.created_rows = self.updated_rows = []
        # create function for count the number of rows status == "ESTABLISHED"
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

    @staticmethod
    def psutilConnectionToList(connection: psutil._common.sconn) -> list:
        """ transfer psutil._common.sconn to list """
        try:
            process = psutil.Process(connection.pid)
            return [process.name(), connection.pid, (connection.family, connection.type),
                    *psutilAddrToIPAndPort(connection.laddr, connection.family),
                    *psutilAddrToIPAndPort(connection.raddr, connection.family), connection.status]
        except psutil.NoSuchProcess:
            return []

    @staticmethod
    def statusToViewStr(val: str) -> str:
        return '' if val == "NONE" else val

    @Slot()
    def updateData(self):
        """ load system data about all network connections on taransport layer and
            create data table """
        # notify the view of the begin of a radical change in data
        self.beginResetModel()
        # create data table
        net_connections = []
        for connection in psutil.net_connections():
            row = TLTableModel.psutilConnectionToList(connection)
            if len(row) > 0:
                net_connections.append(row)
        self.deleted_rows = tables_difference(self.net_connections, net_connections, *TLTableModel.UNIQUE_KEY)
        self.created_rows = tables_difference(net_connections, self.net_connections, *TLTableModel.UNIQUE_KEY)
        self.updated_rows = updated_rows(self.net_connections, net_connections, TLTableModel.UNIQUE_KEY, (7,))
        self.net_connections = net_connections
        # remove from cache domain names deleted connections
        for row in self.deleted_rows:
            self.cacheDomainNames[row[3]][1] -= 1
            self.cacheDomainNames[row[5]][1] -= 1
            if self.cacheDomainNames[row[3]][1] == 0:
                print(f'- {row[3]}: {self.cacheDomainNames.get(row[3], None)}')
                self.cacheDomainNames.pop(row[3], None)
            if self.cacheDomainNames[row[5]][1] == 0:
                print(f'- {row[5]}: {self.cacheDomainNames.get(row[5], None)}')
                self.cacheDomainNames.pop(row[5], None)
        # append in cache domain names created connections
        for row in self.created_rows:
            if row[3] not in self.cacheDomainNames:
                self.cacheDomainNames[row[3]] = [ipToDomainName(socket.inet_ntop(row[2][0], row[3])), 0]
                print(f'+ {row[3]}: {self.cacheDomainNames.get(row[3], None)}')
            self.cacheDomainNames[row[3]][1] += 1
            if row[5] not in self.cacheDomainNames:
                self.cacheDomainNames[row[5]] = [ipToDomainName(socket.inet_ntop(row[2][0], row[5])), 0]
                print(f'+ {row[5]}: {self.cacheDomainNames.get(row[5], None)}')
            self.cacheDomainNames[row[5]][1] += 1

        self.sortData()
        # notify the view of the end of a radical change in data
        self.endResetModel()
        print(f'deleted = {self.deleted_rows}')
        print(f'created = {self.created_rows}')
        print(f'updated = {self.updated_rows}')
        print(f'cache = {self.cacheDomainNames}')
        print(f'len cache: {len(self.cacheDomainNames)}')
        print()

    def unique_key(self, row: int)-> tuple:
        # a tuple of values ​​that uniquely identifies a row in a table
        return tuple(self.net_connections[row][column] for column in TLTableModel.UNIQUE_KEY)

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
                        return self.cacheDomainNames.get(self.net_connections[row][column], ('',))[0]
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
                    return TLTableModel.statusToViewStr(self.net_connections[row][column])
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