import random
import time
import zmq
import zmq_ports as ports

# Publisher
context = zmq.Context()
comm_publisher = context.socket(zmq.PUB)
comm_publisher.bind("tcp://*:%s" % ports.COMMANDER_PUB)

# Subscribe to commander
topic = "10001"
comm_subscriber = context.socket(zmq.SUB)
comm_subscriber.connect("tcp://localhost:%s" % ports.COMM_PUB)
comm_subscriber.setsockopt_string(zmq.SUBSCRIBE, topic)

# Subscribe to sensors
sensors_subscriber = context.socket(zmq.SUB)
sensors_subscriber.connect("tcp://localhost:%s" % ports.SENSORS_PUB)
sensors_subscriber.setsockopt_string(zmq.SUBSCRIBE, topic)

while True:
    # send data
    #topic = random.randrange(9999, 10001)
    messagedata = random.randrange(1, 215) - 80
    #print("%d %d" % (topic, messagedata))
    #comm_publisher.send_string("%s %s" % (topic, "test"))

    while True:
        # receive data from comm
        try:
            msg = comm_subscriber.recv_string(zmq.DONTWAIT)
        except zmq.Again:
            break
        # process task
        #print("commander received:", msg)

    while True:
        # from sensors to comm
        try:
            sens_data = sensors_subscriber.recv_string(zmq.DONTWAIT)
        except zmq.Again:
            break
        # process task
        sens_data = sens_data.strip(topic + " ")
        comm_publisher.send_string("%s %s" % (topic, sens_data))
    time.sleep(0.005)

