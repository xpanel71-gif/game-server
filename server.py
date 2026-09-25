from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 9000))


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
                "server": "game-server",
                "status": "online"
            })

        elif self.path == "/status":
            self.send_json({
                "success": True,
                "server": "game-server",
                "status": "online",
                "endpoints": [
                    "/majorlogin",
                    "/Getbackpack",
                    "/Getlogindata",
                    "/logingetdesc",
                    "/Getgachadesc",
                    "/tcp"
                ]
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

        if self.path == "/majorlogin":
            self.send_json({
                "success": True,
                "endpoint": "/majorlogin",
                "message": "Login request received"
            })

        elif self.path == "/Getbackpack":
            self.send_json({
                "success": True,
                "endpoint": "/Getbackpack",
                "message": "Backpack request received"
            })

        elif self.path == "/Getlogindata":
            self.send_json({
                "success": True,
                "endpoint": "/Getlogindata",
                "message": "Login data request received"
            })

        elif self.path == "/logingetdesc":
            self.send_json({
                "success": True,
                "endpoint": "/logingetdesc",
                "message": "Login description request received"
            })

        elif self.path == "/Getgachadesc":
            self.send_json({
                "success": True,
                "endpoint": "/Getgachadesc",
                "message": "Gacha description request received"
            })

        elif self.path == "/tcp":
            self.send_json({
                "success": True,
                "endpoint": "/tcp",
                "message": "TCP test endpoint received"
            })

        else:
            self.send_json({
                "success": False,
                "message": "Endpoint not found"
            })


server = HTTPServer((HOST, PORT), Handler)

print(f"Game server running on port {PORT}")

server.serve_forever()
