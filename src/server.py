#!/usr/bin/env python3
from cgitb import html
from http import client
import socket
import socketserver
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

class MyTCPHandler(socketserver.StreamRequestHandler):
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

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.bind((HOST, PORT))    
    s.listen(10)

    def getRequest(self):

        # Dictionary for HTTP methods
        httpMethod = {
            "GET": self.get,
            "PUT": self.put,
            "POST": self.post,
            "DELETE": self.delete
        }



    def handle(self):
        """
        This method is responsible for handling an http-request. You can, and should(!),
        make additional methods to organize the flow with which a request is handled by
        this method. But it all starts here!
        """

        rLine = self.rfile.readline()
        eleReq = rLine.split(b" ")
        firstWord = eleReq[0]
        #print(firstWord)

        if firstWord == b"GET":
            print("GET") 
        elif firstWord == b"PUT":
            print("PUT")
        elif firstWord == b"POST":
            print("POST") 
        elif firstWord == b"DELETE":
            print("DELETE")

        for line in rLine:
            if line == b"\r\n":
                self.getRequest.httpMethod()
                break

        self.wfile.write(b"HTTP/1.1 200") 

        '''''
        while True:
            client_connection, client_address = s.accept()


            request = client_connection.recv(1024).decode()
            print(request)

            fin = open('index.html')
            content = fin.read()
            fin.close()

            response = 'HTTP/1.0 200 OK\n\n' + content
            client_connection.sendall(response.encode())
            client_connection.close()


            s.close()   
        '''''


    def post(self):
        pass


    def get(self):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        h = open("index.html", "rb")
        self.wfile.write(h.read())


    def delete(self):
        pass


    def put(self):
        pass
    
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Serving at: http://{}:{}".format(HOST, PORT))
        server.serve_forever()

