__author__ = 'Jernej'
from commander import commander
from comm import comm
import threading

def mainserver():
    def __init__(self):
        #Thread.__init__(self)
        self.client=comm()
        self.commander=commander()
        #self.start()

    def run(self):
        status=""
        data=""
        #while connection not broken by client
        #while result!=c.DISCONNECT:
        while self.client.connected():
            self.client.startVideoStream()
            data = self.client.readmsg()
            #new data available
            if data != None:
                status=self.commander.update(data)
                #TODO: key commands ack ... auto, alt hold, modes
            #Sends sensoric data to mobile device
            t1=threading.Thread(target=self.client.sendmsg(),args=self.commander.sensors.getStrArr())
            t2=threading.Thread(self.commander.control())
            t1.start()
            t2.start()
        self.commander.failsafe()
        self.client.reset()

        #self.client.sendmsg(self.commander.sensors.getStrArr())





