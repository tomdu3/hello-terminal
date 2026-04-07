import threading
import time
import urllib.request
import pytest
from server import SinglePageHandler, PORT
import socketserver

# Helper to run the server in a separate thread
def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SinglePageHandler) as httpd:
        httpd.serve_forever()

@pytest.fixture(scope="module", autouse=True)
def server():
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    time.sleep(1)  # Wait for server to start
    yield

def test_root_html():
    url = f"http://localhost:{PORT}/"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        assert "text/html" in response.getheader("Content-Type")
        body = response.read().decode('utf-8')
        assert "Latin Proverb of the Day" in body

def test_root_terminal():
    url = f"http://localhost:{PORT}/"
    req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        assert "text/plain" in response.getheader("Content-Type")
        body = response.read().decode('utf-8')
        assert "Latin Proverb of the Day" in body
        # ANSI color for ASCII art or bold text could be here
        assert "\033[" in body

def test_first_declension_html():
    url = f"http://localhost:{PORT}/first-declension"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        assert "text/html" in response.getheader("Content-Type")
        body = response.read().decode('utf-8')
        assert "First Latin Declension" in body

def test_first_declension_terminal():
    url = f"http://localhost:{PORT}/first-declension"
    req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        assert "text/plain" in response.getheader("Content-Type")
        body = response.read().decode('utf-8')
        assert "First Latin Declension" in body
        assert "\033[" in body

def test_fifth_declension_html():
    url = f"http://localhost:{PORT}/fifth-declension"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        assert "text/html" in response.getheader("Content-Type")
        body = response.read().decode('utf-8')
        assert "Fifth Latin Declension" in body

def test_fifth_declension_terminal():
    url = f"http://localhost:{PORT}/fifth-declension"
    req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        assert "text/plain" in response.getheader("Content-Type")
        body = response.read().decode('utf-8')
        assert "Fifth Latin Declension" in body
        assert "\033[" in body

def test_invalid_path_defaults_to_home():
    url = f"http://localhost:{PORT}/some-invalid-path"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        body = response.read().decode('utf-8')
        assert "Latin Proverb of the Day" in body
