from picamera import PiCamera
from time import sleep

class camera:
    def __init__(self):
        #testing only
        self.camera="camera"
        self.count=0
        self.w=1920
        self.h=1080
    def takeShot(self):
        sleep(1)
        c=PiCamera()
        try:
            # do something with the camera
            camera.resolution = (1920, 1080)
            sleep(1)
            camera.capture("/home/pi/camera/img"+str(self.count)+".jpg")
            self.count+=1
            print("Shot taken")
        finally:
            c.close()

    def recording(self,state):
        if(state ==  '0'):
            self.stopRecording()
        else:
            self.startRecording()
    def startRecording(self):
        print("Recording on")

    def stopRecording(self):
        print("Recording off")