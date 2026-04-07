import os

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

def html_renderer(template_name: str, **kwargs) -> str:
    """Renders HTML by replacing {{key}} with values from kwargs."""
    path = os.path.join("templates", template_name)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    for k, v in kwargs.items():
        html = html.replace(f"{{{{{k}}}}}", str(v))
    return html

def terminal_renderer(template_name: str, **kwargs) -> str:
    """Renders terminal templates using python str.format."""
    path = os.path.join("templates", template_name)
    with open(path, "r", encoding="utf-8") as f:
        term = f.read()
    
    # Implicit terminal context
    context = {"Colors": Colors, "ASCII_ART": ASCII_ART}
    context.update(kwargs)
    
    return term.format(**context)
