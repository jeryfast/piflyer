__author__ = 'Jernej'
import os

BITRATE_MAX=17000000
HEIGHT_MAX=1080

class streamer:
    def __init__(self,ip):
        self.height=720
        self.width=1080
        self.fps=25
        self.bitrate=8000000
        self.ipAddress=ip
    def run(self):
        os.system("raspivid -t 0 -h "+self.height+" -w "+self.widtht+" -fps "+self.fps+" -hf -b "+self.bitrate+" -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host="+self.ipAddress+" port=5000")

    def updateIP(self,ip):
        self.ipAddress=ip

    #0-100%
    def setBitRate(self,percent):
        self.bitrate=BITRATE_MAX/100*percent

    def setQuality(self,quality):
        # 1 = the best
        if(quality=="1"):
            self.height=HEIGHT_MAX
            self.width=self.height*16/9
        if(quality=="2"):
            self.height=720
            self.width=self.height*16/9
        if(quality=="3"):
            self.height=480
            self.width=self.height*4/3
        if(quality=="4"):
            self.height=240
            self.width=self.height*4/3
