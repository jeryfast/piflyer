import zmq
import zmq_ports
import sys
import time

def joinDelimiter(arr):
    tmp = [None] * len(arr)
    for i in range(len(arr)):
        tmp[i] = str(arr[i])
    return ",".join(tmp)

port = zmq_ports.SERVER_PORT
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
if len(sys.argv) > 2:
    socket.connect ("tcp://localhost:%s" % port1)

#  Do 10 requests, waiting each time for a response
for request in range (1,100):
    #print ("Sending request ", request,"...")
    #joinDelimiter([1,2,3,4,5,6,7,8,9,10])
    socket.send_string(joinDelimiter([1,2,3,4,5,6,7,8,9,10,time.time()]))
    #  Get the reply.
    message = socket.recv()
    #print ("Received reply ", request, "[", message, "]")