__author__ = 'Jernej'
DOWN=0
UP=4096
NEUTRAL=UP/2

class servo_handler:
    def __init__(self):
        self.position=NEUTRAL
    def getPosition(self):
        return self.position
    def setPosition(self,position):
        self.position=position
    def add(self):
        self.position+=1
    def sub(self):
        self.position-=1

