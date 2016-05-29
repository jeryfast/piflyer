__author__ = 'Jernej'
from qrtools import QR
class qr():
    def read(self):
        myCode = QR()
        print(myCode.decode_webcam())
        #print(myCode.data)
        #print(myCode.data_type)
        #print(myCode.data_to_string())
        return myCode.data_to_string