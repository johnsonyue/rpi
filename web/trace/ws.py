import datetime
import time
import json
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

class WSHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		self.scheduled()
	  
	def on_message(self, message):
		return
 
	def on_close(self):
		return
 
	def check_origin(self, origin):
		return True

	def scheduled(self):
		self.write_message("Hello,world!")
		tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=5), self.scheduled) 

if __name__ == '__main__':
	config = json.loads(open("config.json").read())
	HOST_NAME = config["app"]["host_name"]
	WSPORT_NUMBER = config["app"]["wsport_number"]

	application = tornado.web.Application([(r'/ws', WSHandler),])
	ws_server = tornado.httpserver.HTTPServer(application)
	ws_server.listen(WSPORT_NUMBER)

	print time.asctime(), "WS Server Starts - %s:%s" % (HOST_NAME, WSPORT_NUMBER)
	try:
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		pass
	print time.asctime(), "WS Server Stops - %s:%s" % (HOST_NAME, WSPORT_NUMBER)
