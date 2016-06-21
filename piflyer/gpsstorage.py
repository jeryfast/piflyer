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

    def getString(self):
        return self.joinDelimiter(
            [self.latitude, self.longitude, self.altitude, self.speed, self.climb, self.track, self.epx, self.epv,
             self.time, self.mode, self.nsatellites])

    # Update values if instance not doint reading with run()
    def setValues(self,string):
        self.latitude, self.longitude, self.altitude, self.speed, self.climb, self.track, self.epx, self.epv, \
        self.time, self.mode, self.nsatellites = [float(x) for x in string.split(',')]
        self.mode = int(self.mode)
        self.nsatellites = int(self.nsatellites)
