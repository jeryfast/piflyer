import zmq
import random
import time

import browser_controller
import zmq_ports as ports
import zmq_topics as topic
from selenium import webdriver
import os
from pyvirtualdisplay import Display
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from websocket import create_connection

RCV_DELAY=0.01
WSPORT = 9000

########### WEBSOCKET EVENTS

########### WEBSOCKET EVENTS
if __name__ == '__main__':
    #print("Starting comm")
    # IPC
    context = zmq.Context()

    # Publisher
    comm_publisher = context.socket(zmq.PUB)
    comm_publisher.bind("tcp://*:%s" % ports.COMM_PUB)

    # Subscribe to commander
    commander_subscriber = context.socket(zmq.SUB)
    commander_subscriber.connect("tcp://localhost:%s" % ports.COMMANDER_PUB)
    commander_subscriber.setsockopt_string(zmq.SUBSCRIBE, topic.SENSOR_TOPIC)

    # Subscribe to Tornado websocket server
    browser_subscriber = context.socket(zmq.SUB)
    browser_subscriber.connect("tcp://localhost:%s" % ports.TORNADO_PUB)
    browser_subscriber.setsockopt_string(zmq.SUBSCRIBE, topic.COMMAND_TOPIC)

    # Web scoket for sending data to the browser
    ws = create_connection("ws://localhost:9000/ws/")

    # Open a browser
    browser_controller.start()
    connected=False

    while True:
        #xcomm.startVideoStream()
        # from browser to commander
        while True:
            try:
                msg = browser_subscriber.recv_string(zmq.DONTWAIT)
            except zmq.Again:
                break
            # process task
            msg = msg.strip(str(topic.COMMAND_TOPIC) + " ")
            print("from browser:", msg)
            # Connection state
            if(msg[0]=="Q"):
                comm_publisher.send_string("%s %s" % (topic.CONNECTION_TOPIC, msg[1]))
                connected=msg[1]
            else:
                comm_publisher.send_string("%s %s" % (topic.COMMAND_TOPIC, msg))

        # from commander to browser
        while True:
            try:
                msg = commander_subscriber.recv_string(zmq.DONTWAIT)
                msg=msg.strip(str(topic.SENSOR_TOPIC)+" ")
                #print(msg)
                #xcomm.sendMsg(msg)
            except zmq.Again:
                break
            # process task
            if(connected):
                ws.send("_" + msg)
            #print("comm received:", msg)
        time.sleep(0.005)

    ws.close()


