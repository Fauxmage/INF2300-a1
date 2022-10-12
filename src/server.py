#!/usr/bin/env python3
import os
import sys
import json
import socketserver


"""
Written by: Raymon Skjørten Hansen
Email: raymon.s.hansen@uit.no
Course: INF-2300 - Networking
UiT - The Arctic University of Norway
May 9th, 2019
"""

class MyTCPHandler(socketserver.StreamRequestHandler):
 
    def do_GET(self):

        if(self.reqSplit[1] == "/index.html" or self.reqSplit[1] == "/" ):
            file = open("index.html")

            # Convert into string
            fString = file.read()
            status_line = "HTTP/1.1 200 - OK\n"
            content_type = "Content-Type: text/html\n"
            content_lenght = "Content-Lenght: {} \n\n".format(len(fString))
            retMsg = (status_line + content_type + content_lenght + fString)
            self.request.sendall(retMsg.encode("utf-8"))
    
    def do_PUT(self):

        # Get .txt data
        self.data_split_text = self.reqData.split("text=")[1] 
        with open("test.txt", "a") as file:
            file.write(self.data_split_text + "\n")
            
        with open("test.txt") as file:
            sfile_string = file.read()

        status_line = "HTTP/1.1 200 - OK\n"
        content_type = "Content-Type: text/html\n"
        content_lenght = "Content-Lenght: {} \n\n".format(len(sfile_string))
          
        retMsg = (status_line + content_type + content_lenght + sfile_string)
        self.request.sendall(retMsg.encode("utf-8")) 
       
            
    def api_GET(self):

        # Convert to dict
        with open("messages.json", "r") as file:
            data = json.load(file)

        # Response
        res = str(data["messages"]) 
       
        status_line = "HTTP/1.1 200 - OK\n"
        content_type = "Content-Type: text/html\n"
        content_lenght = "Content-Lenght: {} \n\n".format(len(res))
        retMsg = (status_line + content_type + content_lenght + res)
      
        self.request.sendall(retMsg.encode("utf-8"))
      
    
    def apiPOST(self):

        with open("messages.json", "r") as file:
            data = json.load(file)

        # Get last object from messages 
        objVar = data["messages"][-1]['id']    
      
        #New message ID
        newID = objVar + 1
        req_beg = self.reqData.find('{')
        req_end = self.reqData.find('}', req_beg)
        self.secString = self.reqData[req_beg:req_end + 1]
        ret = json.loads(self.secString)
        newText = ret["text"]
        
        # New object 
        newText.update( {'id' : newID} )
        data["messages"].append(ret)
        with open("messages.json", "w") as file:
            json.dump(data, file, indent = 1)

        # Response
        res = str(ret) 
       
        status_line = "HTTP/1.1 200 - OK\n"
        content_type = "Content-Type: application/json\n"
        content_lenght = "Content-Lenght: {} \n\n".format(len(res))
        retMsg = (status_line + content_type + content_lenght + res)
      
        self.request.sendall(retMsg.encode("utf-8"))
    

    def setup(self):
        socketserver.StreamRequestHandler.setup(self)
                 

    def handle(self):
        self.wfile.write(b"HTTP/1.1 200")

        # Formatting for getting HTTP request
        self.reqData = self.request.recv(1024).strip().decode("utf-8")
        self.reqSplit = self.reqData.split(" ")
        if(self.reqSplit[0] == "GET" and self.reqSplit[1] != "/messages" ):
            self.do_GET()
        if(self.reqSplit[0] == "GET" and self.reqSplit[1] == "/messages" ):
            self.api_GET()   
        if(self.reqSplit[0] == "POST" and self.reqSplit[1] == "/test.txt" ):
            self.do_PUT()
        if(self.reqSplit[0] == "POST" and self.reqSplit[1] == "/messages" ):
            self.apiPOST()    

        self.wfile.close()

    
    def finish(self):
        socketserver.StreamRequestHandler.finish(self)
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

        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Serving at: http://{}:{}".format(HOST, PORT))
        server.serve_forever()

