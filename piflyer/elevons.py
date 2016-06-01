from piflyer.servo_handler import servo_handler

class elevons:
    def __init__(self):
        self.left=servo_handler()
        self.right=servo_handler()
        self.multiplier=2
        self.setMultiplier(self.multiplier)
        self.setUpDownLmit(0,100)

    ## Servo settings methods

    def setMultiplier(self,multiplier):
        self.left.setMultiplier(multiplier)
        self.right.setMultiplier(multiplier)

    def setUpDownLmit(self,up,down):
        self.left.setUpDownLimit(up,down)
        self.right.setUpDownLimit(up,down)

    def setTiltSensitivity(self,down,up):
        self.left.setTiltSensitivity(down,up)
        self.right.setTiltSensitivity(down, up)

    # servoUpDirectionSettings
    def setServos(self,left,right):
        self.left.setUpDirection(left)
        self.right.setUpDirection(right)

    def setPitch(self,position):
        self.left.setPositionFromTilt(position)
        self.right.setPositionFromTilt(position)

    #does it work?
    """
    def setRoll(self, position):
        self.left.setPositionFromTilt(self.left.positionToTilt(self.left.getPosition())/2-position/2)
        self.right.setPositionFromTilt(self.right.positionToTilt(self.right.getPosition())+position/2)
        """

    def setPitchRoll(self,pitch,roll):
        #both elevons have equal sensitivity to pitch and roll input
        down,up=self.left.getTiltSensitivity()
        if(pitch>up):
            pitch=up
        elif(pitch<down):
            pitch=down
        if(roll>up):
            roll=up
        elif(roll<down):
            roll=down
        self.left.setPositionFromTilt(pitch/2-roll/2)
        self.right.setPositionFromTilt(pitch/2+roll/2)

    def setAngle(self,pitch,roll):
        print("pitch,roll: %d %d"%(pitch,roll))
        #self.setPitch(pitch)
        #self.setRoll(roll)
        self.setPitchRoll(pitch,roll)
        print("servo L, R: %d %d"%(self.left.getPosition(),self.right.getPosition()))

    ## Autopilot methods - not tested!

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
