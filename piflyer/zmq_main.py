import os, time
os.system("v4l2-ctl --set-fmt-video=width=720,height=480,pixelformat=H264 -p 30")
os.system("v4l2-ctl --set-ctrl video_bitrate=500000")
os.system("v4l2-ctl --set-ctrl h264_profile=baseline")
os.system("export DISPLAY=:99")
#os.system("sudo xvfb-run /usr/bin/firefox /home/pi/piflyer/piflyer/peer1.html &")
os.system("/usr/bin/firefox /home/pi/piflyer/piflyer/peer1.html &")
os.system("python3 tornado_wss.py &")
time.sleep(1)
os.system("python3 zmq_sensors.py &")
os.system("python zmq_gps.py &")
os.system("python3 zmq_commander.py &")
os.system("python3 zmq_comm.py &")

