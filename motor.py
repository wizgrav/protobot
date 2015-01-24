import time
import pigpio

class Motor:
    
  pins = [ {"pwm":6, "dir":26, "init":False},  {"pwm":19, "dir":13, "init":False},  {"pwm":21, "dir":20, "init":True},  {"pwm":16, "dir":12, "init":True} ]

  def __init__(self):
    self.pi=pi
    vmax=200
    pi.clear_bank_1(0xffffffff)
    st=0
    for i in range(0,4):
      self.pins[i]["v"]=0
      self.pins[i]["d"]=True
      if self.pins[i]["init"]:
        st = st | 1<<self.pins[i]["dir"]
      if st: self.pi.set_bank_1(st)
      self.conv(0,i)
  
  def __del__(self):
    for i in range(0,4): self.conv(0,i)
    pi.clear_bank_1(0xffffffff)
  
  def conv(self,v,i):
    v = int(v*self.vmax)
    if v>self.vmax: v=self.vmax
    if v<-self.vmax: v=-self.vmax
    pv=self.pins[i]["v"]
    r=[0,0]
    if (pv < 0 and v >= 0) or ( pv >= 0 and v < 0):
      dd=self.pins[i]["d"]
      r[0 if dd == self.pins[i]["init"] else 1] = 1<<self.pins[i]["dir"]
      self.pins[i]["d"] = !dd
    if pv != v and pv != -v:
      pi.set_PWM_dutycycle(self.pins[i]["pwm"] ,abs(v))
      self.pins[i]["v"] = v
    return r
    
  def update(*m):
    l=len(m)
    if l==3:
      a=[0,0,1,1]
    elif l==5:
      a=[0,1,2,3]
    else:
      a=[0,1,2,3]
      m=[0,0,0,0,0]
    if a:
      cl = 0
      st = 0
      for i in range(0,4):
        r = self.con(m[a[i]+1],i)
        cl = cl | r[0]
        st = st | r[1]
      if cl: self.pi.clear_bank_1(cl)
      if st: self.pi.set_bank_1(st)
    time.delay(50)