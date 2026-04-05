#!/usr/bin/env python3
import sys
import http.server
import socketserver
from datetime import datetime
import json

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
                
                declension_text = (
                    f"{Colors.OKCYAN}{Colors.BOLD}First Latin Declension (-a, -ae){Colors.ENDC}\n\n"
                    f"{Colors.OKGREEN}Singular:{Colors.ENDC}\n"
                    f"  Nom: -a     (terr-a)\n"
                    f"  Gen: -ae    (terr-ae)\n"
                    f"  Dat: -ae    (terr-ae)\n"
                    f"  Acc: -am    (terr-am)\n"
                    f"  Abl: -ā     (terr-ā)\n"
                    f"  Voc: -a     (terr-a)\n\n"
                    f"{Colors.OKGREEN}Plural:{Colors.ENDC}\n"
                    f"  Nom: -ae    (terr-ae)\n"
                    f"  Gen: -ārum  (terr-ārum)\n"
                    f"  Dat: -īs    (terr-īs)\n"
                    f"  Acc: -ās    (terr-ās)\n"
                    f"  Abl: -īs    (terr-īs)\n"
                    f"  Voc: -ae    (terr-ae)\n\n"
                    f"{Colors.BOLD}Rules:{Colors.ENDC}\n"
                    f"- Mostly feminine nouns (e.g., puella, insula).\n"
                    f"- Exceptions include some masculine nouns denoting occupations (e.g., nauta, agricola, poēta).\n\n"
                )
                self.wfile.write(declension_text.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
                with open("templates/first_declension.html", "r", encoding="utf-8") as f:
                    html_template = f.read()
                
                html_response = html_template.replace("{{port}}", str(PORT))
                self.wfile.write(html_response.encode('utf-8'))
            return

        elif self.path == '/second-declension':
            if is_terminal:
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                
                declension_text = (
                    f"{Colors.OKCYAN}{Colors.BOLD}Second Latin Declension (-us, -i / -um, -i){Colors.ENDC}\n\n"
                    f"{Colors.BOLD}Masculine (-us){Colors.ENDC}\n"
                    f"{Colors.OKGREEN}Singular:{Colors.ENDC}\n"
                    f"  Nom: -us    (serv-us)\n"
                    f"  Gen: -ī     (serv-ī)\n"
                    f"  Dat: -ō     (serv-ō)\n"
                    f"  Acc: -um    (serv-um)\n"
                    f"  Abl: -ō     (serv-ō)\n"
                    f"  Voc: -e     (serv-e)\n\n"
                    f"{Colors.OKGREEN}Plural:{Colors.ENDC}\n"
                    f"  Nom: -ī     (serv-ī)\n"
                    f"  Gen: -ōrum  (serv-ōrum)\n"
                    f"  Dat: -īs    (serv-īs)\n"
                    f"  Acc: -ōs    (serv-ōs)\n"
                    f"  Abl: -īs    (serv-īs)\n"
                    f"  Voc: -ī     (serv-ī)\n\n"
                    f"{Colors.BOLD}Neuter (-um){Colors.ENDC}\n"
                    f"{Colors.OKGREEN}Singular:{Colors.ENDC}\n"
                    f"  Nom: -um    (bell-um)\n"
                    f"  Gen: -ī     (bell-ī)\n"
                    f"  Dat: -ō     (bell-ō)\n"
                    f"  Acc: -um    (bell-um)\n"
                    f"  Abl: -ō     (bell-ō)\n"
                    f"  Voc: -um    (bell-um)\n\n"
                    f"{Colors.OKGREEN}Plural:{Colors.ENDC}\n"
                    f"  Nom: -a     (bell-a)\n"
                    f"  Gen: -ōrum  (bell-ōrum)\n"
                    f"  Dat: -īs    (bell-īs)\n"
                    f"  Acc: -a     (bell-a)\n"
                    f"  Abl: -īs    (bell-īs)\n"
                    f"  Voc: -a     (bell-a)\n\n"
                    f"{Colors.BOLD}Rules:{Colors.ENDC}\n"
                    f"- Includes mostly masculine (-us, -er, -ir) and neuter (-um) nouns.\n"
                    f"- Neuter Rule: Nominative, accusative, and vocative are identical, and in the plural end in -a.\n"
                    f"- The vocative of masculine nouns ending in -us ends in -e (serve). Nouns in -ius end in -ī (fīlī).\n\n"
                )
                self.wfile.write(declension_text.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
                with open("templates/second_declension.html", "r", encoding="utf-8") as f:
                    html_template = f.read()
                
                html_response = html_template.replace("{{port}}", str(PORT))
                self.wfile.write(html_response.encode('utf-8'))
            return

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
