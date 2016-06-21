from servo_handler import servo_handler

import number_range as n

TILT_UP_LIMIT = 90
TILT_DOWN_LIMIT = -90


class elevons:
    def __init__(self):
        self.left = servo_handler(1)
        self.right = servo_handler(2)
        self.multiplier = 2
        # mobile devide tilt limits
        self.pitchUpLimit = 45
        self.pitchDownLimit = -45
        self.rollUpLimit = 45
        self.rollDownLimit = -45
        self.setMultiplier(self.multiplier)
        self.setServosUpDownLimit(0, 100)

    ## Servo settings methods

    # servo multiplier, default 2 because of extended range due to elevon mixing (50% pitch 50%roll)
    def setMultiplier(self, multiplier):
        self.left.setMultiplier(multiplier)
        self.right.setMultiplier(multiplier)

    # see servo_handler.py documentation
    def setServosUpDownLimit(self, up, down):
        self.left.setUpDownLimit(up, down)
        self.right.setUpDownLimit(up, down)

    # mobile device pitch limits
    def setPitchTiltLimits(self, up, down):
        if (up <= TILT_UP_LIMIT and down >= TILT_DOWN_LIMIT):
            self.pitchUpLimit = up
            self.pitchDownLimit = down
            print("pitch limit: up:%d, down:%d" % (up, down))

    # mobile device roll limits
    def setRollTiltLimits(self, up, down):
        if (up <= TILT_UP_LIMIT and down >= TILT_DOWN_LIMIT):
            self.rollUpLimit = up
            self.rollDownLimit = down
            print("roll limit: left:%d, right:%d" % (down, up))

    # servoUpDirectionSettings
    def setServosUpDirection(self, left, right):
        self.left.setUpDirection(left)
        self.right.setUpDirection(right)

    def setPitch(self, pitch):
        self.left.setPositionFromTilt(pitch / 2)
        self.right.setPositionFromTilt(pitch / 2)

    def setRoll(self, roll):
        self.left.setPositionFromTilt(-roll / 2)
        self.right.setPositionFromTilt(roll / 2)

    def setPitchRoll(self, pitch, roll):
        self.left.setPositionFromTilt(pitch / 2 - roll / 2)
        self.right.setPositionFromTilt(pitch / 2 + roll / 2)

    # set pitch only, no mixing - not tested!
    def setPitchFromInput(self, pitch):
        pitch = n.arduino_map(n.clamp(pitch, self.pitchDownLimit, self.pitchUpLimit), self.pitchDownLimit,
                              self.pitchUpLimit, -45, 45)
        self.setPitch(pitch)

    # set roll only, no mixing - not tested!
    def setRollFromInput(self, roll):
        roll = n.arduino_map(n.clamp(roll, self.rollDownLimit, self.rollUpLimit), self.rollDownLimit, self.rollUpLimit,
                             -45, 45)
        self.setRoll(roll)
        # print("servo L, R: %d %d" % (self.left.getPosition(), self.right.getPosition()))

    # pitch and roll update, elevons specific method - tested
    def setPitchRollFromInput(self, pitch, roll):
        # both elevons have equal limits to pitch and roll input
        # pitch and roll input have seperate limits
        pitch = n.arduino_map(n.clamp(pitch, self.pitchDownLimit, self.pitchUpLimit), self.pitchDownLimit,
                              self.pitchUpLimit, -45, 45)
        roll = n.arduino_map(n.clamp(roll, self.rollDownLimit, self.rollUpLimit), self.rollDownLimit, self.rollUpLimit,
                             -45, 45)
        self.setPitchRoll(pitch, roll)

    # manual - raw control
    def setAngle(self, pitch, roll):
        # print("pitch,roll: %d %d"%(pitch,roll))
        self.setPitchRollFromInput(pitch, roll)
        # print("servo L, R: %d %d"%(self.left.getPosition(),self.right.getPosition()))

    ## Stabilize and Autopilot mode methods - not tested!, just draft
    """
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
    """

    # stabilize mode algorithm
    def control(self, target_pitch, target_roll, pitch, roll):
        # idea: map target-sensor values difference to pitch and roll control
        self.setPitchRoll(target_pitch - pitch, target_roll - roll)
        #print("control pitch/roll", target_pitch - pitch, "/", target_roll - roll)

        """
        if(target_pitch<pitch):
           self.pullUp()

        elif(target_pitch>pitch):
           self.pullDown()

        if(target_roll<roll):
            self.turnRight()

        if(target_roll>roll):
            self.turnLeft()
        """
