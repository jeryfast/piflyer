import os


def shutdown():
    print("system shutdown initiated")
    os.system("sudo pkill firefox-esr")
    os.system("sudo halt")
    os.system("pkill python")

