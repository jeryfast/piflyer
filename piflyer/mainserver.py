__author__ = 'Jernej'
from commander import commander
from comm import comm
import threading
import time


def processingTime(t0):
    return time.time() - t0

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
                self.client.sendMsg(self.commander.sensors.getStrArr())
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
        #self.sendThread=dataSendingThread(self.client, self.commander)
        #self.sendThread = m.Process(target=sendData, args=(self.client,self.commander))
        #self.sendThread.start()
        #self.controlThread=controlThread(self.commander)
        print("starting sensor readings")
        self.commander.sensors.start()



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
            print("readmsg",processingTime(t0))

            t0=time.time()
            #new data available
            if data != None:
                status=self.commander.update(data)
                #TODO: key commands ack ... auto, alt hold, modes
            print("update",processingTime(t0))

            t0=time.time()
            #Sends sensoric data to mobile device
            #should run in its own thread, independent, sending data as fast as possible
            self.client.sendMsg(self.commander.sensors.getStrArr())
            print("sendmsg",processingTime(t0))

            t0 = time.time()
            self.commander.control()
            print("control", processingTime(t0))
            #self.controlThread.start()
            time.sleep(0.5)
        #self.sendThread.stopStream()
        print("out of while ")
        #self.sendThread.event.clear()
        #self.controlThread.event.clear()
        #self.commander.failsafe()
        self.client.reset()







