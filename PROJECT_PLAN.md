# Terminal Web Page Project Plan

We will build a simple Python web server that responds differently based on the client making the request. If the request comes from a terminal tool like `curl`, it will return beautifully formatted terminal-friendly text featuring ASCII art and a Latin proverb of the day. If it comes from a web browser, it will return a standard HTML page demonstrating the same content.

## Proposed Architecture
- **Language**: Python 3.14 (No external dependencies needed, keeping it lightweight).
- **Server**: We will use Python's built-in `http.server` module.
- **Core Logic**: The server will inspect the `User-Agent` header of incoming GET requests to determine whether the client is a terminal or browser.

## Component Breakdown

### 1. The Server (`server.py`)
- We will create a standalone script `server.py`.
- It will define a custom request handler by subclassing `http.server.BaseHTTPRequestHandler`.
- It will compute a "proverb of the day" based on the current day of the year.

### 2. Terminal Response
- **Trigger**: The User-Agent contains `curl`, `wget`, or `httpie`.
- **Action**: Respond with `Content-type: text/plain; charset=utf-8`.
- **Content**: Send a string using ANSI escape sequences (e.g., `\033[1;32m`).
- **Features**: A large ASCII text banner and a smartly formatted Latin proverb with its English translation.

### 3. Browser Response
- **Trigger**: Any other User-Agent (typically web browsers).
- **Action**: Respond with `Content-type: text/html; charset=utf-8`.
- **Content**: Send basic HTML that displays the ASCII banner and the proverb, styled with CSS to reflect a terminal-like environment visually.

## Verification Plan

### Manual Verification
1. **Terminal Test**: Run `curl localhost:8000` from the terminal and verify that raw text with ANSI formatting is returned, displaying the ASCII art and the proverb appropriately.
2. **Browser Test**: Open `http://localhost:8000` in a web browser and verify standard HTML rendering.
