#!/usr/bin/env python3
import sys
import http.server
import socketserver
from datetime import datetime
import json

PORT = 8000

from utils.renderers import terminal_renderer, html_renderer

with open("latin_proverbs.json", "r", encoding="utf-8") as f:
    PROVERBS = json.load(f)

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
}

def serve_template(handler, template_basename, context=None):
    """Universally handles HTTP response formatting for both terminal and web clients."""
    if context is None:
        context = {}
    
    user_agent = handler.headers.get('User-Agent', '').lower()
    is_terminal = any(agent in user_agent for agent in ['curl', 'wget', 'httpie'])
    
    if is_terminal:
        handler.send_response(200)
        handler.send_header("Content-type", "text/plain; charset=utf-8")
        handler.end_headers()
        content = terminal_renderer(f"{template_basename}.term", **context)
        handler.wfile.write(content.encode('utf-8'))
    else:
        handler.send_response(200)
        handler.send_header("Content-type", "text/html; charset=utf-8")
        handler.end_headers()
        content = html_renderer(f"{template_basename}.html", **context)
        handler.wfile.write(content.encode('utf-8'))

class SinglePageHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in STATIC_ROUTES:
            serve_template(self, STATIC_ROUTES[self.path], {"port": PORT})
            return

        # Default to Proverb of the Day
        latin, english = get_proverb_of_the_day()
        serve_template(self, "base", {"latin": latin, "english": english, "port": PORT})

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SinglePageHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            sys.exit(0)
