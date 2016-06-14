import tornado.ioloop
import tornado.web
import tornado.websocket
import zmq
import zmq_ports as ports
import zmq_topics as topic
from tornado.options import define, options, parse_command_line

define("port", default=9000, type=int)

# IPC
context = zmq.Context()
browser_publisher = context.socket(zmq.PUB)
browser_publisher.bind("tcp://*:%s" % ports.TORNADO_PUB)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = []
    def check_origin(self, origin):
        return True

    def open(self, *args):
        print ("New connection")
        self.clients.append(self)
        #self.write_message("Welcome!")

    def on_message(self, message):
        #print ("New message {}".format(message))
        clients=self.clients.copy()
        count = clients.__len__()
        while count >= 1:
            client=clients.pop()
            count-=1
            if client!=self:
                if message[0]=='_':
                    #print("sending message to browser")
                    message = message.strip('_')
                    client.write_message(message)
                else:
                    browser_publisher.send_string("%s %s" % (topic.COMMAND_TOPIC, message))

    def on_close(self):
        print ("Connection closed")
        self.clients.remove(self)

if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/', IndexHandler),
        (r'/ws/', WebSocketHandler),
    ])
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
