# Dictionary Mapping Routing

This document details the first approach presented in the endpoint refactoring plan: using a functional dictionary-mapping mechanism instead of a massive `if/elif` chain.

## The Problem

Currently, `server.py` defines each route sequentially in the `do_GET` block:

```python
elif self.path == '/first-declension':
    if is_terminal:
        # 4 lines to set headers
        # 2 lines to format and write the terminal version
    else:
        # 4 lines to set headers
        # 2 lines to format and write the HTML version
    return
elif self.path == '/second-declension':
    # Exact same 12 lines of code...
```

For 5 declensions, this creates around 80 lines of highly repetitive code. The only thing changing between these blocks is the string `'first_declension'` to `'second_declension'`.

## The Functional Solution

We can resolve this by treating generic string properties (like template names) as **data** rather than logic. Here is exactly how we implement this.

### 1. The Rendering Helper

We extract the repetitive "are we in terminal or HTML?" logic into a single dedicated helper function. This function takes care of the headers and invoking the appropriate renderer.

```python
def serve_template(handler, template_basename, context=None):
    """
    Universally handles HTTP response formatting for both terminal and web clients.
    """
    if context is None:
        context = {}
        
    if handler.is_terminal:
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
```

### 2. The Routing Dictionary

We define a configuration variable mapping URL paths directly to their corresponding template base names. This completely eliminates the `if/elif` checks.

```python
# Defined at the class or module level
STATIC_ROUTES = {
    '/first-declension': 'first_declension',
    '/second-declension': 'second_declension',
    '/third-declension': 'third_declension',
    '/fourth-declension': 'fourth_declension',
    '/fifth-declension': 'fifth_declension',
}
```

### 3. Integrating into `do_GET`

Finally, `do_GET` handles the routing dynamically. If the incoming path exists in our dictionary, it immediately serves it with the helper function and returns.

```python
class SinglePageHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        user_agent = self.headers.get('User-Agent', '').lower()
        self.is_terminal = any(agent in user_agent for agent in ['curl', 'wget', 'httpie'])
        
        # 1. Check if the path requested matches one of our defined templates
        if self.path in STATIC_ROUTES:
            target_template = STATIC_ROUTES[self.path]
            serve_template(self, target_template, context={"port": PORT})
            return

        # 2. Fallback logic for the base URL ("/")
        latin, english = get_proverb_of_the_day()
        serve_template(self, "base", context={"latin": latin, "english": english, "port": PORT})
```

## Benefits
- **Zero Duplication**: The rendering logic exists strictly in one place.
- **Maintainability**: Adding a "sixth declension" requires modifying a single line (adding it to `STATIC_ROUTES`), rather than 15 lines of nested ifs and else clauses.
- **Testability**: The `serve_template` block can be tested entirely independent of the route parsing.
