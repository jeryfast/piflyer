__author__ = 'Jernej'
import sys
from mainserver import mainserver

if __name__ == '__main__':
    s = mainserver()
    if __name__ == '__main__':
        print("Starting main server ...")
        while 1:
            try:
                s.run()
            except:
                s.client.close()
                print(sys.exc_info())
        sys.exit(0)

