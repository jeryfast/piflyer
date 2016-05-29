__author__ = 'Jernej'
import socket

import piflyer.commands as c
from piflyer.commander import commander

TCP_PORT = 13000
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

class mainserver:
    def __init__(self):
        self.conn=""
        self.addr=""
    def run(self):
        #create an INET, STREAMing socket
        self.s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connect to a server port
        self.s.bind(("0.0.0.0", TCP_PORT))
        print(socket.gethostname())
        self.s.listen(1)
        #client must connect within timeout for safety reasons
        self.s.settimeout(5)
        self.conn, self.addr = self.s.accept()
        print ('Connection address:', self.addr)
        result=""
        #while connection not broken by client
        while result!=c.DISCONNECT:
            data = self.conn.recv(BUFFER_SIZE)
            if not data:break
            data=data.decode("utf-8")
            print("Received:"+data)
            #execute commands
            result=commander.execute(data)
            print(result)
            self.conn.send(result.encode("utf-8"))
        self.conn.close()






