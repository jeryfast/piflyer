from piflyer.servo_handler import servo_handler
TILT_UP_LIMIT=90
TILT_DOWN_LIMIT=-90

class elevons:
    def __init__(self):
        self.left=servo_handler()
        self.right=servo_handler()
        self.multiplier=2
        self.pitchUpLimit=45
        self.pitchDownLimit=-45
        self.rollUpLimit = 45
        self.rollDownLimit = -45
        self.setMultiplier(self.multiplier)
        self.setServosUpDownLimit(0, 100)

    def arduino_map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    ## Servo settings methods

    # servo multiplier, default 2 because of extended range due to elevon mixing (50% pitch 50%roll)
    def setMultiplier(self,multiplier):
        self.left.setMultiplier(multiplier)
        self.right.setMultiplier(multiplier)

    # see servo_handler.py documentation
    def setServosUpDownLimit(self, up, down):
        self.left.setUpDownLimit(up,down)
        self.right.setUpDownLimit(up,down)

    # mobile device pitch limits
    def setPitchTiltLimits(self, up, down):
        if (up <= TILT_UP_LIMIT and down >= TILT_DOWN_LIMIT):
            self.pitchUpLimit=up
            self.pitchDownLimit=down
            print("pitch limit: up:%d, down:%d"%(up,down))

    # mobile device roll limits
    def setRollTiltLimits(self, up, down):
        if (up <= TILT_UP_LIMIT and down >= TILT_DOWN_LIMIT):
            self.rollUpLimit=up
            self.rollDownLimit=down
            print("roll limit: left:%d, right:%d" % (down, up))

    # servoUpDirectionSettings
    def setServosUpDirection(self, left, right):
        self.left.setUpDirection(left)
        self.right.setUpDirection(right)

    # set pitch only, no mixing
    def setPitch(self,position):
        self.left.setPositionFromTilt(position)
        self.right.setPositionFromTilt(position)

    #does it work?
    """
    # set roll only, no mixing
    def setRoll(self, position):
        self.left.setPositionFromTilt(self.left.positionToTilt(self.left.getPosition())/2-position/2)
        self.right.setPositionFromTilt(self.right.positionToTilt(self.right.getPosition())+position/2)
        """

    # pitch and roll update, elevons specific method - tested
    def setPitchRoll(self,pitch,roll):
        # both elevons have equal limits to pitch and roll input
        # pitch and roll should have seperate limits
        pitch = self.arduino_map(clamp(pitch, self.pitchDownLimit,self.pitchUpLimit),self.pitchDownLimit,self.pitchUpLimit,-45, 45)
        roll = self.arduino_map(clamp(roll, self.rollDownLimit, self.rollUpLimit), self.rollDownLimit, self.rollUpLimit, -45, 45)
        self.left.setPositionFromTilt(pitch/2 - roll/2)
        self.right.setPositionFromTilt(pitch / 2 + roll / 2)

    def setAngle(self,pitch,roll):
        print("pitch,roll: %d %d"%(pitch,roll))
        self.setPitchRoll(pitch,roll)
        print("servo L, R: %d %d"%(self.left.getPosition(),self.right.getPosition()))

    ## Stabilize and Autopilot mode methods - not tested!, just draft

    def turnRight(self, val=1):
        self.left.add(val)
        self.right.sub(val)

    def turnLeft(self, val=1):
        self.left.sub(val)
        self.right.add(val)

    def pullUp(self):
         self.left.add()
         self.right.add()

    def pullDown(self):
         self.left.sub()
         self.right.sub()

    def control(self,target_pitch,target_roll,pitch, roll,):
        #print("controlling servos")

        if(target_pitch<pitch):
           self.pullUp()

        elif(target_pitch>pitch):
           self.pullDown()

        if(target_roll<roll):
            self.turnRight()

        if(target_roll>roll):
            self.turnLeft()

    ##Helpers

# return limit value if n out of limits
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

