#!/usr/bin/env python3
import sys
import http.server
import socketserver
from datetime import datetime
import json

import os
PORT = int(os.environ.get("PORT", 8000))

from utils.renderers import terminal_renderer, html_renderer

with open("latin_proverbs.json", "r", encoding="utf-8") as f:
    PROVERBS = json.load(f)

with open("assets/404.txt", "r", encoding="utf-8") as f:
    ART_404 = f.read()

def get_proverb_of_the_day():
    day_of_year = datetime.now().timetuple().tm_yday
    prov = PROVERBS[day_of_year % len(PROVERBS)]
    return prov["latin"], prov["translation"]

STATIC_ROUTES = {
    '/first-declension': 'first_declension',
    '/second-declension': 'second_declension',
    '/third-declension': 'third_declension',
    '/fourth-declension': 'fourth_declension',
    '/fifth-declension': 'fifth_declension',
    '/first-conjugation': 'first_conjugation',
    '/second-conjugation': 'second_conjugation',
    '/third-conjugation': 'third_conjugation',
    '/third-io-conjugation': 'third_io_conjugation',
    '/fourth-conjugation': 'fourth_conjugation',
    '/first-declension-ex': 'first_declension_ex',
    '/second-declension-ex': 'second_declension_ex',
    '/third-declension-ex': 'third_declension_ex',
}

def serve_template(handler, template_basename, context=None, status_code=200):
    """Universally handles HTTP response formatting for both terminal and web clients."""
    if context is None:
        context = {}
    
    user_agent = handler.headers.get('User-Agent', '').lower()
    is_terminal = any(agent in user_agent for agent in ['curl', 'wget', 'httpie'])
    
    if is_terminal:
        handler.send_response(status_code)
        handler.send_header("Content-type", "text/plain; charset=utf-8")
        handler.end_headers()
        content = terminal_renderer(f"{template_basename}.term", **context)
        handler.wfile.write(content.encode('utf-8'))
    else:
        handler.send_response(status_code)
        handler.send_header("Content-type", "text/html; charset=utf-8")
        handler.end_headers()
        content = html_renderer(f"{template_basename}.html", **context)
        handler.wfile.write(content.encode('utf-8'))

class SinglePageHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in STATIC_ROUTES:
            serve_template(self, STATIC_ROUTES[self.path], {"port": PORT})
            return

        if self.path.startswith('/assets/'):
            try:
                file_path = self.path.lstrip('/')
                with open(file_path, "rb") as f:
                    self.send_response(200)
                    if file_path.endswith(".png"):
                        self.send_header("Content-type", "image/png")
                    elif file_path.endswith(".txt"):
                        self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(f.read())
                return
            except FileNotFoundError:
                pass

        if self.path == '/':
            # Default to Proverb of the Day for Home
            latin, english = get_proverb_of_the_day()
            serve_template(self, "base", {"latin": latin, "english": english, "port": PORT})
            return

        # 404 for everything else
        serve_template(self, "404", {"port": PORT, "path": self.path, "art": ART_404}, status_code=404)

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SinglePageHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            sys.exit(0)
