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

class SinglePageHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        user_agent = self.headers.get('User-Agent', '').lower()
        is_terminal = any(agent in user_agent for agent in ['curl', 'wget', 'httpie'])
        
        if self.path == '/first-declension':
            if is_terminal:
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                
                declension_text = terminal_renderer("first_declension.term")
                self.wfile.write(declension_text.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
                html_response = html_renderer("first_declension.html", port=PORT)
                self.wfile.write(html_response.encode('utf-8'))
            return

        elif self.path == '/second-declension':
            if is_terminal:
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                
                declension_text = terminal_renderer("second_declension.term")
                self.wfile.write(declension_text.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
                html_response = html_renderer("second_declension.html", port=PORT)
                self.wfile.write(html_response.encode('utf-8'))
            return

        elif self.path == '/third-declension':
            if is_terminal:
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                
                declension_text = terminal_renderer("third_declension.term")
                self.wfile.write(declension_text.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
                html_response = html_renderer("third_declension.html", port=PORT)
                self.wfile.write(html_response.encode('utf-8'))
            return

        elif self.path == '/fourth-declension':
            if is_terminal:
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                
                declension_text = terminal_renderer("fourth_declension.term")
                self.wfile.write(declension_text.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
                html_response = html_renderer("fourth_declension.html", port=PORT)
                self.wfile.write(html_response.encode('utf-8'))
            return

        elif self.path == '/fifth-declension':
            if is_terminal:
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                
                declension_text = terminal_renderer("fifth_declension.term")
                self.wfile.write(declension_text.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
                html_response = html_renderer("fifth_declension.html", port=PORT)
                self.wfile.write(html_response.encode('utf-8'))
            return

        latin, english = get_proverb_of_the_day()
        
        if is_terminal:
            ### Terminal response
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            
            response = terminal_renderer("base.term", latin=latin, english=english)
            self.wfile.write(response.encode('utf-8'))
        else:
            ### HTML response
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            html_response = html_renderer("base.html", latin=latin, english=english, port=PORT)
            self.wfile.write(html_response.encode('utf-8'))

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SinglePageHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            sys.exit(0)
