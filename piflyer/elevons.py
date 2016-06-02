from piflyer.servo_handler import servo_handler

class elevons:
    def __init__(self):
        self.left=servo_handler()
        self.right=servo_handler()
        self.multiplier=2
        self.setMultiplier(self.multiplier)
        self.setUpDownLimit(0, 100)

    ## Servo settings methods

    # servo multiplier, default 2 because of extended range due to elevon mixing (50% pitch 50%roll)
    def setMultiplier(self,multiplier):
        self.left.setMultiplier(multiplier)
        self.right.setMultiplier(multiplier)

    # see servo_handler.py documentation
    def setUpDownLimit(self, up, down):
        self.left.setUpDownLimit(up,down)
        self.right.setUpDownLimit(up,down)

    # see servo_handler.py documentation - not quite tested yet
    def setTiltSensitivity(self,down,up):
        self.left.setTiltSensitivity(down,up)
        self.right.setTiltSensitivity(down, up)

    # servoUpDirectionSettings
    def setServos(self,left,right):
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
    # pitch and roll update, elevons specific method
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