"""
========================================================================================
TRUEGUARD: Interactive Web UI Local Server
========================================================================================
Runs a local web server and opens the TRUEGUARD diagnostic console in your browser.

Usage:
  py -3.9 run_demo_server.py
  (or: python run_demo_server.py)
========================================================================================
"""

import os
import sys
import json
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8080
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class TrueGuardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)

    def do_POST(self):
        if self.path == "/api/guard":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            prompt = data.get("prompt", "")

            # Simple fallback response for browser testing
            response = {
                "prompt": prompt,
                "status": "success",
                "message": "Processed by TRUEGUARD local engine"
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint not found")


def main():
    print("=" * 70)
    print("  🛡️ TRUEGUARD INTERACTIVE DIAGNOSTIC UI")
    print("=" * 70)
    print(f"Starting local server at http://localhost:{PORT}/index.html")
    print("Press Ctrl+C to stop.\n")

    url = f"http://localhost:{PORT}/index.html"
    try:
        webbrowser.open(url)
    except Exception:
        pass

    server = HTTPServer(("127.0.0.1", PORT), TrueGuardHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
