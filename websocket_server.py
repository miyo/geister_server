import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import options
from geister_server import GeisterServer

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")

class WebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("open websocket connection")

    def on_close(self):
        print("close websocket connection")

class WebSocket0(WebSocket):

    def on_message(self, message):
        print(message)
        g = GeisterServer()
        print(g)
        self.write_message(u"hogehoge")

class WebSocket1(WebSocket):

    def on_message(self, message):
        print(message)
        g = GeisterServer()
        print(g)
        self.write_message(u"fefe")

        
class PlayerSocket():
    
    def __init__(self):
        self.app0 = tornado.web.Application([
            (r"/", MainHandler),
            (r"/ws", WebSocket0),
        ])
        self.app0.listen(8080)
        
        self.app1 = tornado.web.Application([
            (r"/", MainHandler),
            (r"/ws", WebSocket1),
        ])
        self.app1.listen(8081)


if __name__ == "__main__":
    p = PlayerSocket()
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()

    
