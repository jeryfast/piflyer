import random as r
#from sense_hat import SenseHat
import time
import zmq
import zmq_ports as ports

REFRESH_DELAY=0.02
TOPIC = 10001

class sensors():
    def __init__(self):
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.compass = 10
        self.temp = 0
        self.humidity = 0
        self.pressure = 0
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.altitude = 0

        # Comment if not running on RPI
        """self.sense = SenseHat(topic, sensors_publisher)
        self.sense.clear()
        self.sense.set_imu_config(True, True, True)"""

    def joinDelimiter(self, arr):
        tmp=[None]*len(arr)
        for i in range(len(arr)):
            tmp[i]=str(arr[i])
        return ",".join(tmp)

    def getRandomStrArr(self):
        pitch = r.randint(3, 5)
        roll = r.randint(3, 5)
        yaw = r.randint(0, 2)
        compass = r.randint(240, 241)
        temp = r.randint(19, 20)
        humidity = r.randint(43, 46)
        pressure = r.randint(983, 985)
        ax = 0.1
        ay = 0.1
        az = 0.1
        altitude = 286
        return self.joinDelimiter([pitch, roll, yaw, compass, temp, humidity, pressure, ax, ay, az, altitude])

    def run(self):
        while True:
            """self.temp = round(self.sense.get_temperature(), 1)
            self.humidity = round(self.sense.get_humidity(), 1)
            self.pressure = round(self.sense.get_pressure(), 2)
            self.sense.set_imu_config(True, True, True)
            pitch, yaw, roll = self.sense.get_orientation().values()
            ax, ay, az = self.sense.get_accelerometer_raw().values()
            self.compass = round(self.sense.get_compass(), 2)
            self.pitch = round(pitch, 2)
            self.roll = round(roll, 2)
            if (self.pitch > 180):
                self.pitch -= 360
            if (self.roll > 180):
                self.roll -=  360
            self.yaw = round(yaw, 2)
            self.ax = round(ax, 2)
            self.ay = round(ay, 2)
            self.az = round(az, 2)
            self.altitude = round((288.15 / -0.0065) * ((self.pressure * 100 / 101325) ** (-(8.31432 * -0.0065) / (9.80665 * 0.0289644)) - 1),2)
            """
            self.pitch = r.randint(3, 5)
            self.roll = r.randint(3, 5)
            self.yaw = r.randint(0, 2)
            self.compass = r.randint(240, 241)
            self.temp = r.randint(19, 20)
            self.humidity = r.randint(43, 46)
            self.pressure = r.randint(983, 985)
            self.ax = 0.1
            self.ay = 0.1
            self.az = 0.1
            self.altitude = 286

            sensors_publisher.send_string("%d %s" % (TOPIC, self.getStrArr()))

            time.sleep(REFRESH_DELAY)

    def getStrArr(self):
        return self.joinDelimiter([self.pitch, self.roll, self.yaw, self.compass, self.temp, self.humidity, self.pressure, self.ax, self.ay,
                                   self.az, self.altitude])

if __name__ == '__main__':

    # Publisher
    context = zmq.Context()
    sensors_publisher = context.socket(zmq.PUB)
    sensors_publisher.bind("tcp://*:%s" % ports.SENSORS_PUB)
    sensors=sensors()
    sensors.run()





