#!/usr/bin/env python3

from mmodules import rest

def application(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	
	try:
		id = str(int(environ.get('PATH_INFO', '')[1:]))
	except:
		id = ''
	
	if id:
		rest.key_value = rest.kv.KeyValue(id, rest.send)
		body = rest.key_value.manifest()
		if not body:
			body = '{"match_unread":0,"match_count":0,"msg_unread":0,"msg_count":0}'
	else:
		body = ''
	
	return [body.encode('utf-8')]


if __name__ == '__main__':
	port = 6726
	from wsgiref.simple_server import make_server
	server = make_server('', port, application)
	print('Manifesting on port {}...'.format(port))
	server.serve_forever()
