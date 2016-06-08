import random
import string
from selenium import webdriver
import selenium
from pyvirtualdisplay import Display
import time
import threading
NULL=''

M = 1000
N = 13

class comm():
    def __init__(self):
        self.display = Display(visible=0, size=(480, 320))
        self.display.start()

        #self.driver = webdriver.PhantomJS(executable_path=r'C:\Users\Jernej\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        firefox_profile.set_preference("media.navigator.permission.disabled", True);
        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
        self.driver.set_window_size(800, 600)

        #ID array
        #self.arr = [None] * M
        #self.driver = webdriver.Firefox()
        #self.driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNITWITHJS)
        self.driver.get('http://peerclient.cloudapp.net/peer1.html')
        self.start()
        self.streaming=False
        self.lastmsg= ""
        self.lastmsgtime=0

    def start(self):
        time.sleep(3)
        try:
            self.msg = self.driver.find_element_by_id('msg')
            self.sender = self.driver.find_element_by_id('sender')
            self.receiver = self.driver.find_element_by_id('receiver')
            self.videoswitch = self.driver.find_element_by_id('videoswitch')
            self.connection = self.driver.find_element_by_id('connected')
        except AttributeError:
            time.sleep(0.5)

    def reset(self):
        #self.driver.save_screenshot('screenshot.png')
        try:
            if(self.driver.find_element_by_id('refresh').text != 'false'):
                print("refreshing")
                self.driver.refresh()
                self.start()
                self.streaming = False
        except:
            time.sleep(0.5)

    def get_my_id(self):
        if(self.connected()):
            return self.driver.find_element_by_id('peerid').text

    def get_remote_id(self):
        if(self.connected()):
            return self.driver.find_element_by_id('remoteid').text

    #def connect(self):
    def set_attr(self, locator, attr, value):
        self.driver.execute_script('document.getElementById("' + locator + '").' + attr + '="' + value + '";')

    def connected(self):
        #print("check-connected")
        t=time.time()
        if(t-self.lastmsgtime>5):
            self.lastmsgtime=t
            text=""
            try:
                self.connection = self.driver.find_element_by_id('connected')
                text=self.connection.text
            except:
                pass

            if(text!='true'):
                return False
        return True

    def readmsg(self):
        result=None
        try:
            text=self.receiver.text
            if(text!=self.lastmsg):
                self.lastmsg=text
                self.lastmsgtime=time.time()
                result=text
        except:
            pass
        #if(text!=NULL):
            #self.rcvclear.click()
            #self.driver.execute_script('document.getElementById("receiver").innerHTML="";')
        return result

    def sendmsg(self, msg):
        #self.msg.send_keys(msg)
        #self.msg.send_keys(Keys.ENTER)
        #self.driver.execute_script('document.getElementById("msg").value = "' + msg + '";document.getElementById("sender").click()')
        #self.browser.execute_script('document.getElementById("sender").click()')
        try:
            self.driver.execute_script('sendstr("'+msg+'")')
        except:
            pass
        #print(str(round(r,2))+" Frekvenca: "+str(1/r)+"Hz")

    def startVideoStream(self):
        print(threading._active)
        if(not self.streaming):
            try:
                self.updateIsStreaming()
                self.driver.execute_script('document.getElementById("videoswitch").click()')
                time.sleep(0.5)
            except:
                print("mediastreamopen error")

    def updateIsStreaming(self):
        try:
            x=self.driver.execute_script('return isMediaStreamOpen()')
        except:
            return

        self.streaming = x

    def close(self):
        self.driver.close()
        #self.display.stop()

    def generateIDs(self):
        for i in range(len(self.arr)):
            self.arr[i] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))
        for i in range(len(self.arr)):
            print(self.arr[i])
