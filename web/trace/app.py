import os
import time
import datetime
import json
import BaseHTTPServer
from SocketServer import ThreadingMixIn

import cgi
import subprocess

import ip

class Server(BaseHTTPServer.HTTPServer):
	def __init__(self, (HOST_NAME, PORT_NUMBER), handler, config):
		BaseHTTPServer.HTTPServer.__init__(self, (HOST_NAME, PORT_NUMBER), handler)
		self.config = config

class ThreadedHTTPServer(ThreadingMixIn, Server):
	def __init__(self, (HOST_NAME, PORT_NUMBER), handler, config):
		Server.__init__(self, (HOST_NAME, PORT_NUMBER), handler, config)
	
class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
	def do_GET(self):
		config = json.loads(open("config.json").read())
		url_path = self.path.lstrip('/')
		file_path = config["app"]["root_dir"] + "/" + url_path

		if os.path.exists(file_path):
			self.send_response(200)
			suffix = file_path.split('.')[-1]
			if suffix == "css":
				self.send_header("Content-type", "text/css")
			elif suffix == "js":
				self.send_header("Content-type", "text/script")
			elif suffix == "svg":
				self.send_header("Content-type", "image/svg+xml")
			else:
				self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write(open(file_path,'rb').read())
                elif url_path.split('?')[0] == "download":
			get = {}
			for x in url_path.split('?')[1].split('&'):
				get[x.split('=')[0]] = x.split('=')[1]
			if get["file"] and get["type"]:
				download_path = get["file"]
				download_type = get["type"]
				if os.path.exists(download_path):
					self.send_response(200)
					self.end_headers()
					if (download_type == "target"):
						self.wfile.write(open(download_path,'rb').read())
					elif (download_type == "trace"):
						h = subprocess.Popen("sc_warts2text "+download_path, shell=True, stdout=subprocess.PIPE)
						self.wfile.write(h.stdout.read())
					elif (download_type == "links"):
						self.wfile.write("1.in 2.out 3.is_dest 4.star 5.delay 6.freq 7.ttl 8.monitor 9.firstseen 10.lastseen\n")
						h = subprocess.Popen("./decode -t caida -f "+download_path+" | python trace2link.py", shell=True, stdout=subprocess.PIPE)
						self.wfile.write(h.stdout.read())
				else:
					self.send_response(404)
					self.end_headers()
			else:
				self.send_response(404)
				self.end_headers()
		else:
			self.send_response(404)
			self.end_headers()
			
	def do_POST(self):
		action = self.path.replace('/','')
		valid_action = ["trace", "list", "read", "remove"]
		if ( action not in valid_action ):
			self.send_response(505)
			self.end_headers()
			self.wfile.write("Invalid Action: %s" % action)
			return
		
		config = self.server.config
		post = cgi.FieldStorage(
			fp=self.rfile, 
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
			'CONTENT_TYPE':self.headers['Content-Type'],
		})

		config = json.loads(open("config.json").read())
		data_dir = config["data"]["root_dir"]
		if ( action == "trace" ):
			if post.has_key("target") or post.has_key("file"):
                                if post.has_key("target"):
					target = post["target"].value
				else:
					target = post["file"].value
				target = ip.process(target)

				user = "anonymous"
				node_name = config["app"]["node_name"]
				date = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
				output_dir = data_dir+"/"+user
				target_file_path = output_dir+"/"+date+"."+node_name+".target"

				if not os.path.exists(output_dir):
					os.makedirs(output_dir)
				fp = open(target_file_path, 'wb')
				fp.write(target)
				fp.close()

				h = subprocess.Popen(["./db","trace", target_file_path, output_dir], stdout=subprocess.PIPE)
				result = h.stdout.read()
				self.send_response(200)
				self.end_headers()
				self.wfile.write(result)
		elif ( action == "list" ):
				user = "anonymous"
				output_dir = data_dir+"/"+user

				h = subprocess.Popen(["./db","list", output_dir], stdout=subprocess.PIPE)
				result = h.stdout.read()
				self.send_response(200)
				self.end_headers()
				self.wfile.write(result)
		elif ( action == "remove" ):
			if post.has_key("rm_list"):
				rm_list = post["rm_list"].value
				user = "anonymous"
				output_dir = data_dir+"/"+user

				h = subprocess.Popen(["./db","remove", output_dir, rm_list], stdout=subprocess.PIPE)
				result = h.stdout.read()
				self.send_response(200)
				self.end_headers()
				self.wfile.write(result)
		elif ( action == "read" ):
			if post.has_key("read_list"):
				read_list = post["read_list"].value
				user = "anonymous"
				output_dir = data_dir+"/"+user

				h = subprocess.Popen(["./db","seen", output_dir, read_list], stdout=subprocess.PIPE)
				result = h.stdout.read()
				self.send_response(200)
				self.end_headers()
				self.wfile.write(result)
