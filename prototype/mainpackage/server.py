import re
import requests
import socketserver
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer

from networking import *

class ProxyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, World!") 

        # # Remove headers that should not be forwarded
        # self.headers.pop("If-Modified-Since", None)
        # self.headers.pop("Cache-Control", None)
        # self.headers.pop("Upgrade-Insecure-Requests", None)

        # # Determine if the request is to a secure host
        # if self.path.startswith("https://"):
        #     # Strip the "https://" and replace with "http://"
        #     self.path = self.path.replace("https://", "http://", 1)

        # # Forward the request to the target server
        # response = requests.get(self.path, headers=dict(self.headers))

        # # Modify the response
        # self.send_response(response.status_code)
        # for header, value in response.headers.items():
        #     if header.lower() not in ["strict-transport-security", "public-key-pins"]:
        #         self.send_header(header, value)
        # self.end_headers()

        # # Strip links in response body
        # content = response.content.replace(b"https://", b"http://")

        # # Write the modified content back to the client
        # self.wfile.write(content)

    def do_POST(self):
        # Handle post requests
        pass

class Server:
    def __init__(self):
        self.http_daemon = None
        self.is_ready_bool = False

    def start(self, port: int):
        ip_address = get_ip_address()

        # Create a TCP server with the specified port, whilst using...
        # self.http_daemon = socketserver.TCPServer(("", port), ProxyHTTPRequestHandler)
        # self.http_daemon = HTTPServer(("", port), ProxyHTTPRequestHandler)
        # self.http_daemon = socketserver.TCPServer(("", port), SimpleHTTPRequestHandler)
        self.http_daemon = socketserver.TCPServer(("", port), ProxyHTTPRequestHandler)
        
        # Print serving ip address / port & update server status
        print("Serving at", ip_address + ":" + str(port) + "\n")
        self.is_ready_bool = True

        self.http_daemon.serve_forever() # Set server to handle requests indefinitely
    
    def is_ready(self):
        return self.is_ready_bool

    def stop(self):
        if self.http_daemon is not None:
            # Shut down server
            self.http_daemon.shutdown()
            self.http_daemon.server_close()
            
            # Cleanup variables
            self.http_daemon = None
            self.is_ready_bool = False

            print("Server closed...")
