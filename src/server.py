#!/usr/bin/env python3
from cgitb import html
import cgitb
from distutils.file_util import write_file
from http import client
import socket
import socketserver
from sqlite3 import connect
from urllib import request, response
import requests
import json

"""
Written by: Raymon Skjørten Hansen
Email: raymon.s.hansen@uit.no
Course: INF-2300 - Networking
UiT - The Arctic University of Norway
May 9th, 2019
"""


def post(self):
    self.wfile.write(b"HTTP/1.1 201") 
    print("POST works")
    self.send_response(200)

    self.data = {
        "text": ""
    }

    rLines = self.rfile.read(int(350))
    print(rLines)
    return "rLines"


def get(self):
    self.payload = '''''
    HTTP/1.1 200 OK
    Host: localhost:8080
    Content-Type: text/html
    Content-Lengt: 4000


    '''''

    print("GET works")
    file = open("index.html", "rb")
    self.wfile.write(b"self.payload" + file.read())


def delete(self):
    print("DELETE works")
    pass


def put(self):
    print("PUT works")
    pass

def getRequest(self):
    pass




class MyTCPHandler(socketserver.StreamRequestHandler):  


    def handle(self):
        """
        This method is responsible for handling an http-request. You can, and should(!),
        make additional methods to organize the flow with which a request is handled by
        this method. But it all starts here!
        """


        self.wfile.write(b"HTTP/1.1 200") 
        # Seperate name of method and jump to HTTP method functions based upon request
        rLine = self.rfile.readline()
        eleReq = rLine.split(b" ")
        firstWord = eleReq[0]

        if firstWord == b"GET":
            get(self) 
        elif firstWord == b"PUT":
            put(self)
        elif firstWord == b"POST":
            post(self)
        elif firstWord == b"DELETE":
            delete(self)

    
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Serving at: http://{}:{}".format(HOST, PORT))
        server.serve_forever()




"""
This class is responsible for handling a request. The whole class is
handed over as a parameter to the server instance so that it is capable
of processing request. The server will use the handle-method to do this.
It is instantiated once for each request!
Since it inherits from the StreamRequestHandler class, it has two very
usefull attributes you can use:

rfile - This is the whole content of the request, displayed as a python
file-like object. This means we can do readline(), readlines() on it!

wfile - This is a file-like object which represents the response. We can
write to it with write(). When we do wfile.close(), the response is
automatically sent.

The class has three important methods:
handle() - is called to handle each request.
setup() - Does nothing by default, but can be used to do any initial
tasks before handling a request. Is automatically called before handle().
finish() - Does nothing by default, but is called after handle() to do any
necessary clean up after a request is handled.
"""

