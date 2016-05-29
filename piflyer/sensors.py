class sensors:
    def __init__(self):
        self.pitch = 10.0
        self.roll = -3.0
        self.yaw = 1.0
        self.compass= 100.0
        self.temp = 23.0
        self.humidity = 50.0
        self.pressure = 990.0
        self.ax = 0.0
        self.ay = 0.0
        self.az = 0.0

    def read(self):
        print("branje podatkov iz senzorjev")


