from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

class CanHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/data":
            self.send_response(200)
            self.send_header
        else:
            self.send_response(404)

    def do_GET(self):
        pass

class AiHttpRequestHandler(BaseHTTPRequestHandler):
    pass

def run(server_class, handler):
    address = ('localhost', 8080)
    server = server_class(address, handler)
    server.server_forever()

if __name__ == "__main__":
    run(HTTPServer, CanHTTPRequestHandler)