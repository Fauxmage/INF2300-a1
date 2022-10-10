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
 
    def get_request(self):
        
        if(self.data_split[1] == "/index.html" or self.data_split[1] == "/" ):
           
            file = open("index.html")
            # convert the file into string
            file_string = file.read()
            
          

            status_line = "HTTP/1.1 200 - OK\n"
            content_type = "Content-Type: text/html\n"
            content_lenght = "Content-Lenght: {} \n\n".format(len(file_string))
          
            responsee = status_line + content_type + content_lenght + file_string
         
          
            
            self.request.sendall(responsee.encode("utf-8"))

          

        elif(self.data_split[1] == "/server.py"):
            status_line = "HTTP/1.1 403 - Forbidden\n"
            content_type = "Content-Type: text/html\n"
            content_lenght = "Content-Lenght: NA \n\n"
            responsee = status_line + content_type + content_lenght
            self.request.sendall(responsee.encode("utf-8"))
          
            

        else:
            status_line = "HTTP/1.1 404 - Not Found\n"
            content_type = "Content-Type: text/html\n"
            content_lenght = "Content-Lenght: NA \n\n"
            responsee = status_line + content_type + content_lenght
            self.request.sendall(responsee.encode("utf-8"))

    
    def put_request(self):

        """ retrieving the txt input """
        self.data_split_text = self.data.split("text=")[1] 
        with open("test.txt", "a") as f:
            f.write(self.data_split_text + "\n")
            
        with open("test.txt") as f:
            sfile_string = f.read()

      

        status_line = "HTTP/1.1 200 - OK\n"
        content_type = "Content-Type: text/html\n"
        content_lenght = "Content-Lenght: {} \n\n".format(len(sfile_string))
          
        responsee = status_line + content_type + content_lenght + sfile_string
        self.request.sendall(responsee.encode("utf-8")) 
       
            
              

    def get_json_handler(self):

        # converts the json object into a python dictionary

        with open("messages.json", "r") as f:
            data = json.load(f)

        

        y = str(data["messages"]) 
       
        status_line = "HTTP/1.1 200 - OK\n"
        content_type = "Content-Type: text/html\n"
        content_lenght = "Content-Lenght: {} \n\n".format(len(y))
        responsee = status_line + content_type + content_lenght + y
      
        self.request.sendall(responsee.encode("utf-8"))
      
         
         
             
    def call_forbidden(self):

        status_line = "HTTP/1.1 403 - Forbidden\n"
        content_type = "Content-Type: text/html\n"
        content_lenght = "Content-Lenght: NA \n\n"
        responsee = status_line + content_type + content_lenght
        self.request.sendall(responsee.encode("utf-8"))

    
    def post_json_handler(self):

      

        with open("messages.json", "r") as f:
            data = json.load(f)

        #getting the last object from the list data["messages"]
        var = data["messages"][-1]['id']    
      

        #new id
        new_id = var + 1

        start = self.data.find('{')
        end = self.data.find('}', start)
        self.substring = self.data[start:end + 1]
        res = json.loads(self.substring)

        #new text
        new_text = res["text"]
        #new object
        res.update( {'id' : new_id} )

    

        data["messages"].append(res)
        
        with open("messages.json", "w") as f:
            json.dump(data,f, indent=2)

   

        # sending the response
        y = str(res) 
       
        status_line = "HTTP/1.1 200 - OK\n"
        content_type = "Content-Type: application/json\n"
        content_lenght = "Content-Lenght: {} \n\n".format(len(y))
        responsee = status_line + content_type + content_lenght + y
      
        self.request.sendall(responsee.encode("utf-8"))
    
    def setup(self):
        return super().setup()
                 

    def handle(self):
       
        """" data has the request from the client """
        self.data = self.request.recv(1024).strip().decode("utf-8")
      

        self.data_split = self.data.split(" ")
        
        if(self.data_split[0] == "GET" and self.data_split[1] != "/messages" ):
            self.get_request()

        if(self.data_split[0] == "GET" and self.data_split[1] == "/messages" ):
            self.get_json_handler()   

        if(self.data_split[0] == "POST" and self.data_split[1] == "/test.txt" ):
            self.put_request()

        if(self.data_split[0] == "POST" and self.data_split[1] == "/messages" ):
            self.post_json_handler()    

      #  a post request to any other file is not allowed
        if(self.data_split[0] == "POST" and  self.data_split[1] != "/messages" ):
           # self.call_forbidden()
            if(self.data_split[0] == "POST" and self.data_split[1] != "/test.txt" ):    
                self.call_forbidden()
         

        
      
        self.wfile.close()
    
    def finish(self):
        return super().finish()
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
        try:
            print("Serving at: http://{}:{}".format(HOST, PORT))
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
            print("\nShutting down...")

