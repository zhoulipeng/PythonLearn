import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from json import loads
from tornado.options import define, options
define("port", default=8885, help="run on the given port", type=int)

class PublishHandler(tornado.web.RequestHandler):
    def post(self):
        values = loads(self.request.body)
        print "Publish:", values
        self.write("0")

class UnpublishHandler(tornado.web.RequestHandler):
    def post(self):
        values = loads(self.request.body)
        print "Unpublish:", values
        self.write("0")

class ConnectHandler(tornado.web.RequestHandler):
    def post(self):
        values = loads(self.request.body)
        print "Connect:", values
        self.write("0")

class CloseHandler(tornado.web.RequestHandler):
    def post(self):
        values = loads(self.request.body)
        print "Close:", values
        self.write("0")

class PlayHandler(tornado.web.RequestHandler):
    def post(self):
        values = loads(self.request.body)
        print "Play:", values
        self.write("0")

class StopHandler(tornado.web.RequestHandler):
    def post(self):
        values = loads(self.request.body)
        print "Stop:", values
        self.write("0")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/publish", PublishHandler),
		(r"/unpublish", UnpublishHandler),
		(r"/connect", ConnectHandler),
		(r"/close", CloseHandler),
		(r"/play", PlayHandler),
		(r"/stop", StopHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
