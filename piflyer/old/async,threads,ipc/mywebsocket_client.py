from websocket import create_connection, WebSocket, socket
from time import time
ws = create_connection("ws://localhost:9001/websocket")
while True:
    print ("Sending ")
    t=time()
    ws.send("test")
    #print("time: ",time()-t)
    #print ("Reeiving...")
    result =  ws.recv()
    print ("Received '%s'" % result, time()-t)
ws.close()

