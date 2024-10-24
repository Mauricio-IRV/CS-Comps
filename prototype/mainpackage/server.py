import http.server
import socketserver

from networking import *

class Server:
    def __init__(self):
        self.http_daemon = None
        self.is_ready_bool = False

    def start(self):
        port = 8000
        ip_address = get_ip_address()
        
        # Use the SimpleHTTPRequestHandler to handle HTTP requests
        Handler = http.server.SimpleHTTPRequestHandler

        # Create a TCP server with the specified port and handler
        self.http_daemon = socketserver.TCPServer(("", port), Handler)
        
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