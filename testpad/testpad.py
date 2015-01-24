from server import ProtoServer
from motor import Motor
import pigpio


pi = pigpio.pi()
m = Motor(pi)

def motorfn(data):
    d = s.data["motor"]
    if d:
        m.set(-float(d[0]),-float(d[1]))
        
s=ProtoServer(("192.168.1.253", 6661),"gamepad.html",{"motor":motorfn})


try:
    while True:
        s.update()
except:
    m.set(0,0)
