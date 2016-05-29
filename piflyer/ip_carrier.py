from _csv import reader

__author__ = 'Jernej'
import socket
from json import loads
from urllib.request import urlopen

ERROR="IP address not valid"
OK="Valid"
class ip_carrier:
    def __init__(self):
        #if testing on PC enter mobileIp manually
        #self.mobileIp="10.71.34.101"
        self.mobileIp="192.168.1.64"
        self.myIp=""

    def setMobileIp(self,mIP):
        if(self.is_valid_ipv4_address(mIP)):
            self.mobileIp=mIP
        elif(self.is_valid_ipv6_address(mIP)):
            self.mobileIp=mIP
        else:
            return ERROR
        return OK

    def getMobileIP(self):
        return self.mobileIp

    def setMyIP(self,IP):
        self.myIp=IP

    def getMyIP(self):
        return self.myIp

    def saveMyIP(self):
        mip = loads(urlopen('https://api.ipify.org/?format=json').read().decode('utf-8'))['ip']
        self.setMyIP(mip)

    def is_valid_ipv4_address(address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return False
        return True

    def is_valid_ipv6_address(address):
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return False
        return True


