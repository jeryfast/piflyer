__author__ = 'Jernej'
from commander import commander
from comm import comm
import threading

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

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
            self.client.startVideoStream()
            data = self.client.readmsg()
            #new data available
            if data != None:
                status=self.commander.update(data)
                #TODO: key commands ack ... auto, alt hold, modes
            #Sends sensoric data to mobile device
            #elf.client.sendmsg(self.commander.sensors.getStrArr())

            t1=FuncThread(self.client.sendmsg,1,self.commander.sensors.getStrArr())
            t1.start()
            t1.join()
            #t2=threading.Thread(self.commander.control())
        self.commander.failsafe()
        self.client.reset()

        #self.client.sendmsg(self.commander.sensors.getStrArr())





