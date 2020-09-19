import socket
import psutil

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