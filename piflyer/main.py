__author__ = 'Jernej'
import sys
from mainserver import mainserver

s = mainserver()

print("Starting main server ...")
while 1:
    try:
        s.run()
    except:
        s.client.close()
        print(sys.exc_info())

