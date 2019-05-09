#!/usr/bin/python3
from wsgiref.simple_server import make_server
# from hello import application

def application(environ, start_response):
	start_response('200 ok', [('Content-Type', 'text/html')])
	return [b'<h1>Hello, Python web!</h1>']
httpd=make_server('', 900,application)
print('serving http on port 900')
httpd.serve_forever()
