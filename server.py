from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = "0.0.0.0"
PORT = 9000

class Handler(BaseHTTPRequestHandler):

    def send_json(self, data):
        body = json.dumps(data).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send_json({
                "success": True,
                "message": "My game server is online"
            })
        else:
            self.send_json({
                "success": False,
                "message": "Endpoint not found"
            })

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        print("POST:", self.path)
        print("Bytes:", len(body))

        self.send_json({
            "success": True,
            "endpoint": self.path,
            "message": "Request received"
        })

server = HTTPServer((HOST, PORT), Handler)

print(f"Server running on http://127.0.0.1:{PORT}")

server.serve_forever()
