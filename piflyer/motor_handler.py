__author__ = 'Jernej'
class motor_handler:
    def __init__(self):
        self.throttle=0

    def add(self):
        self.throttle+=1

    def sub(self):
        self.throttle-=1
    
    #def initialize(self):
        #print("motor initialize sequence")

    def getThrottle(self):
        return self.throttle

    def setThrottle(self,throttle):
        self.throttle=throttle

    def control(self,throttle):
        #print("controlling a motor")
        if(self.throttle<throttle):
            self.throttle+=1
        elif(self.throttle>throttle):
            self.throttle-=1


