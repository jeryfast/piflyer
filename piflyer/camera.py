from picamera import PiCamera
from time import sleep
import os

class camera:
    def __init__(self):
        #testing only
        self.camera="camera"
        self.count=0
        self.w=2592
        self.h=1944
        self.busy=False

    def takeShot(self):
        os.system("v4l2-ctl --set-fmt-video=width="+self.w+",height="+self.h+",pixelformat=3")
        os.system("v4l2-ctl --stream-mmap=3 --stream-count=1 --stream-to=/home/pi/camera/img"+str(self.count)+".jpg")
        os.system("v4l2-ctl --set-fmt-video=width=720,height=480,pixelformat=H264 -p 30")
        print("Shot taken")

    def recording(self,state):
        if(state ==  '0'):
            self.stopRecording()
        else:
            self.startRecording()
    def startRecording(self):
        print("Recording on")

    def stopRecording(self):
        print("Recording off")