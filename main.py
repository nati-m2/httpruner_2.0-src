#!/usr/bin/env python
import os
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
count =0
f = open("httpruner config.txt", "r")
sook = f.read()
adr = sook.split(":")
if len(adr)< 3:
    exit(-1)

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        global count
        count = count + 1  # 2.1 צריך לשנות לגירסה הבאה
        self._set_headers()
        self.wfile.write(self._html("hi!"))
        if count > 20:
            exit(0)
        if self.client_address[0] != adr[2]:
            count = count + 1
            print(self.client_address[0])
        print(count)

    def do_HEAD(self):
       self._set_headers()

    def do_POST(self):
        global count
        self._set_headers()
        self.wfile.write(self._html("POST!"))
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        if count > 20:
            exit(0)
        if self.client_address[0]==adr[2]:
            #os.startfile(post_data)              #<------------------- demo
            print(self.client_address[0])         #<------------------- demo
            print(post_data)                      #<------------------- demo
        else:
            #print(post_data)
            count = count + 1

def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        #default="localhost",
        default=adr[0],
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=adr[1],
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
    exit(0)