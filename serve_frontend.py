"""
Simple HTTP Server for TrueSight Frontend.

Sends aggressive no-cache headers so browsers always pick up the latest
HTML/CSS/JS during demo iteration — eliminates the "I changed the file but
nothing updated" class of bug.
"""

import http.server
import socketserver
import os
import sys
import threading
import webbrowser
from pathlib import Path

# Force UTF-8 stdout so the print() emojis below don't crash on Windows cp1252.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler + Cache-Control: no-store on every response."""

    def end_headers(self):
        # Tell every client (browser, proxy, CDN) to fetch fresh every time.
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        # Cross-origin so the page can fetch from any local dev backend.
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    # Override the default 304-by-If-Modified-Since path; with no-store
    # browsers won't send If-Modified-Since, but be defensive anyway.
    def send_head(self):
        return super().send_head()


class FrontendServer:
    def __init__(self, port=3000):
        self.port = port
        self.directory = Path(__file__).parent / "frontend"

    def start_server(self):
        os.chdir(self.directory)

        # Allow rapid restarts without "address already in use".
        socketserver.TCPServer.allow_reuse_address = True

        with socketserver.TCPServer(("", self.port), NoCacheHandler) as httpd:
            print(f"[TrueSight] Frontend Server running at http://localhost:{self.port}")
            print(f"[TrueSight] Serving files from: {self.directory}")
            print("[TrueSight] Cache-Control: no-store (browsers will always fetch fresh)")
            print("[TrueSight] Press Ctrl+C to stop the server")
            print("-" * 60)

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n[TrueSight] Frontend server stopped")
                httpd.shutdown()


def main():
    server = FrontendServer(port=3000)

    server_thread = threading.Thread(target=server.start_server)
    server_thread.daemon = True
    server_thread.start()

    import time
    time.sleep(2)

    print("[TrueSight] Opening browser...")
    webbrowser.open(f"http://localhost:3000")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[TrueSight] Goodbye.")


if __name__ == "__main__":
    main()
