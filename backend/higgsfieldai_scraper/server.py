import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from scraper import login

queue = []


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            item = json.loads(post_data)

            if item.get("username") is None or item.get("password") is None:
                self.send_response(422)
                self.end_headers()
                return

            response = login(item["username"], item["password"])

            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()


def run(port: int):
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()
