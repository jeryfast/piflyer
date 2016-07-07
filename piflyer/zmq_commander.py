import random
import time
import zmq

import zmq_ports as ports
import zmq_topics as topic

from zmq_sensors import sensors
from elevons import elevons
from motor_handler import motor_handler
import commands as c
from camera import camera
from gpsstorage import gpsdata
import rpi

MODE = "M"
CONTROL = "C"
HOLD = "H"

ALT = "T"
AUTO = "A"

CAMERA = "S"
RECORD = "R"

MANUAL = "m"
STABILIZED = "s"
RESQUE = "r"

SERVO_INIT = "SI"
SERVO_LIMIT = "SL"
TILT_PITCH_LIMIT = "PL"
TILT_ROLL_LIMIT = "RL"
THROTTLE_LIMIT = "TL"

SPEED = "V"

SHUTDOWN = "X"


class commander:
    def __init__(self):
        self.mode = "m"

        self.pitch_hold = False
        # self.hdg_hold=False
        self.alt_hold = False
        self.auto_hold = False
        self.speed_hold = False
        self.is_connected = 0

        self.status = c.OK
        self.servos_init = False
        self.throttle_updated = False

        self.pitch = 0.0
        self.roll = 0.0
        self.throttle = 0.0
        self.heading = 0.0
        self.altittude = 0.0
        self.speed = 0

        self.elevons = elevons()
        self.sensors = sensors()
        self.gps = gpsdata()
        self.motor = motor_handler(0)
        self.camera = camera()

    def getParameters(self):
        return [self.pitch, self.roll, self.throttle]

    def setMode(self, mode):
        self.mode = mode
        print("mode: ",mode)

    def setHold(self, words):
        if (words[1] == ALT):
            self.alt_hold = bool(int(float(words[2])))
            print("ALT_HOLD: %s" % (self.alt_hold))
        elif (words[1] == AUTO):
            self.auto_hold = bool(int(float(words[2])))
            print("AUTO_HOLD: %s" % (self.auto_hold))
        elif (words[1] == SPEED):
            self.speed = bool(int(float(words[2])))
            print("SPEED HOLD: %s" % (self.speed))

    # process command
    def update(self, arg=""):
        try:

            self.status = c.OK
            words = arg.split(',')
            if (words[0] == MODE):
                self.setMode(words[1])
                print("updating mode:" + arg)

            elif (words[0] == CONTROL):
                self.servos_init = False
                if(not self.alt_hold):
                    self.pitch = int(float(words[1]))
                self.roll = int(float(words[2]))
                if (len(words) >= 4):
                    self.throttle = int(words[3])
                    self.throttle_updated = True

            elif (words[0] == CAMERA):
                #should change SENSOR_TOPIC to something else
                print("taking shot")
                commander_publisher.send_string("%s %s" % (topic.SENSOR_TOPIC, "stopStream"))
                self.camera.takeShot()
                print("starting stream")
                commander_publisher.send_string("%s %s" % (topic.SENSOR_TOPIC, "startStream"))

            elif (words[0] == RECORD):
                self.camera.recording(words[1])

            # hold functions
            elif (words[0] == HOLD):
                self.setHold(words)

            elif (words[0] == AUTO):
                if (self.auto_hold):
                    self.heading = float(words[1])
                    if (self.alt_hold):
                        self.altittude = float(words[2])
                    else:
                        self.pitch = float(int(words[2]))
                    if (self.speed_hold):
                        self.speed = float(int(words[2]))

            elif (words[0] == SERVO_INIT):
                self.servos_init = True
                self.elevons.setServosUpDirection(int(float(words[1])), int(float(words[2])))
            elif (words[0] == SERVO_LIMIT):
                self.servos_init = True
                self.elevons.setServosUpDownLimit(int(float(words[1])), int(float(words[2])))
            elif (words[0] == TILT_PITCH_LIMIT):
                self.servos_init = True
                self.elevons.setPitchTiltLimits(int(float(words[1])), int(float(words[2])))
            elif (words[0] == TILT_ROLL_LIMIT):
                self.servos_init = True
                self.elevons.setRollTiltLimits(int(float(words[1])), int(float(words[2])))
            elif (words[0] == THROTTLE_LIMIT):
                self.servos_init = True
                self.motor.setThrottleLimits(int(float(words[1])), int(float(words[2])))
            elif(words[0] == SHUTDOWN):
                print("shutdown")
                rpi.shutdown()
            else:
                self.status = c.INVALID
                # print("status invalid")
        except:
            result=self.status = c.INVALID
        return self.status

    def control(self):
        # print("control")
        if (not self.servos_init):
            if (self.mode == MANUAL):
                # print("Manual %f %f" % (self.pitch,self.roll))
                # constantly updated even if no change ... not ok
                self.elevons.setAngle(self.pitch, self.roll)
                # self.elevons.setRoll(self.roll)
                # not tested
                if (self.throttle_updated):
                    self.throttle_updated = False
                    self.motor.setThrottleFromInput(self.throttle)

            # not tested
            elif (self.mode == STABILIZED):
                #print("Stabilized %f %f" % (self.pitch, self.roll))
                # auto on
                if(self.auto_hold):
                    # alt on, auto on, autothrottle
                    if (self.alt_hold):
                        print("controlling hdg, alt")
                    # alt off, auto on, autothrottle
                    else:
                        print("controlling hdg, pitch")
                        self.controlHdgPitchWing()

                # auto off
                else:
                    # alt on, auto off
                    if (self.alt_hold):
                        print("controlling roll")
                    # alt off, auto off
                    else:
                        self.elevons.stabilize(self.pitch, self.roll, self.sensors.pitch, self.sensors.roll)
                    if (self.throttle_updated):
                        self.throttle_updated = False
                        self.motor.setThrottleFromInput(self.throttle)

            # not tested
            elif (self.mode == RESQUE):
                self.elevons.stabilize(0, 0, self.sensors.pitch, self.sensors.roll)
                self.motor.setThrottleFromInput(self.throttle)
                # self.motor. ...

    # not tested
    def failsafe(self):
        # print("failsafe")

        # TODO control in reference to altitude, speed and glide slope
        self.elevons.stabilize(0, 0, self.sensors.pitch, self.sensors.roll)
        self.motor.setThrottleFromInput(self.throttle)

    def run(self):
        # print(self.is_connected)
        if (self.is_connected):
            self.control()
        else:
            self.failsafe()

    # not tested
    def controlHdgPitchWing(self):
        hdgdiff = self.heading-self.sensors.heading
        sign = hdgdiff/abs(hdgdiff)
        if(abs(hdgdiff)>10 and abs(self.sensors.pitch)<5):
            print("turn")
            done=self.elevons.turn(30*sign, self.sensors.roll, 20)
            if(done):
                self.elevons.stabilize(0, 0, self.sensors.pitch, self.sensors.roll)
        else:
            print("pitch")
            self.elevons.stabilize(self.pitch,0,self.sensors.pitch,self.sensors.roll)



if __name__ == '__main__':
    # print("Starting commander")
    # Publisher
    context = zmq.Context()
    commander_publisher = context.socket(zmq.PUB)
    commander_publisher.bind("tcp://*:%s" % ports.COMMANDER_PUB)

    # Subscribe to comm messages
    comm_subscriber = context.socket(zmq.SUB)
    comm_subscriber.connect("tcp://localhost:%s" % ports.COMM_PUB)
    comm_subscriber.setsockopt_string(zmq.SUBSCRIBE, topic.COMMAND_TOPIC)

    # Subscrine to comm connection info
    connection_subscriber = context.socket(zmq.SUB)
    connection_subscriber.connect("tcp://localhost:%s" % ports.COMM_PUB)
    connection_subscriber.setsockopt_string(zmq.SUBSCRIBE, topic.CONNECTION_TOPIC)

    # Subscribe to sensors
    sensors_subscriber = context.socket(zmq.SUB)
    sensors_subscriber.connect("tcp://localhost:%s" % ports.SENSORS_PUB)
    sensors_subscriber.setsockopt_string(zmq.SUBSCRIBE, topic.SENSOR_TOPIC)

    # Subscribe to gps
    gps_subscriber = context.socket(zmq.SUB)
    gps_subscriber.connect("tcp://localhost:%s" % ports.GPS_PUB)
    gps_subscriber.setsockopt_string(zmq.SUBSCRIBE, topic.GPS_TOPIC)

    # Initiate commander
    commander = commander()

    while True:
        # Get connection info from comm
        while True:
            try:
                connection = connection_subscriber.recv_string(zmq.DONTWAIT)
            except zmq.Again:
                break
            # process task
            print(connection[2])
            commander.is_connected = int(connection[2])

        # Receive data from comm
        while True:
            try:
                data = comm_subscriber.recv_string(zmq.DONTWAIT)
            except zmq.Again:
                break
            # process task
            data = data.strip(topic.COMMAND_TOPIC + " ")
            commander.update(data)
            # print("commander received:", msg)

        # From sensors to comm, update sensors instance
        while True:
            try:
                sens_data = sensors_subscriber.recv_string(zmq.DONTWAIT)
            except zmq.Again:
                break
            # process task
            sens_data = sens_data.strip(topic.SENSOR_TOPIC + " ")
            commander.sensors.setValues(sens_data)
            commander_publisher.send_string("%s %s" % (topic.SENSOR_TOPIC, sens_data))

        # From gps to me - update gps data
        while True:
            try:
                gps_data = gps_subscriber.recv_string(zmq.DONTWAIT)
            except zmq.Again:
                break
            # process task
            gps_data = gps_data.strip(topic.GPS_TOPIC + " ")
            commander.gps.setValues(gps_data)

        commander.run()
        time.sleep(0.005)
