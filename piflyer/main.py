__author__ = 'Jernej'
import sys
#from piflyer.initclient import initclient
#from piflyer.mainserver import mainserver
#initclient = initclient()
#mainserver = mainserver()
from piflyer.mainserver1 import mainserver
s = mainserver()

print("Starting Main ...")
print("Starting a python server ...")
while 1:
    try:
        """if(initclient.connect()):
            print("Client connected :)")
            #start a server
            print("Starting a server ...")
            mainserver.run()
        else:
            print("Server not started ...")"""
        #s.client.connect()
        #if(s.client.connected()):

        s.run()
        #s.client.reset()
    except:
        print(sys.exc_info())
        s.client.close()
