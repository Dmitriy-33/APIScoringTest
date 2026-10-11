import json
from store import Store
from typing import Any, Dict, Tuple, Callable
from http.server import BaseHTTPRequestHandler, HTTPServer
from app.auth import check_auth
from app.handlers import handle_online_score, handle_clients_interests

METHOD_DISPATCH: Dict[str, Callable] = {
    "online_score": handle_online_score,
    "clients_interests": handle_clients_interests,
}


class APIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON"})
            return

        login = data.get("login")
        token = data.get("token")
        method = data.get("method")
        arguments = data.get("arguments", {})

        if method not in METHOD_DISPATCH:
            self._send_response(404, {"error": "Unknown method"})
            return

        if not check_auth(login, token):
            self._send_response(403, {"error": "Forbidden"})
            return

        handler = METHOD_DISPATCH[method]
        ctx = {"request_id": "demo"}

        store = Store()

        response_body, status_code = handler(arguments, ctx, store)
        self._send_response(status_code, response_body)

    def _send_response(self, code: int, body: Dict[str, Any]):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(body, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        pass


def run_server(host: str = "localhost", port: int = 8080):
    server_address = (host, port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f"API server running on http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
