__author__ = 'Jernej'
from commander import commander
from comm import comm

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
            #self.client.startVideoStream()
            data = self.client.readmsg()
            #new data available
            if data != '':
                status=self.commander.update(data)
                #TODO: key commands ack ... auto, alt hold, modes
            #self.client.sendmsg("test:"+str(i))

            self.client.sendmsg(self.commander.sensors.getStrArr())
            #i+=1
            #print(time.time() * 1000)
            self.commander.control()
            #time.sleep(0.5)
        self.commander.failsafe()
        self.client.reset()






