# Traceroute Web Interface
 - usage:

		root# git clone http://github.com/johnnsonyue/rpi
		root# cd rpi/ && ./rpi.sh
        	... ...
		root# cd web/trace/
		#modify config.json.tpl, and rename it config.json
		... ...
		root# nohup python httpd.py >>httpd.log 2>&1 &
		root# nohup python ws.py >>ws.log 2>&1 &

- config:
	
		#replace <ip> with the IP address of your machine
		#replace app=>root_dir with $path_to_rpi/web
		#change data=>root_dir  to where you wish to store the result data
