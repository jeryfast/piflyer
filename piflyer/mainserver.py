__author__ = 'Jernej'
from commander import commander
from comm import comm
import threading
from multiprocessing import Process
from time import time

class dataSendingThread(threading.Thread):
    def __init__(self,myclient,mycommander):
        threading.Thread.__init__(self)
        self.daemon = True
        self.client=myclient
        self.commander=mycommander
        self.event=threading.Event()
        self.start()

    def run(self):
        while True:
            self.event.wait()
            try:
                self.client.sendmsg(self.commander.sensors.getStrArr())
            except:
                print("Sending thread exception")



class controlThread(threading.Thread):
    def __init__(self, mycommander):
        threading.Thread.__init__(self)
        self.daemon = True
        self.commander = mycommander
        self.freq = 10
        self.event=threading.Event()
        self.start()

    def run(self):
        while True:
            self.event.wait()
            try:
                self.commander.control()
            except:
                print("Commander thread exception")

class mainserver():
    def __init__(self):
        self.client=comm()
        self.commander=commander()
        self.sendThread=dataSendingThread(self.client, self.commander)
        #self.controlThread=controlThread(self.commander)

    def run(self):
        status=""
        data=""
        while self.client.connected():
            self.sendThread.event.set()
            #self.controlThread.event.set()
            self.client.startVideoStream()
            #print("read ",threading.current_thread())
            data = self.client.readmsg()
            #new data available
            if data != None:
                status=self.commander.update(data)
                #TODO: key commands ack ... auto, alt hold, modes
            #Sends sensoric data to mobile device
            #should run in its own thread, independent, sending data as fast as possible
            #self.client.sendmsg(self.commander.sensors.getStrArr())
            self.commander.control()
            #self.controlThread.start()
        #self.sendThread.stopStream()
        print("not connected ",threading.current_thread())
        self.sendThread.event.clear()
        #self.controlThread.event.clear()
        #self.commander.failsafe()
        self.client.reset()






