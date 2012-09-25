from cgi import parse_qs
from wsgiref.simple_server import make_server

def simple_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)
    print("hello")
httpd = make_server('', 1337, simple_app)
# print "Serving on port 1337..."
httpd.serve_forever()
