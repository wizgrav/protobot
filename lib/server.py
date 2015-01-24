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
                a[len(a)-1] = a[len(a)-1].split("?")[0]
                key = a[0]
                val = a[1:]
                self.server.data[key]=val
                if key in self.server.handlers:
                    self.server.handlers[key](val)
                else:
                    print("UNHANDLED( "+key+" ) = ", val)
                    
class ProtoServer(SocketServer.TCPServer):
    data = {}
    def __init__(self,hostport,default,handlers={}, timeout=0.05):
        self.handlers = handlers
        self.allow_reuse_address = True
        self.timeout = timeout
        SocketServer.TCPServer.__init__(self,hostport, ProtoHandler)
        with open (default, "r") as myfile:
            self.ret=myfile.read()
    def update(self):
        self.handle_request()
            

if __name__ == "__main__":
    s = ProtoServer(("192.168.1.253", 6661),"index.html")
    s.serve_forever()
