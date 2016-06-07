__author__ = 'Jernej'
import number_range as n
MIN=0
MAX=100
class motor_handler:
    def __init__(self):
        self.throttle = 0
        self.minThrottle = 0
        self.maxThrottle = 100

    def add(self):
        self.throttle+=1

    def sub(self):
        self.throttle-=1
    
    def initialize(self):
        #write, when you test it manually with manual throttle
        print("motor initializing sequence")

    def setThrottleLimits(self,min,max):
        if(min>=MIN and max<=MAX):
            self.minThrottle=min
            self.maxThrottle=max
            print("Throttle limits set from %d to %d"%(min,max))

    def setThrottleFromInput(self, throttle):
        throttle=n.arduino_map(n.clamp(throttle,MIN,MAX),MIN,MAX,self.minThrottle,self.maxThrottle)
        self.setThrottle(throttle)
        print("throttle: %d" % (self.throttle))

    def getThrottle(self):
        return self.throttle

    def setThrottle(self,throttle):
        if(throttle>=self.minThrottle and throttle<=self.maxThrottle):
            self.throttle=throttle

    # auto throttle
    #def control(self,throttle):
        #print("controlling a motor")



