import os, time
def shutdown():
    print("system shutdown initiated")
    os.system("sudo pkill firefox-esr")
    os.system("pkill python")
    os.system("sudo halt")
