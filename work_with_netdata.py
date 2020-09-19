import socket
import psutil
import threading

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

def psutilAddrToIPAndPort(paddr, pfamily: socket.AddressFamily)-> tuple:      # -> tuple(bytes, int)
    """ Correct result network address of psutil.net_connections() """
    if type(paddr) != tuple:
        ip, port = paddr.ip, paddr.port
    else:
        ip, port = ('::', 0) if pfamily == socket.AF_INET6 else ('0.0.0.0', 0)
    return socket.inet_pton(pfamily, ip), port

class CacheDomainNames:
    # Dictionary that stores domain names
    class DNRecord:
        # Data unit for CacheDomainNames that have simple structure
        def __init__(self, domain_name: str):
            self.domain_name = domain_name
            self.__count_refs = 0                   # the number of objects referring to this domain name
        def inc_refs(self):
            self.__count_refs += 1
        def dec_refs(self):
            if self.__count_refs > 0: self.__count_refs -= 1
        def count_refs(self)-> int:
            return self.__count_refs
        def zero_refs(self):
            self.__count_refs = 0
        def __str__(self):
            return "[" + str(self.domain_name) + ", " + str(self.__count_refs) + "]"
        def __repr__(self):
            return self.__str__()

    def __init__(self):
        self.__memory = {}
        cpu_count = psutil.cpu_count() - 1
        self.__MAX_COUNT_THREADS = cpu_count if cpu_count else 1
        self.__threads = []

    def append_ref(self, ip_addr: bytes, ip_family: socket.AddressFamily)-> None:
        if ip_addr not in self.__memory:
            self.__memory[ip_addr] = self.DNRecord(ipToDomainName(socket.inet_ntop(ip_family, ip_addr)))
            print(f'+ {ip_addr}: {self.__memory[ip_addr]}')
        self.__memory[ip_addr].inc_refs()

    def remove_ref(self, ip_addr: bytes)-> None:
        dnrecord = self.__memory.get(ip_addr, None)
        if dnrecord == None:
            return
        dnrecord.dec_refs()
        if dnrecord.count_refs() == 0:
            print(f'- {ip_addr}: {dnrecord}')
            self.__memory.pop(ip_addr, None)

    def clear_refs(self):
        self.__memory.clear()

    def domain_name(self, ip_addr: bytes, default = None)-> str:
        record = self.__memory.get(ip_addr, None)
        return record.domain_name if record else default

    def __append_refs(self, *addrs)-> None:                # addrs: tuple((bytes, socket.AddressFamily), ...)
        for addr in addrs:
            self.append_ref(addr[0], addr[1])

    def remove_refs(self, *addrs)-> None:               # addrs: tuple(bytes, ...)
        for addr in addrs:
            self.remove_ref(addr)

    def append_refs(self, *addrs)-> None:                 # addrs: tuple((bytes, socket.AddressFamily), ...)
        self.__free_dead_threads()
        running = self.__run_in_new_thread(self.__append_refs, *addrs)
        if not running:
            self.__append_refs(*addrs)

    def __free_dead_threads(self):
        for thread in self.__threads:
            if not thread.is_alive():
                self.__threads.remove(thread)

    def __run_in_new_thread(self, func, *args)-> bool:
        if len(self.__threads) < self.__MAX_COUNT_THREADS:
            thread = threading.Thread(target=func, args=args)
            self.__threads.append(thread)
            thread.start()
            return True
        return False

    def __len__(self):
        return len(self.__memory)

    def __str__(self):
        return self.__memory.__str__()

    def __repr__(self):
        return self.__memory.__repr__()