import datetime
import time
import json
import os
import subprocess
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

class WSApplication(tornado.web.Application):
	def __init__(self, handlers, config):
		tornado.web.Application.__init__(self, handlers)
		self.config = config

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
		user = "anonymous"
		config = self.application.config
		data_dir = config["data"]["root_dir"]
		output_dir = data_dir+"/"+user
		if not os.path.exists(output_dir):
			self.write_message(json.dumps({"result_list":{}}))
		else:
			h = subprocess.Popen("ls "+output_dir+" | grep mark", shell=True, stdout=subprocess.PIPE)
			result_list = h.stdout.read().splitlines()
			self.write_message(json.dumps({"result_list":result_list}))

		tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=5), self.scheduled) 

if __name__ == '__main__':
	config = json.loads(open("config.json").read())
	HOST_NAME = config["app"]["host_name"]
	WSPORT_NUMBER = config["app"]["wsport_number"]

	application = WSApplication([(r'/ws', WSHandler),], config)
	ws_server = tornado.httpserver.HTTPServer(application)
	ws_server.listen(WSPORT_NUMBER)

	print time.asctime(), "WS Server Starts - %s:%s" % (HOST_NAME, WSPORT_NUMBER)
	try:
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		pass
	print time.asctime(), "WS Server Stops - %s:%s" % (HOST_NAME, WSPORT_NUMBER)
