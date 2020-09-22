import psutil
import socket
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex, Slot
from PySide2.QtGui import QColor
from operator import itemgetter
from work_with_list import lists_are_diff, tables_difference, updated_rows, get_of, new_primary_key
from work_with_netdata import (nameTransportProtocol, ipToDomainName, portToServiceName,
                               isZeroIPAddress, psutilAddrToIPAndPort, CacheDomainNames)


# class TLTableModel is model table for work with host's network connections on transport layer
class TLTableModel(QAbstractTableModel):
    MAX_PK = 2**64
    UNIQUE_KEY = tuple(i for i in range(2, 7))         # column numbers that uniquely identify a row in a table
    # All main headers in TLTableModel
    TABLE_HEADERS = ("Process", "PID", "Protocol", "Local Address", "Local Port",
                     "Remote Address", "Remote Port", "Status")
    SIGN_ASC = '⯅'
    SIGN_DESC = '⯆'
    DEFAULT_FILENAME = "net_connections"
    DEFAULT_EXTANSIONS = ('csv', 'txt')

    def __init__(self):
        super().__init__()
        self.setFilename(self.DEFAULT_FILENAME + '.' + self.DEFAULT_EXTANSIONS[0])
        self.__pk = -1                                  # value for generate primary key for table rows
        self.net_connections = []                       # main model table
        self.domainNameMode = True                      # return numeric address or domain name?
        self.cacheDomainNames = CacheDomainNames()      # for solved ip adresses to domain names for display in table
        self.serviceNameMode = True                     # return numeric port or service name?
        self.sortColumn = 0                             # sorted column number
        self.sortASC = True                             # ascending sort?
        # tuples primary keys deleted, created and updated rows
        self.del_pks = self.new_pks = self.chg_pks = tuple()
        # create function for count the number of rows status == "ESTABLISHED"
        self.countEstablished = self.__generateCountValueInTable(7, "ESTABLISHED")
        self.countListen = self.__generateCountValueInTable(7, "LISTEN")
        self.countCloseWait = self.__generateCountValueInTable(7, "CLOSE_WAIT")
        self.countTimeWait = self.__generateCountValueInTable(7, "TIME_WAIT")
        # load system data in self.net_connections
        self.updateData()

    def pk(self)-> int:
        self.__pk = new_primary_key(self.__pk, self.MAX_PK)
        return self.__pk

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
    def psutilConnectionToList(connection: psutil._common.sconn, pk_function = lambda:0) -> list:
        """ transfer psutil._common.sconn to list.
            pk_function - function for generate primary key values for table rows"""
        try:
            process = psutil.Process(connection.pid)
            return [process.name(), connection.pid, (connection.family, connection.type),
                    *psutilAddrToIPAndPort(connection.laddr, connection.family),
                    *psutilAddrToIPAndPort(connection.raddr, connection.family), connection.status,
                    pk_function()]
        except psutil.NoSuchProcess:
            return []

    @staticmethod
    def loadDataNetConnections(pk_function = lambda:0)-> list:
        """ load system data about all network connections on taransport layer and
            create data table.
            pk_function - function for generate primary key values for table rows"""
        net_connections = []
        for connection in psutil.net_connections():
            row = TLTableModel.psutilConnectionToList(connection, pk_function)
            if len(row) > 0:
                net_connections.append(row)
        return net_connections

    def removeRowByPK(self, pk: int):
        """ Function for remove row from
            table by primary key"""
        ind = -1
        for i in range(self.rowCount()):
            if self.primary_key(i) == pk:
                ind = i
                break
        if ind >= 0:
            self.net_connections.pop(ind)

    @Slot()
    def updateData(self):
        # notify the view of the begin of a radical change in data
        self.beginResetModel()
        # load system data about all network connections
        net_connections = TLTableModel.loadDataNetConnections(self.pk)
        # remove rows which were added from those deleted in the previous step
        for pk in self.del_pks:
            self.removeRowByPK(pk)
        del_rows = tables_difference(self.net_connections, net_connections, *TLTableModel.UNIQUE_KEY)
        new_rows = tables_difference(net_connections, self.net_connections, *TLTableModel.UNIQUE_KEY)
        chg_rows = updated_rows(self.net_connections, net_connections, TLTableModel.UNIQUE_KEY, (7,))
        self.del_pks = tuple(row[8] for row in del_rows)
        self.new_pks = tuple(row[8] for row in new_rows)
        self.chg_pks = tuple(row[8] for row in chg_rows)
        # append del_rows for display in tableview deleted rows
        self.net_connections = net_connections + del_rows
        # append in cache domain names created connections
        self.cacheDomainNames.append(
            *[(row[3], row[2][0]) for row in self.net_connections if row[3] not in self.cacheDomainNames],
            *[(row[5], row[2][0]) for row in self.net_connections if row[5] not in self.cacheDomainNames])
        self.sortData()
        # notify the view of the end of a radical change in data
        self.endResetModel()

    def unique_key(self, row: int)-> tuple:
        # a tuple of values that uniquely identifies a row in a table
        if not self.isRowValid(row):
            row = 0
        return get_of(self.net_connections[row], *TLTableModel.UNIQUE_KEY)

    def primary_key(self, row: int)-> int:
        # value that uniquely identifies a row in a table
        if not self.isRowValid(row):
            row = 0
        return self.net_connections[row][8]

    @Slot(bool)
    def setDomainNameMode(self, flag: bool):
        """ numeric address or domain name? """
        self.domainNameMode = flag

    @Slot(bool)
    def setServiceNameMode(self, flag: bool):
        """ numeric port or service name? """
        self.serviceNameMode = flag

    @Slot()
    def sortData(self):
        """ sorts model data """
        self.net_connections = sorted(self.net_connections, key=itemgetter(self.sortColumn), reverse=not self.sortASC)

    @Slot()
    def sortDataByColumn(self, column: int):
        """ set sorts model data by column """
        if not self.isColumnValid(column):
            return
        if column == self.sortColumn:
            self.sortASC = not self.sortASC
        else:
            self.sortASC = True
            self.sortColumn = column
        # self.sortData()               # If you need instant results. Сreates additional load

    def setSortColumn(self, column: int):
        """ set sorted column number"""
        if self.isColumnValid(column):
            self.sortColumn = column
        else:
            self.sortColumn = 0

    def setAscendingSort(self, flag: bool):
        """set ascending sort? """
        self.sortASC = flag

    def rowCount(self, parent = QModelIndex()):
        return len(self.net_connections)

    def columnCount(self, parent = QModelIndex()):
        if self.rowCount() == 0:
            return 0
        return len(self.net_connections[0]) - 1

    def headerData(self, section, orientation, role):
        """ return every column header """
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            header = self.TABLE_HEADERS[section]
            # mark the header by which the data is sorted
            if section == self.sortColumn:
                # + sort ascending; - sort descending;
                header += '  ' + (self.SIGN_ASC if self.sortASC else self.SIGN_DESC)
            return header
        else:
            return f'{section}'

    def data(self, index, role=Qt.DisplayRole):
        """ need for get data of model """
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            if column == 0:
                return self.processViewStr(row)
            elif column == 1:
                return self.pidViewStr(row)
            elif column == 2:
                return self.protocolViewStr(row)
            elif column == 3:
                return self.localAddressViewStr(row)
            elif column == 4:
                return self.localPortViewStr(row)
            elif column == 5:
                return self.remoteAddressViewStr(row)
            elif column == 6:
                return self.remotePortViewStr(row)
            elif column == 7:
                return self.statusViewStr(row)
        elif role == Qt.BackgroundRole:
            if self.primary_key(row) in self.new_pks:
                return QColor(Qt.green)
            elif self.primary_key(row) in self.chg_pks:
                return QColor(Qt.yellow)
            elif self.primary_key(row) in self.del_pks:
                return QColor(Qt.red)
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight
        return None

    def isRowValid(self, row: int)-> bool:
        return row >= 0 and row < self.rowCount()

    def isColumnValid(self, column: int)-> bool:
        return column >= 0 and column < self.columnCount()

    def realData(self, row: int, column: int):
        """ get real data of model """
        if self.isRowValid(row) and self.isColumnValid(column):
            return self.net_connections[row][column]
        else:
            return None

    def countEndpoints(self):
        return self.rowCount()

    def process(self, row: int) -> str:
        return self.realData(row, 0)

    def pid(self, row: int) -> int:
        return self.realData(row, 1)

    def protocol(self, row: int) -> tuple:
        return self.realData(row, 2)

    def localAddress(self, row: int) -> bytes:
        return self.realData(row, 3)

    def localDomainName(self, row: int) -> str:
        return ipToDomainName(socket.inet_ntop(self.realData(row, 2)[0], self.realData(row, 3)))

    def localPort(self, row: int) -> int:
        return self.realData(row, 4)

    def localServiceName(self, row: int) -> str:
        return portToServiceName(self.realData(row, 4), self.realData(row, 2)[1])

    def remoteAddress(self, row: int) -> bytes:
        return self.realData(row, 5)

    def remoteDomainName(self, row: int) -> str:
        return ipToDomainName(socket.inet_ntop(self.realData(row, 2)[0], self.realData(row, 5)))

    def remotePort(self, row: int) -> int:
        return self.realData(row, 6)

    def remoteServiceName(self, row: int) -> str:
        return portToServiceName(self.realData(row, 6), self.realData(row, 2)[1])

    def status(self, row: int)-> str:
        return self.realData(row, 7)

    def processViewStr(self, row: int)-> str:
        return self.process(row)

    def pidViewStr(self, row: int)-> str:
        return str(self.pid(row))

    def protocolViewStr(self, row: int)-> str:
        return nameTransportProtocol(*self.protocol(row))

    def localAddressViewStr(self, row: int)-> str:
        local_addr = self.localAddress(row)
        addr = socket.inet_ntop(self.protocol(row)[0], local_addr)
        return self.cacheDomainNames.domain_name(local_addr, addr) if self.domainNameMode else addr

    def localPortViewStr(self, row: int)-> str:
        port = self.localPort(row)
        return portToServiceName(port, self.protocol(row)[1]) if self.serviceNameMode else str(port)

    def remoteAddressViewStr(self, row: int) -> str:
        remote_addr = self.remoteAddress(row)
        protocol = self.protocol(row)
        if isZeroIPAddress(remote_addr, protocol[0]) and protocol[1] == socket.SOCK_DGRAM:
            return '*'
        addr = socket.inet_ntop(protocol[0], remote_addr)
        return self.cacheDomainNames.domain_name(remote_addr, addr) if self.domainNameMode else addr

    def remotePortViewStr(self, row: int)-> str:
        port = self.remotePort(row)
        ptype = self.protocol(row)[1]
        if port == 0 and ptype == socket.SOCK_DGRAM:
            return '*'
        return portToServiceName(port, ptype) if self.serviceNameMode else str(port)

    def statusViewStr(self, row: int)-> str:
        status = self.status(row)
        return '' if status == "NONE" else status

    def setFilename(self, filename: str) -> None:
        if filename != "":
            self._filename = filename

    def filename(self) -> str:
        return self._filename

    @Slot()
    def writeDataInFile(self)-> None:
        # print(self._filename)
        with open(self._filename, 'w') as file:
            for i in range(len(self.TABLE_HEADERS)):
                file.write(self.TABLE_HEADERS[i])
                if i < len(self.TABLE_HEADERS) - 1:
                    file.write(';')
            file.write('\n')
            for i in range(self.rowCount()):
                file.write(self.processViewStr(i) + ';')
                file.write(self.pidViewStr(i) + ';')
                file.write(self.protocolViewStr(i) + ';')
                file.write(self.localAddressViewStr(i) + ';')
                file.write(self.localPortViewStr(i) + ';')
                file.write(self.remoteAddressViewStr(i) + ';')
                file.write(self.remotePortViewStr(i) + ';')
                file.write(self.statusViewStr(i) + '\n')