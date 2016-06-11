import zmq
import zmq_ports
import time
import sys

sensor_port = zmq_ports.SERVER_PORT
comm_port = zmq_ports.COMM_PORT
commander_port = zmq_ports.COMMANDER_PORT
sensors_port = zmq_ports.SENSORS_PORT

if len(sys.argv) > 1:
    port =  sys.argv[1]

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

while True:
    #  Wait for next request from client
    message = socket.recv_string()
    message=message.split(",")
    if(message!=""):
        print ("Received request: ", time.time()-float(message[-1]))
        time.sleep (0.01)
        socket.send_string("World from %s" % port)