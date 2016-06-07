__author__ = 'Jernej'
from commander import commander
from comm import comm
from threading import Thread
from time import sleep

class mainserver():
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
            #self.client.startVideoStream()
            data = self.client.readmsg()
            #new data available
            if data != '':
                status=self.commander.update(data)
                #TODO: key commands ack ... auto, alt hold, modes
            #Sends sensoric data to mobile device
            self.client.sendmsg(self.commander.sensors.getStrArr())
            #print(self.commander.sensors.getStrArr())
            self.commander.control()
        self.commander.failsafe()
        self.client.reset()






