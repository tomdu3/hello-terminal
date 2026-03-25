#!/usr/bin/env python3
import sys
import http.server
import socketserver
from datetime import datetime

PORT = 8000

# ANSI colors
class Colors:    
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

ASCII_ART = f"""{Colors.OKCYAN}{Colors.BOLD}
  _____                   _             _ 
 |_   _|___ _ __ _ __ ___(_)_ __   __ _| |
   | |/ _ \\ '__| '_ ` _ \\| | '_ \\ / _` | |
   | |  __/ |  | | | | | | | | | | (_| | |
   |_|\\___|_|  |_| |_| |_|_|_| |_|\\__,_|_|
{Colors.ENDC}"""

PROVERBS = [
    ("Carpe diem", "Seize the day"),
    ("Veni, vidi, vici", "I came, I saw, I conquered"),
    ("Audentes fortuna iuvat", "Fortune favors the bold"),
    ("Ad astra per aspera", "To the stars through difficulties"),
    ("Cogito ergo sum", "I think, therefore I am"),
    ("Dum spiro, spero", "While I breathe, I hope"),
    ("Per aspera ad astra", "Through hardships to the stars"),
    ("Ars longa, vita brevis", "Art is long, life is short"),
    ("In vino veritas", "In wine there is truth")
]

def get_proverb_of_the_day():
    day_of_year = datetime.now().timetuple().tm_yday
    return PROVERBS[day_of_year % len(PROVERBS)]

class SinglePageHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        user_agent = self.headers.get('User-Agent', '').lower()
        is_terminal = any(agent in user_agent for agent in ['curl', 'wget', 'httpie'])
        
        latin, english = get_proverb_of_the_day()
        
        if is_terminal:
            ### Terminal response
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            
            response = (
                f"{ASCII_ART}\n"
                f"{Colors.OKGREEN}Latin Proverb of the Day:{Colors.ENDC}\n"
                f"{Colors.BOLD}{latin}{Colors.ENDC} - {english}\n\n"
            )
            self.wfile.write(response.encode('utf-8'))
        else:
            ### HTML response
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            with open("templates/base.html", "r", encoding="utf-8") as f:
                html_template = f.read()
            
            html_response = html_template.replace("{{latin}}", latin).replace("{{english}}", english).replace("{{port}}", str(PORT))
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
