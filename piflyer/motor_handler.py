__author__ = 'Jernej'
import number_range as n
import time
import Adafruit_PCA9685
import delays

MIN=0
MAX=100

# Initialise the PWM device using the default address
pwm = Adafruit_PCA9685.PCA9685(0x41)
# Note if you'd like more debug output you can instead run:
# pwm = PWM(0x40, debug=True)

# Set frequency to 60 Hz
pwm.set_pwm_freq(60)

# default:min 150, max 600
servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096
on = 0

class motor_handler:
    def __init__(self, channel):
        self.throttle = 0
        self.minThrottle = 0
        self.maxThrottle = 100
        self.channel = channel
        self.setServoValue(self.channel, servoMin)

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
            self.setServoValue(self.channel,n.arduino_map(throttle, MIN, MAX, servoMin, servoMax))

    def setServoValue(self, channel, value):
        t = time.time()
        if (t - self.timer > delays.SENSOR_REFRESH_DELAY):
            self.timer = t
            value = n.arduino_map(value, 0, 180, servoMin, servoMax)
            pwm.set_pwm(channel, on, int(value))

    # auto throttle
    #def control(self,throttle):
        #print("controlling a motor")



