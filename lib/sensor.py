import pigpio


class Sensor:
    
    ax=0
    ay=0
    az=0
    
    mx=0
    my=0
    mz=0

    def __init__(self, pi):
        self.pi = pi
        self.acc = self.pi.i2c_open(1, 0x19, 0)
        self.pi.i2c_write_byte_data(self.acc,0x20,0x37)
        self.mag = self.pi.i2c_open(1, 0x1e, 0)
        self.pi.i2c_write_byte_data(self.mag,0x00,0x14)
        self.pi.i2c_write_byte_data(self.mag,0x01,0x20)
        self.pi.i2c_write_byte_data(self.mag,0x02,0x01)
        
    def update(self):
        self.ax = self.read(self.acc,0x29)
        self.ay = self.read(self.acc,0x2B)
        self.az = self.read(self.acc,0x2D) 
        self.mx = self.read(self.mag,0x03)
        self.my = self.read(self.mag,0x05)
        self.mz = self.read(self.mag,0x07)
    def debug(self):
        print (self.ax,self.ay,self.az,"***",self.mx,self.my,self.mz)
    def read(self, dev,addr):
        return self.pi.i2c_read_byte_data(dev, addr)


if __name__ == "__main__":
    import time
    pi = pigpio.pi()
    s = Sensor(pi)
    while True:
        s.update()
        s.debug()
        time.sleep(0.5)
