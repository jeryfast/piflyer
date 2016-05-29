import sys

__author__ = 'Jernej'
import socks

#Comment if not running on raspberry pi
#import QRReader
from piflyer.ip_carrier import ip_carrier

TCP_PORT = 13000
BUFFER_SIZE = 20

class initclient:
    def __init__(self):
        #Comment if not running on raspberry pi
        #self.QR=QRReader.QR
        self.carrier=ip_carrier()

    def connect(self):
        try:
            #Save my IP address
            self.carrier.saveMyIP()

            #Get mobile device InitServer IP address from QR code
            #Comment if not running on raspberry pi
            #self.carrier.setMobileIp(self.QR.read())

            #try:
            #Connect to InitServer
            #Old
            #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.connect((self.carrier.getMobileIP(), TCP_PORT))
            #New
            s=socks.socksocket()
            s.set_proxy(socks.SOCKS5, self.carrier.getMyIP())
            s.connect(self.carrier.getMobileIP(),TCP_PORT)
            #except:
            #    print("Cannot connect to mobile device")
            #Send your own IP address
            s.send(self.carrier.getMyIP().encode("utf-8"))
            #Read feedback
            #data = s.recv(BUFFER_SIZE)
            #Close connection
            s.close()
        except:
            print(sys.exc_info())
            return False
        return True
