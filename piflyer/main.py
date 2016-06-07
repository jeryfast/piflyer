__author__ = 'Jernej'
import sys
from mainserver import mainserver

s = mainserver()

print("Starting Main ...")
print("Starting a python server ...")
while 1:
    try:
        s.run()
    except:
        print(sys.exc_info())
        s.client.close()
