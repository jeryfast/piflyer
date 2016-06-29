import os, time
def shutdown():
    os.system("sudo pkill firefox-esr")
    os.system("pkill python")
    os.system("sudo halt")
