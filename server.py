from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

class CanHTTPRequestHandler(BaseHTTPRequestHandler):


    def _response(self, data):
        self.send_response(200)
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        self._response("Done")
        print(str(self.rfile.read()))


    def do_GET():
        pass

class AiHttpRequestHandler(BaseHTTPRequestHandler):
    pass

def run(server_class=HTTPServer, server_handler=CanHTTPRequestHandler):
    server = server_class(('',8080),server_handler)
    server.serve_forever()

if __name__ == "__main__":
    run()