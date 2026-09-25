from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 9000))


class Handler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()

        self.send_response(status)
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
                "error": "not_found",
                "message": "Endpoint not found"
            }, 404)

    def do_POST(self):

        try:
            length = int(self.headers.get("Content-Length", 0))

            if length > 1024 * 1024:
                self.send_json({
                    "success": False,
                    "error": "payload_too_large"
                }, 413)
                return

            body = self.rfile.read(length)

            print("POST:", self.path)
            print("Bytes:", len(body))

            responses = {
                "/majorlogin": "Login request received",
                "/Getbackpack": "Backpack request received",
                "/Getlogindata": "Login data request received",
                "/logingetdesc": "Login description request received",
                "/Getgachadesc": "Gacha description request received",
                "/tcp": "TCP test endpoint received"
            }

            if self.path in responses:
                self.send_json({
                    "success": True,
                    "endpoint": self.path,
                    "message": responses[self.path]
                })
            else:
                self.send_json({
                    "success": False,
                    "error": "not_found",
                    "message": "Endpoint not found"
                }, 404)

        except Exception as e:
            print("Request error:", e)

            self.send_json({
                "success": False,
                "error": "server_error",
                "message": "Request could not be processed"
            }, 500)

    def do_PUT(self):
        self.send_json({
            "success": False,
            "error": "method_not_allowed",
            "message": "PUT is not supported"
        }, 405)

    def do_DELETE(self):
        self.send_json({
            "success": False,
            "error": "method_not_allowed",
            "message": "DELETE is not supported"
        }, 405)

    def do_PATCH(self):
        self.send_json({
            "success": False,
            "error": "method_not_allowed",
            "message": "PATCH is not supported"
        }, 405)


server = HTTPServer((HOST, PORT), Handler)

print(f"Game server running on port {PORT}")

server.serve_forever()
