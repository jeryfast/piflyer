from piflyer.servo_handler import servo_handler

class elevons:
    def __init__(self):
        self.left=servo_handler()
        self.right=servo_handler()

    def setAngle(self,pitch,roll):
        #print("setting servos")
        #for testing
        x=1

    def turnRight(self):
        self.left.add()
        self.right.sub()

    def turnLeft(self):
        self.left.sub()
        self.right.add()

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
