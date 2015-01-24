import SocketServer

class ProtoHandler(SocketServer.BaseRequestHandler):
    
    def handle(self):
        msg = self.request.recv(1024)
        a = msg.split(" ",2)
        if len(a) >1  and a[0] == "GET":
            a = a[1].split("/")
            a =[i for i in a if i != '']
            if len(a) == 0:
                self.request.sendall(self.server.ret)
            else:
                self.server.data=a
                print a
        
            
class ProtoServer(SocketServer.TCPServer):
    def __init__(self,hostport,default):
        self.allow_reuse_address = True
        SocketServer.TCPServer.__init__(self,hostport, ProtoHandler)
        with open (default, "r") as myfile:
            self.ret=myfile.read()
    
            

if __name__ == "__main__":
    s = ProtoServer(("192.168.1.253", 6661),"index.html")
    s.serve_forever()
