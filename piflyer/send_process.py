from multiprocessing import Process, Queue, Manager, current_process
import sys
from threading import Thread
import random as r
import time
from random import randint
from selenium import webdriver
import sys

#pi
from pyvirtualdisplay import Display

SEND=0
READ=1
END=2
REFRESH_DELAY=0.5

class sensors1(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon=True
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.compass= 10
        self.temp = 0
        self.humidity = 0
        self.pressure = 0
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.altitude = 0
    def run(self):
        while True:
            self.pitch = r.randint(3, 5)
            self.roll = r.randint(3, 5)
            self.yaw = r.randint(0, 2)
            self.compass = r.randint(240, 241)
            self.temp = r.randint(19, 20)
            self.humidity = r.randint(43, 46)
            self.pressure = r.randint(983, 985)
            self.ax = 0.1
            self.ay = 0.1
            self.az = 0.1
            self.altitude = 286
            time.sleep(REFRESH_DELAY)
    def getStrArr(self):
        return self.joinDelimiter([self.pitch, self.roll, self.yaw, self.compass, self.temp, self.humidity, self.pressure, self.ax, self.ay,
                                   self.az, self.altitude])
class commander1():
    def __init__(self):
        self.sensors = sensors1()

class comm1():
    def __init__(self):
        #pi
        #self.display = Display(visible=0, size=(480, 320))
        #self.display.start()
        firefox_profile = webdriver.FirefoxProfile()
        # firefox_profile = DesiredCapabilities.FIREFOX()
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        firefox_profile.set_preference("media.navigator.permission.disabled", True)
        self.datadriver = webdriver.Firefox(firefox_profile=firefox_profile)
        self.datadriver.get('http://peerclient.cloudapp.net/peer1.html')
        time.sleep(3)
        self.receiver = self.datadriver.find_element_by_id('receiver')
        self.connection = self.datadriver.find_element_by_id('connected')
        self.text = self.receiver.text
    def read(self):
        text = self.receiver.text
        print("rcv:",text)
    def send(self,data):
        self.datadriver.execute_script('sendstr("' + data[0] + '")')
    def close(self):
        self.datadriver.close()

#process class
class comm_process(Process):
    def __init__(self,q):
        super(comm_process, self).__init__()
        self.q=q
        self.start()
    def run(self):
        com = comm1()
        end = False
        t = 0
        DELAY = 0.02
        while True:
            if (not self.q.empty()):
                data = self.q.get()
                if (data[0] == SEND):
                    self.com.send(data[1:])
                elif (data[0] == READ):
                    self.com.read()
                elif (data[0] == END):
                    break
            time.sleep(DELAY)
        #com.display.stop()


def joinDelimiter(arr):
    tmp = [None] * len(arr)
    for i in range(len(arr)):
        tmp[i] = str(arr[i])
    return ",".join(tmp)

if __name__ == '__main__':
    q =  Queue()
    dataprocess = comm_process(q)

class mainserver1():
    def __init__(self):
        self.commander1 = commander1()
        print("starting sensor readings")
        self.commander1.sensors.start()

    def run(self):
            while (1):
                pitch = randint(3, 5)
                roll = randint(3, 5)
                yaw = randint(0, 2)
                compass = randint(240, 241)
                temp = randint(19, 20)
                humidity = randint(43, 46)
                pressure = randint(983, 985)
                ax = 0.1
                ay = 0.1
                az = 0.1
                altitude = 286
                q.put([SEND, joinDelimiter([pitch, roll, yaw, compass, temp, humidity, pressure, ax, ay,
                                            az, altitude])])
                q.put([READ])
                time.sleep(0.05)
                if __name__ == '__main__':
                    while (1):
                        # print("thread:", threading.get_ident())
                        # 0-send
                        # 1-read
                        pitch = randint(3, 5)
                        roll = randint(3, 5)
                        yaw = randint(0, 2)
                        compass = randint(240, 241)
                        temp = randint(19, 20)
                        humidity = randint(43, 46)
                        pressure = randint(983, 985)
                        ax = 0.1
                        ay = 0.1
                        az = 0.1
                        altitude = 286
                        q.put([SEND, joinDelimiter([pitch, roll, yaw, compass, temp, humidity, pressure, ax, ay,
                                                    az, altitude])])
                        q.put([1])
                        time.sleep(0.05)
                    sys.exit(0)

if __name__ == '__main__':
    s = mainserver1()
    print("Starting main server ...")
    while 1:
        try:
            s.run()
        except:
            print(sys.exc_info())
    sys.exit(0)
"""
if __name__ == '__main__':
    q = Queue()
    dataprocess=process(q)
    #p = Process(target=dataprocess.run,args=(q,))
    if __name__ == '__main__':
        while(1):
            #print("thread:", threading.get_ident())
            #0-send
            #1-read
            pitch = randint(3, 5)
            roll = randint(3, 5)
            yaw = randint(0, 2)
            compass = randint(240, 241)
            temp = randint(19, 20)
            humidity = randint(43, 46)
            pressure = randint(983, 985)
            ax = 0.1
            ay = 0.1
            az = 0.1
            altitude = 286
            q.put([SEND,joinDelimiter([pitch, roll, yaw, compass, temp, humidity,pressure, ax, ay,
                                   az, altitude])])
            #q.put([0,joinDelimiter([randint(0, 180), randint(0, 180), randint(0, 180)])])
            #q.put([0,joinDelimiter([randint(0, 180), randint(0, 180), randint(0, 180)])])
            #q.put([0,joinDelimiter([randint(0, 180), randint(0, 180), randint(0, 180)])])
            #q.put([0,joinDelimiter([randint(0, 180), randint(0, 180), randint(0, 180)])])
            #q.put([0,randint(0, 180), randint(0, 180), randint(0, 180)])
            q.put([1])
            time.sleep(0.05)
        sys.exit()
"""