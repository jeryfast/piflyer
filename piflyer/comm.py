import random
import string
import time
from selenium import webdriver
#from multiprocessing.context import Process
from pyvirtualdisplay import Display
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from Cython.Utils import


NULL=''

M = 1000
N = 13
SEND_DELAY=0.05

class comm():
    def __init__(self):
        self.display = Display(visible=0, size=(480, 320))
        self.display.start()
        print("Starting firefox")
        #self.driver = webdriver.PhantomJS(executable_path=r'C:\Users\Jernej\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        firefox_profile = webdriver.FirefoxProfile()
        #firefox_profile = DesiredCapabilities.FIREFOX()
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
        self.connchecktime=0
        self.sendtimer=0

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
        t=round(time.time(),1)
        if(t-self.connchecktime>1 and t-self.lastmsgtime>3):
            self.connchecktime=round(t,1)
            text=""
            try:
                text = self.connection.text
            except:
                pass

            if(text!="true"):
                return False
        return True

    def readMsg(self):
        result=None
        try:
            text=self.receiver.text
            if(text!=self.lastmsg):
                self.lastmsgtime = time.time()
                self.lastmsg=text
                result=text
        except:
            pass
        #if(text!=NULL):
            #self.rcvclear.click()
            #self.driver.execute_script('document.getElementById("receiver").innerHTML="";')
        return result

    """
    def sendMsgAsync(self,msg):
        if __name__ == '__main__':
            p = Process(target=self.sendMsg, args=(msg,))
            p.start()
            p.join()
    """

    def sendMsg(self, msg):
        t=time.time()
        if(t-self.sendtimer>SEND_DELAY):
            try:
                self.driver.execute_script('sendstr("'+msg+'")')
                self.sendtimer = t
                return True
            except:
                pass



    def startVideoStream(self):
        if(not self.streaming):
            try:
                self.updateIsStreaming()
                self.driver.execute_script('document.getElementById("videoswitch").click()')
                time.sleep(1)
            except:
                print("mediastreamopen error")

    def updateIsStreaming(self):
        print("updateIsStreaming")
        try:
            x=self.driver.execute_script('return isMediaStreamOpen()')
        except:
            return

        self.streaming = x

    def close(self):
        self.driver.close()
        self.display.stop()

    def generateIDs(self):
        for i in range(len(self.arr)):
            self.arr[i] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))
        for i in range(len(self.arr)):
            print(self.arr[i])
