from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer
import requests
import socketserver

from networking import *
from modules import *
from scapy.layers.http import *

from http.server import SimpleHTTPRequestHandler
import requests

class ProxyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):

        super().do_GET()
        '''
        # Forward the request to the target server
        resp = requests.get("http://danger.jeffondich.com/")
        b_content = None

        # Modify HTTP(S) Headers / Response
        try: b_content = resp.content.replace(b"https://", b"http://")
        except: pass

        try: resp.headers.pop("Strict-Transport-Security", None)
        except: pass

        try: resp.headers.pop("Transfer-Encoding", None)
        except: pass

        try: resp.headers.pop("Content-Encoding", None)
        except: pass

        # Send modified response
        self.send_response(200)
        for header, value in resp.headers.items():
            self.send_header(header, value)
            print(f"Sent: {header}: {value}")
        self.end_headers()
        self.wfile.write(b_content)
        '''

class Server:
    def __init__(self):
        self.http_daemon = None
        self.is_ready_bool = False

    def start(self, port: int):
        ip_address = get_ip_address()

        # Create a TCP server with the specified port, whilst using...
        self.http_daemon = HTTPServer(("", port), ProxyHTTPRequestHandler)
        
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
