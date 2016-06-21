import zmq
import random
import time
import zmq_ports as ports
import zmq_topics as topic
from selenium import webdriver
import os
from pyvirtualdisplay import Display
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from websocket import create_connection
import delays

RCV_DELAY=0.01
WSPORT = 9000

class comm():
    def __init__(self):
        try:
            #linux
            self.display = Display(visible=0, size=(480, 320))
            self.display.start()
        except:
            #windows
            pass
        fp = webdriver.FirefoxProfile()
        fp.set_preference('permissions.default.stylesheet', 2)
        fp.set_preference('permissions.default.image', 2)
        fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        fp.set_preference("media.navigator.permission.disabled", True)
        fp.set_preference("browser.startup.homepage", "about:blank")
        fp.set_preference("startup.homepage_welcome_url", "about:blank")
        fp.set_preference("startup.homepage_welcome_url.additional", "about:blank")

        binary = FirefoxBinary('/usr/bin/iceweasel')

        fp1 = webdriver.FirefoxProfile()
        fp1.set_preference('permissions.default.stylesheet', 2)
        fp1.set_preference('permissions.default.image', 2)
        fp1.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        fp1.set_preference("media.navigator.permission.disabled", True)
        fp1.set_preference("browser.startup.homepage", "about:blank")
        fp1.set_preference("startup.homepage_welcome_url", "about:blank")
        fp1.set_preference("startup.homepage_welcome_url.additional", "about:blank")

        try:
            #linux
            self.datadriver = webdriver.Firefox(firefox_profile=fp,firefox_binary=binary)
            self.videodriver=webdriver.Firefox(firefox_profile=fp1, firefox_binary=binary)
        except:
            #windows, for testing
            self.datadriver=webdriver.Firefox(firefox_profile=fp)
            #self.videodriver = webdriver.Firefox(firefox_profile=fp1)
        self.datadriver.set_window_size(480, 320)
        #self.videodriver.set_window_size(480, 320)

        self.start()
        self.getids()
        self.streaming=False
        self.lastmsg= ""
        self.connchecktime=0
        self.sendtimer=0
        self.rcvtimer=0
        self.isConnected=False

    def start(self):
        url="file:"+os.getcwd()+os.sep+'peer1.html'
        self.datadriver.get(url)
        #self.videodriver.get(url)

    def getids(self):
        try:
            # time.sleep(3)
            self.msg = self.datadriver.find_element_by_id('msg')
            self.sender = self.datadriver.find_element_by_id('sender')
            self.receiver = self.datadriver.find_element_by_id('receiver')
            self.connection = self.datadriver.find_element_by_id('connected')
            #self.videoswitch = self.videodriver.find_element_by_id('videoswitch')
        except:
            pass

    def reset(self):
        try:
            if (self.datadriver.find_element_by_id('refresh').text != 'false'):
                print("refreshing")
                self.datadriver.execute_script("location.reload();")
                #self.videodriver.execute_script("location.reload();")
                self.getids()
                time.sleep(2)
                self.streaming = False
        except:
            print("reset failed")

    def connected(self):
        # print("check-connected")
        self.isConnected = True
        t = round(time.time(), 1)
        if (t - self.connchecktime > 1 and t - self.rcvtimer > 3):
            self.connchecktime = round(t, 1)
            text = ""
            try:
                text = self.connection.text
            except:
                self.isConnected = False
            if (text != "true"):
                self.isConnected = False
        return self.isConnected

    def readMsg(self):
        result = None
        t0 = time.time()
        if (t0 - self.rcvtimer > RCV_DELAY):
            try:
                text = self.receiver.text
                if (text != self.lastmsg):
                    t = time.time()
                    dt = t - t0
                    self.rcvtimer = t
                    self.lastmsg = text
                    result = text
                    #print("comm:readMsg", dt)
            except:
                pass
        return result

    def sendMsg(self, msg):
        t = time.time()
        if (t - self.sendtimer > SEND_DELAY):
            #try:
            #
            self.datadriver.execute_script('sendstr("' + msg + '")')
            self.sendtimer = t
            return True
            #except:


    def startVideoStream(self):
        if (self.isConnected and not self.streaming):
            try:
                self.videodriver.execute_script('document.getElementById("videoswitch").click()')
                time.sleep(2)
                self.updateIsStreaming()
            except:
                print("mediastreamopen error")

    def updateIsStreaming(self):
        print("updateIsStreaming")
        try:
            x = self.videodriver.execute_script('return isMediaStreamOpen()')
        except:
            return
        self.streaming = x

    def close(self):
        self.datadriver.close()
        #self.videodriver.close()
        try:
            self.display.stop()
        except:
            pass

########### WEBSOCKET EVENTS

########### WEBSOCKET EVENTS
if __name__ == '__main__':
    #print("Starting comm")
    # IPC
    context = zmq.Context()

    # Publisher
    comm_publisher = context.socket(zmq.PUB)
    comm_publisher.bind("tcp://*:%s" % ports.COMM_PUB)

    # Subscribe to commander
    commander_subscriber = context.socket(zmq.SUB)
    commander_subscriber.connect("tcp://localhost:%s" % ports.COMMANDER_PUB)
    commander_subscriber.setsockopt_string(zmq.SUBSCRIBE, topic.SENSOR_TOPIC)

    # Subscribe to Tornado websocket server
    browser_subscriber = context.socket(zmq.SUB)
    browser_subscriber.connect("tcp://localhost:%s" % ports.TORNADO_PUB)
    browser_subscriber.setsockopt_string(zmq.SUBSCRIBE, topic.COMMAND_TOPIC)

    # Web scoket for sending data to the browser
    ws = create_connection("ws://localhost:9000/ws/")

    #xcomm=comm()

    while True:
        #while(xcomm.connected()):
        #comm_publisher.send_string("%s %s" % (topic.CONNECTION_TOPIC, "1"))
        #xcomm.startVideoStream()
        # from browser to commander
        while True:
            try:
                msg = browser_subscriber.recv_string(zmq.DONTWAIT)
            except zmq.Again:
                break
            # process task
            msg = msg.strip(str(topic.COMMAND_TOPIC) + " ")
            print("from browser:", msg)
            #print("sending message", msg)
            #ws.send("_"+msg)
            comm_publisher.send_string("%s %s" % (topic.COMMAND_TOPIC, msg))

        """messagedata = xcomm.readMsg()
        if messagedata != None:
            comm_publisher.send_string("%s %s" % (topic.COMMAND_TOPIC, messagedata))"""


        # from commander to browser
        while True:
            try:
                msg = commander_subscriber.recv_string(zmq.DONTWAIT)
                msg=msg.strip(str(topic.SENSOR_TOPIC)+" ")
                #print(msg)
                #xcomm.sendMsg(msg)
            except zmq.Again:
                break
            # process task
            ws.send("_" + msg)
            #print("comm received:", msg)
        time.sleep(0.005)

    # Tell the commander the connection state, to react with control or failsafe
    t=time.time()
    comm_publisher.send_string("%s %s" % (topic.CONNECTION_TOPIC, "0"))
    print(time.time()-t)
    print("not connected")
    time.sleep(0.005)
    ws.close()

        #xcomm.reset()


