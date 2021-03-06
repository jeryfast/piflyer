__author__ = 'Jernej'
from commander import commander
from comm import comm
import threading
import time

class mainserver():
    def __init__(self):
        self.client=comm()
        self.commander=commander()
        #self.sendThread=dataSendingThread(self.client, self.commander)
        #self.sendThread = m.Process(target=sendData, args=(self.client,self.commander))
        #self.sendThread.start()
        #self.controlThread=controlThread(self.commander)
        print("starting sensor readings")
        #self.commander.sensors.start()
        self.printDelay=0

    def processingTime(self,t0, name):
        t=round(time.time(),2)
        if t-self.printDelay>0.5:
            self.printDelay=t
            print(name,time.time() - round(t0,2))

    def run(self):
        status=""
        data=""
        while self.client.connected():
            #self.sendThread.event.set()
            #self.controlThread.event.set()
            #self.client.startVideoStream()
            #print("read ",threading.current_thread())

            t0 = time.time()
            data = self.client.readMsg()
            #data="C,10,0"
            self.processingTime(t0,"readmsg")

            t0=time.time()
            #new data available
            if data != None:
                #status=self.commander.update(data)
                pass
                #TODO: key commands ack ... auto, alt hold, modes
            self.processingTime(t0,"update")

            t0=time.time()
            #Sends sensoric data to mobile device
            #should run in its own thread, independent, sending data as fast as possible
            self.client.sendMsg(self.commander.sensors.getStrArr())
            self.processingTime(t0,"sendmsg")

            t0 = time.time()
            self.commander.control()
            self.processingTime(t0,"control")

            #self.controlThread.start()
        #self.sendThread.stopStream()
        #self.sendThread.event.clear()
        #self.controlThread.event.clear()
        #self.commander.failsafe()
        self.client.reset()







