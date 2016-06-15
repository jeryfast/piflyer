__author__ = 'Jernej'
import number_range as n
import time
MIN = 0
MAX = 180
class servo_handler:
    def __init__(self):
        # servo position variables
        self.up = MIN
        self.down = MAX
        self.neutral = MAX/2
        self.position = 0
        self.oldRange=[0,0]
        # mobile phone tilt reference - dont`t change
        self.upTilt = 45
        self.downTilt = -45
        # upAdd can be 1 or -1
        self.upAdd = -1
        # input intensitymultiplier
        self.multiplier=1
        self.t=0

    def getPosition(self):
        return self.position

    def getUpPosition(self):
        return self.up

    def getDownPosition(self):
        return self.down

    # converter
    def tiltToPosition(self, tilt):
        return n.arduino_map(tilt, self.downTilt, self.upTilt, self.down, self.up)

    # converter with limits
    def tiltToPositionWithLimits(self,tilt, upTilt, downTilt):
        return n.arduino_map(tilt, downTilt, upTilt, self.down, self.up)

    # converter
    def positionToTilt(self,position):
        return n.arduino_map(position, self.down, self.up, self.downTilt, self.upTilt)

    """
    # reference limits of tilt controls
    def setTiltLimits(self, up, down):
        self.upTilt = up
        self.downTilt = down

    # reference limits of tilt control
    def getTiltLimits(self):
        return [self.upTilt,self.downTilt]
    """

    # resolution: 100, from servosettings
    def setPositionPercent(self, position):
        position = n.arduino_map(position, 0, 100, MIN, MAX)
        self.setPosition(position)

    def setPositionFromTilt(self, tiltPosition):
        self.setPosition(self.tiltToPosition(tiltPosition*self.multiplier))

    # resolution: 180 or abs(MAX-MIN)
    def setPosition(self,position):
        if(position>MIN and position<MAX):
            x=time.time
            if(x-self.t>1000):
                t=x
                print("position: ",position)
            self.position=position

    # servo movement range limits - tested!
    def setUpDownLimit(self,up,down):

        # save history for live servo update - to know which value to update - top/left or bottom/right
        a, b = self.oldRange
        u, d = False, False
        if (up != a):
            u = True
            self.oldRange[0] = up
        if (down != b):
            d = True
            self.oldRange[1] = down

        """
        Sets up and down servo limitations in percentage values: range - 0 to 100,
        useful for flap of airbrake definition, control surface offsets for
        airplane neutral point correction
        Correct upDirection values must be set to work properly
        up=0, down=100 -> full range
        """
        if(self.upAdd == -1):
            self.up=n.arduino_map(up, 0, 100, MIN, MAX)
            self.down=n.arduino_map(down, 0, 100, MIN, MAX)
            if(u):
                self.setPosition(self.up)
                print("Servo position: %d" % (self.up))
                u=False
            elif(d):
                self.setPosition(self.down)
                print("Servo position: %d" % (self.down))
                d=False
        elif(self.upAdd == 1):
            self.up=n.arduino_map(up, 0, 100, MAX, MIN)
            self.down=n.arduino_map(down, 0, 100, MAX, MIN)
            if (u):
                self.setPosition(self.up)
                print("Servo position: %d" % (self.up))
                u = False
            elif (d):
                self.setPosition(self.down)
                print("Servo position: %d" % (self.down))
                d = False

    # servo directions settings - tested
    def setUpDirection(self, val):
        if (val > 50):
            self.up = MAX
            self.down = MIN
            self.upAdd = 1
        else:
            self.up = MIN
            self.down = MAX
            self.upAdd = -1
        self.setPositionPercent(val)
        print("Servo position: %d"%(val))

    def setMultiplier(self, multiplier):
        self.multiplier=multiplier

    # not tested yet
    def add(self, val=None):
        if (not val):
            val = 1
            self.setPosition(self.position + val*self.upAdd)

    # not tested yet
    def sub(self, val=None):
        if (not val):
            val = 1
        self.setPosition(self.position - val*self.upAdd)

#RPi code
#!/usr/bin/python

"""from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x41)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

#default:min 150, max 600
servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096
#added
on=0

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  #pwm.setPWM(channel, 0, pulse)
  print(pulse)

def arduino_map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def setServoValue(channel, value):
  value = arduino_map(value, 0, 180, servoMin, servoMax)
  pwm.setPWM(channel, on, value)

#  Set frequency to 60 Hz
pwm.setPWMFreq(60)

# Change speed of continuous servo on channel O
for i in range(181):
  setServoValue(0,i)
"""

