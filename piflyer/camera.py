class camera:
    def __init__(self):
        #testing only
        self.camera="camera"
    def takeShot(self):
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