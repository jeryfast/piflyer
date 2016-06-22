import random as r
from gps import *
import time
import threading
import zmq
import zmq_ports as ports
import zmq_topics as topic
import delays

gpsd = None  # seting the global variable
class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd  # bring it in scope
        gpsd = gps(mode=WATCH_ENABLE)  # starting the stream of info
        self.current_value = None
        self.running = True  # setting the thread running to true

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()  # this will continue to loop and grab EACH set of gpsd info to clear the buffer

class gpsdata():
    def __init__(self):
        self.latitude=0
        self.longitude=0
        self.altitude=0
        self.speed=0
        self.climb=0
        self.track=0
        self.epx=0
        self.epv=0
        self.utc = 0
        self.time = 0
        self.mode = 0
        self.nsatellites = 0

    def joinDelimiter(self, arr):
        tmp=[None]*len(arr)
        for i in range(len(arr)):
            tmp[i]=str(arr[i])
        return ",".join(tmp)

    def getRandomStrArr(self):
        pass

    def run(self):
        try:
            while True:
                self.latitude = gpsd.fix.latitude
                self.longitude = gpsd.fix.longitude
                self.altitude = gpsd.fix.altitude
                self.speed = gpsd.fix.speed
                self.climb = gpsd.fix.climb
                self.track = gpsd.fix.track
                self.epx = round(gpsd.fix.epx,1)
                self.epv = round(gpsd.fix.epv,1)
                self.utc = gpsd.utc
                self.time = gpsd.fix.time
                self.mode = gpsd.fix.mode
                self.nsatellites = len(gpsd.satellites)
                gps_publisher.send_string("%s %s" % (topic.GPS_TOPIC, self.getString()))
                time.sleep(delays.GPS_REFRESH_DELAY)

        except (KeyboardInterrupt, SystemExit):
            # when you press ctrl+c
            print("\nKilling Thread...")
            gpsp.running = False
            gpsp.join()
        print("Done.\nExiting.")

    def getString(self):
        return self.joinDelimiter(
            [self.latitude, self.longitude, self.altitude, self.speed, self.climb, self.track, self.epx, self.epv,
             self.mode, self.nsatellites])

    # Update values if instance not doint reading with run()
    def setValues(self,string):
        self.latitude, self.longitude, self.altitude, self.speed, self.climb, self.track, self.epx, self.epv, \
        self.mode, self.nsatellites = [float(x) for x in string.split(',')]
        self.mode = int(self.mode)
        self.nsatellites = int(self.nsatellites)

if __name__ == '__main__':
    # Publisher
    context = zmq.Context()
    gps_publisher = context.socket(zmq.PUB)
    gps_publisher.bind("tcp://*:%s" % ports.GPS_PUB)
    # create, start thread
    gpsp = GpsPoller()
    gpsp.start()
    #
    mygps = gpsdata()
    mygps.run()





