import time

__author__ = 'Jernej'
import piflyer.commands as c
from piflyer.commander import commander
from piflyer.comm import comm
import time
import random as r
D=","

class mainserver:
    def __init__(self):
        self.client=comm()
        self.commander=commander()
    def run(self):
        status=""
        data=""
        #while connection not broken by client
        #while result!=c.DISCONNECT:
        i=0
        while self.client.connected():
            self.client.startVideoStream()
            data = self.client.readmsg()
            #new data available
            if data != '':
                #data=data.decode("utf-8")
                #print("Received: "+data)
                #execute commands
                #result=self.commander.update(data)
                #print("Commander: "+result)
                #self.client.sendmsg(result)
                #self.conn.send(result.encode("utf-8"))"""
                status=self.commander.update(data)
            #self.client.sendmsg("test:"+str(i))
            pitch = str(r.randint(3, 5))
            roll = str(r.randint(3, 5))
            yaw = str(r.randint(0, 2))
            compass=str(r.randint(240,241))
            temp=str(r.randint(19,20))
            humidity=str(r.randint(43,46))
            pressure=str(r.randint(983,985))
            altitude = "286"
            self.client.sendmsg(pitch+D+roll+D+yaw+D+compass+D+temp+D+humidity+D+pressure+",0.00,0.00,0.00"+D+altitude)
            #i+=1
            #print(time.time() * 1000)
            self.commander.control()
            #time.sleep(0.5)
        self.commander.failsafe()
        self.client.reset()






