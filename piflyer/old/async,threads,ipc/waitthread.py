import threading
import time

# This function gets called by our thread.. so it basically becomes the thread innit..
class dataSendingThread(threading.Thread):
    def __init__(self,x):
        threading.Thread.__init__(self)
        self.daemon = True
        self.x=x
        self.e=threading.Event()

    def run(self):
        while True:
            self.e.wait()
            print(self.x*self.x)
            time.sleep(0.5)
sendThread=dataSendingThread(5)
