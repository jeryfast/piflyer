import os, time
os.system("/usr/bin/firefox /home/pi/piflyer/piflyer/peer1.html &")
os.system("python3 tornado_wss.py &")
time.sleep(1)
os.system("python3 zmq_sensors.py &")
os.system("python3 zmq_commander.py &")
os.system("python3 zmq_comm.py &")

