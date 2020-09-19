import socket
import psutil
import threading
import time

ZERO_IPV4 = bytes([0] * 4)
ZERO_IPV6 = bytes([0] * 16)
LIFETIME_DNRECORD = 120         # the number of seconds the entry is valid, default 2 minutes

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

def psutilAddrToIPAndPort(paddr, pfamily: socket.AddressFamily)-> tuple:      # -> tuple(bytes, int)
    """ Correct result network address of psutil.net_connections() """
    if type(paddr) != tuple:
        ip, port = paddr.ip, paddr.port
    else:
        ip, port = ('::', 0) if pfamily == socket.AF_INET6 else ('0.0.0.0', 0)
    return socket.inet_pton(pfamily, ip), port


class CacheDomainNames:
    """ Class for working with domain names cache.
        It is a more optimal solution in contrast to simple
        functions for calculating domain names as needed. """
    class DNRecord:
        # Data unit for CacheDomainNames that have simple structure
        def __init__(self, domain_name: str, lifetime: float):
            # lifetime - the number of seconds the entry is valid
            self.domain_name = domain_name
            self.__death_time = time.time() + lifetime         # time when the entry will no longer be valid

        def is_alive(self)-> bool:
            return time.time() < self.__death_time

        def set_death_time(self, val: float)-> None:
            if val > 0:
                self.__death_time = val
            else:
                self.__death_time = 0

        def __str__(self):
            return "[" + str(self.domain_name) + ", " + str(self.__death_time) + " sec]"

        def __repr__(self):
            return self.__str__()

    def __init__(self, lifetime_record = LIFETIME_DNRECORD):
        """ Initialization memory and setting basic configurations"""
        self.__memory = {}                                      # dictionary that stores DNRecords
        self.__lifetime_record = lifetime_record                # the number of seconds the entry is valid
        cpu_count = psutil.cpu_count() - 1
        self.__MAX_COUNT_THREADS = cpu_count if cpu_count else 1
        self.__threads = []

    def domain_name(self, ip_addr: bytes, default = None)-> str:
        """ Return domain name of memory """
        record = self.__memory.get(ip_addr, None)
        return record.domain_name if record else default

    def __append(self, ip_addr: bytes, ip_family: socket.AddressFamily)-> None:
        """ function of adding one record to the cache """
        if ip_addr not in self.__memory:
            # resolve ip address into domain name and write to cache
            self.__memory[ip_addr] = self.DNRecord(ipToDomainName(socket.inet_ntop(ip_family, ip_addr)),
                                                                                    self.__lifetime_record)

    def __appends(self, *addrs)-> None:                # addrs: tuple((bytes, socket.AddressFamily), ...)
        """ function of adding multiple records to cache """
        for addr in addrs:
            self.__append(addr[0], addr[1])

    def append(self, *addrs)-> None:                 # addrs: tuple((bytes, socket.AddressFamily), ...)
        """ function of adding multiple records to cache
            and works in multi-threaded mode"""
        self.__remove_dead_threads()
        self.__remove_dead_domain_names()
        # filter out addresses that are already being examined by other threads
        addrs = self.__addrs_not_in_thread_works(*addrs)
        # try run function 'append' in new thread
        running = self.__run_in_new_thread(self.__appends, *addrs)
        if not running:
            self.__appends(*addrs)

    def __addrs_not_in_thread_works(self, *addrs):
        """ The function looks for addresses that
            are not currently calculated by other threads."""
        need_addrs = []         # addresses not involved in settlement
        for addr in addrs:
            flag = True
            for thread in self.__threads:
                if addr in thread.work:
                    flag = False
                    break
            if flag:
                need_addrs.append(addr)
        return need_addrs

    def __remove_dead_domain_names(self):
        """ Removes all domain names
            from the cache that have expired """
        keys = [key for key in self.__memory if not self.__memory[key].is_alive()]
        for key in keys:
            dnrecord = self.__memory.pop(key, None)

    def clear(self):
        """ Removes all domain names from the cache """
        self.__memory.clear()

    def set_lifetime_record(self, lifetime: float)-> None:
        if lifetime > 0:
            self.__lifetime_record = lifetime
        else:
            self.__lifetime_record = 0

    def lifetime_record(self)-> float:
        return self.__lifetime_record

    def __contains__(self, key):
        return key in self.__memory

    def __len__(self):
        return len(self.__memory)

    def __str__(self):
        return self.__memory.__str__()

    def __repr__(self):
        return self.__memory.__repr__()

    def __remove_dead_threads(self):
        """ Removes all thread that finished work """
        for thread in self.__threads:
            if not thread.is_alive():
                self.__threads.remove(thread)

    def __run_in_new_thread(self, func, *args)-> bool:
        """ Runs a function on a new thread.
            return:
               False - cannot be started since the number
                       of threads is equal to the number of logical cores
               True - function run in new thread"""
        if len(self.__threads) < self.__MAX_COUNT_THREADS:
            thread = threading.Thread(target=func, args=args, daemon=True)
            thread.work = args
            self.__threads.append(thread)
            thread.start()
            return True
        return False