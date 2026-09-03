"""
Bal Krishna Janmashtami Divine Dot-Art Web Launcher
Opens the ultra-high-fidelity glowing canvas experience in your default web browser.
"""

import os
import sys
import webbrowser
import http.server
import socketserver
import threading

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_PORT = 8080

def get_server(start_port=DEFAULT_PORT):
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *args: None
    socketserver.TCPServer.allow_reuse_address = True
    
    port = start_port
    while port < start_port + 100:
        try:
            httpd = socketserver.TCPServer(("", port), handler)
            return httpd, port
        except OSError:
            port += 1
    raise RuntimeError("Could not find an available port.")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        httpd, port = get_server(DEFAULT_PORT)
    except Exception as e:
        print(f"Error starting server: {e}")
        return

    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    url = f"http://localhost:{port}/index.html"
    print(f"\n🕉️  Bal Krishna Janmashtami Experience is Live at: {url}")
    print("✨ Press Ctrl+C to stop the server anytime.\n")
    webbrowser.open(url)

    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.shutdown()

if __name__ == "__main__":
    main()
