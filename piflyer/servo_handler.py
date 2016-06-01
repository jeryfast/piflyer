__author__ = 'Jernej'
MIN = 0
MAX = 180
class servo_handler:
    def __init__(self):
        # servo position variables
        self.up = MIN
        self.down = MAX
        self.neutral = MAX/2
        self.position = 0
        # mobile phone tilt
        self.upTilt = 45
        self.downTilt = -45
        # upAdd can be 1 or -1
        self.upAdd = -1
        # input intensitymultiplier
        self.multiplier=1

    def arduino_map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    def getPosition(self):
        return self.position

    # converter
    def tiltToPosition(self, tilt):
        return self.arduino_map(tilt, self.downTilt, self.upTilt, self.down, self.up)

    # converter
    def positionToTilt(self,position):
        return self.arduino_map(position, self.down, self.up, self.downTilt, self.upTilt)

    # sensitivity of tilt controls
    def setTiltSensitivity(self, down, up):
        self.upTilt = up
        self.downTilt = down

    def getTiltSensitivity(self):
        return [self.downTilt,self.upTilt]

    # resolution: 100, from servosettings
    def setPositionPercent(self, position):
        position = self.arduino_map(position, 0, 100, MIN, MAX)
        self.setPosition(position)

    def setPositionFromTilt(self, tiltPosition):
        self.setPosition(self.tiltToPosition(tiltPosition*self.multiplier))

    # resolution: 180 or abs(MAX-MIN)
    def setPosition(self,position):
        if(position>MIN and position<MAX):
            self.position=position

    # servo movement limits - tested
    def setUpDownLimit(self,up,down):
        """
        Sets up and down servo limitations in percentage values: range - 0 to 100,
        useful for flap of airbrake definition, control surface offsets for
        airplane neutral point correction
        Correct upDirection values must be set to work properly
        up=0, down=100 -> full range
        """
        if(self.upAdd == -1):
            self.up=self.arduino_map(up, 0, 100, MIN, MAX)
            self.down=self.arduino_map(down, 0, 100, MIN, MAX)
        elif(self.upAdd == 1):
            self.up=self.arduino_map(up, 0, 100, MAX, MIN)
            self.down=self.arduino_map(down, 0, 100, MAX, MIN)

    # servo directions settings-works
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

