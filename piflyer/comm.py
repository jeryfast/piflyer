import random
import string
from selenium import webdriver
from pyvirtualdisplay import Display
import time
NULL=''

M = 1000
N = 13

class comm:
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
        #self.driver.set_window_size(800, 600)

        #ID array
        #self.arr = [None] * M
        #self.driver = webdriver.Firefox()
        #self.driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNITWITHJS)
        self.driver.get('http://peerclient.cloudapp.net/peer1.html')
        #self.driver.get('http://siol.net')
        #self.driver.get('http://localhost:63342/TcpServer/peer1.html')
        time.sleep(3)
        self.start()
        self.streaming=False

    def start(self):
        self.msg = self.driver.find_element_by_id('msg')
        self.sender = self.driver.find_element_by_id('sender')
        self.receiver = self.driver.find_element_by_id('receiver')
        self.videoswitch = self.driver.find_element_by_id('videoswitch')
        self.connection = self.driver.find_element_by_id('connected')

    def reset(self):
        #self.driver.save_screenshot('screenshot.png')
        if(self.driver.find_element_by_id('refresh').text != 'false'):
            print("refreshing")
            self.driver.refresh()
            self.start()
            self.streaming = False
            time.sleep(2)

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
        return self.connection.text=='true'

    def readmsg(self):
        text=self.receiver.text
        if(text!=NULL):
            #self.rcvclear.click()
            self.driver.execute_script('document.getElementById("receiver").innerHTML="";')
        return text

    def sendmsg(self, msg):
        #self.msg.send_keys(msg)
        #self.msg.send_keys(Keys.ENTER)
        #self.driver.execute_script('document.getElementById("msg").value = "' + msg + '";document.getElementById("sender").click()')
        #self.browser.execute_script('document.getElementById("sender").click()')
        self.driver.execute_script('sendstr("'+msg+'")')
        #print(str(round(r,2))+" Frekvenca: "+str(1/r)+"Hz")

    def startVideoStream(self):
        if(not self.streaming):
            self.streaming=True
            self.driver.execute_script('document.getElementById("videoswitch").click()')

    def close(self):
        self.driver.close()
        self.display.stop()
    def generateIDs(self):
        for i in range(len(self.arr)):
            self.arr[i] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))
        for i in range(len(self.arr)):
            print(self.arr[i])
