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

def render(t) -> str:
    """Custom template handler for PEP 750 templates."""
    return "".join(str(s) + format(v.value, v.format_spec or "") for s, v in zip(t.strings, t.interpolations)) + str(t.strings[-1])

ASCII_ART = render(t"""{Colors.OKCYAN}{Colors.BOLD}
  _____                   _             _ 
 |_   _|___ _ __ _ __ ___(_)_ __   __ _| |
   | |/ _ \\ '__| '_ ` _ \\| | '_ \\ / _` | |
   | |  __/ |  | | | | | | | | | | (_| | |
   |_|\\___|_|  |_| |_| |_|_|_| |_|\\__,_|_|
{Colors.ENDC}""")

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
                
                declension_text = render(t"""{Colors.OKCYAN}{Colors.BOLD}First Latin Declension (-a, -ae){Colors.ENDC}

{Colors.OKGREEN}Singular:{Colors.ENDC}
  Nom: -a     (terr-a)
  Gen: -ae    (terr-ae)
  Dat: -ae    (terr-ae)
  Acc: -am    (terr-am)
  Abl: -ā     (terr-ā)
  Voc: -a     (terr-a)

{Colors.OKGREEN}Plural:{Colors.ENDC}
  Nom: -ae    (terr-ae)
  Gen: -ārum  (terr-ārum)
  Dat: -īs    (terr-īs)
  Acc: -ās    (terr-ās)
  Abl: -īs    (terr-īs)
  Voc: -ae    (terr-ae)

{Colors.BOLD}Rules:{Colors.ENDC}
- Mostly feminine nouns (e.g., puella, insula).
- Exceptions include some masculine nouns denoting occupations (e.g., nauta, agricola, poēta).

""")
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
                
                declension_text = render(t"""{Colors.OKCYAN}{Colors.BOLD}Second Latin Declension (-us, -i / -um, -i){Colors.ENDC}

{Colors.BOLD}Masculine (-us){Colors.ENDC}
{Colors.OKGREEN}Singular:{Colors.ENDC}
  Nom: -us    (serv-us)
  Gen: -ī     (serv-ī)
  Dat: -ō     (serv-ō)
  Acc: -um    (serv-um)
  Abl: -ō     (serv-ō)
  Voc: -e     (serv-e)

{Colors.OKGREEN}Plural:{Colors.ENDC}
  Nom: -ī     (serv-ī)
  Gen: -ōrum  (serv-ōrum)
  Dat: -īs    (serv-īs)
  Acc: -ōs    (serv-ōs)
  Abl: -īs    (serv-īs)
  Voc: -ī     (serv-ī)

{Colors.BOLD}Neuter (-um){Colors.ENDC}
{Colors.OKGREEN}Singular:{Colors.ENDC}
  Nom: -um    (bell-um)
  Gen: -ī     (bell-ī)
  Dat: -ō     (bell-ō)
  Acc: -um    (bell-um)
  Abl: -ō     (bell-ō)
  Voc: -um    (bell-um)

{Colors.OKGREEN}Plural:{Colors.ENDC}
  Nom: -a     (bell-a)
  Gen: -ōrum  (bell-ōrum)
  Dat: -īs    (bell-īs)
  Acc: -a     (bell-a)
  Abl: -īs    (bell-īs)
  Voc: -a     (bell-a)

{Colors.BOLD}Rules:{Colors.ENDC}
- Includes mostly masculine (-us, -er, -ir) and neuter (-um) nouns.
- Neuter Rule: Nominative, accusative, and vocative are identical, and in the plural end in -a.
- The vocative of masculine nouns ending in -us ends in -e (serve). Nouns in -ius end in -ī (fīlī).

""")
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

        elif self.path == '/third-declension':
            if is_terminal:
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                
                declension_text = render(t"""{Colors.OKCYAN}{Colors.BOLD}Third Latin Declension (-is){Colors.ENDC}

{Colors.BOLD}Masculine / Feminine{Colors.ENDC}
{Colors.OKGREEN}Singular:{Colors.ENDC}
  Nom: —      (rēx)
  Gen: -is    (rēg-is)
  Dat: -ī     (rēg-ī)
  Acc: -em    (rēg-em)
  Abl: -e     (rēg-e)
  Voc: —      (rēx)

{Colors.OKGREEN}Plural:{Colors.ENDC}
  Nom: -ēs    (rēg-ēs)
  Gen: -um    (rēg-um)
  Dat: -ibus  (rēg-ibus)
  Acc: -ēs    (rēg-ēs)
  Abl: -ibus  (rēg-ibus)
  Voc: -ēs    (rēg-ēs)

{Colors.BOLD}Neuter{Colors.ENDC}
{Colors.OKGREEN}Singular:{Colors.ENDC}
  Nom: —      (flūmen)
  Gen: -is    (flūmin-is)
  Dat: -ī     (flūmin-ī)
  Acc: —      (flūmen)
  Abl: -e     (flūmin-e)
  Voc: —      (flūmen)

{Colors.OKGREEN}Plural:{Colors.ENDC}
  Nom: -a     (flūmin-a)
  Gen: -um    (flūmin-um)
  Dat: -ibus  (flūmin-ibus)
  Acc: -a     (flūmin-a)
  Abl: -ibus  (flūmin-ibus)
  Voc: -a     (flūmin-a)

{Colors.BOLD}Rules:{Colors.ENDC}
- Contains masculine, feminine, and neuter nouns. The genitive singular always ends in -is.
- The nominative singular has variable endings.
- Neuter Rule: Nominative, accusative, and vocative cases are identical, and in the plural they end in -a.
- "I-stem" nouns (e.g., urbs, mare) have slightly different endings (e.g., genitive plural -ium).

""")
                self.wfile.write(declension_text.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
                with open("templates/third_declension.html", "r", encoding="utf-8") as f:
                    html_template = f.read()
                
                html_response = html_template.replace("{{port}}", str(PORT))
                self.wfile.write(html_response.encode('utf-8'))
            return

        elif self.path == '/fourth-declension':
            if is_terminal:
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                
                declension_text = render(t"""{Colors.OKCYAN}{Colors.BOLD}Fourth Latin Declension (-us, -ūs / -ū, -ūs){Colors.ENDC}

{Colors.BOLD}Masculine (-us){Colors.ENDC}
{Colors.OKGREEN}Singular:{Colors.ENDC}
  Nom: -us    (port-us)
  Gen: -ūs    (port-ūs)
  Dat: -uī    (port-uī)
  Acc: -um    (port-um)
  Abl: -ū     (port-ū)
  Voc: -us    (port-us)

{Colors.OKGREEN}Plural:{Colors.ENDC}
  Nom: -ūs    (port-ūs)
  Gen: -uum   (port-uum)
  Dat: -ibus  (port-ibus)
  Acc: -ūs    (port-ūs)
  Abl: -ibus  (port-ibus)
  Voc: -ūs    (port-ūs)

{Colors.BOLD}Neuter (-ū){Colors.ENDC}
{Colors.OKGREEN}Singular:{Colors.ENDC}
  Nom: -ū     (corn-ū)
  Gen: -ūs    (corn-ūs)
  Dat: -ū     (corn-ū)
  Acc: -ū     (corn-ū)
  Abl: -ū     (corn-ū)
  Voc: -ū     (corn-ū)

{Colors.OKGREEN}Plural:{Colors.ENDC}
  Nom: -ua    (corn-ua)
  Gen: -uum   (corn-uum)
  Dat: -ibus  (corn-ibus)
  Acc: -ua    (corn-ua)
  Abl: -ibus  (corn-ibus)
  Voc: -ua    (corn-ua)

{Colors.BOLD}Rules:{Colors.ENDC}
- Contains mostly masculine nouns ending in -us and a few neuter nouns ending in -ū.
- Some important feminine exceptions end in -us, such as manus (hand) and domus (house).
- Neuter Rule: Nominative, accusative, and vocative cases are identical, and in the plural they end in -a (specifically -ua).
- The genitive singular and nominative/accusative/vocative plural of masculine nouns are identical (-ūs).

""")
                self.wfile.write(declension_text.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
                with open("templates/fourth_declension.html", "r", encoding="utf-8") as f:
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
            
            response = render(t"""{ASCII_ART}
{Colors.OKGREEN}Latin Proverb of the Day:{Colors.ENDC}
{Colors.BOLD}{latin}{Colors.ENDC} - {english}

""")
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
