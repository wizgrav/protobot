import pigpio


class Motor:

    pins = [{'pwm': 6, 'dir': 26, 'init': True}, {'pwm': 19, 'dir': 13,
            'init': True}, {'pwm': 21, 'dir': 20, 'init': False},
            {'pwm': 16, 'dir': 12, 'init': False}]

    def __init__(self, pi):
        self.pi = pi
        self.vmax = 240.0
        self.vmin = 80.0
        try:
            self.pi.clear_bank_1(0xffffffff)
        except:
            pass
        st = 0
        for i in range(0, 4):
            self.pins[i]['v'] = 0
            self.pins[i]['d'] = True
            self.pi.set_mode(self.pins[i]['pwm'], pigpio.OUTPUT)
            self.pi.set_mode(self.pins[i]['dir'], pigpio.OUTPUT)
            if self.pins[i]['init']:
                st = st | 1 << self.pins[i]['dir']
            if st:
                self.pi.set_bank_1(st)
            self.con(0, i)
        try:
            self.pi.clear_bank_1(0xffffffff)
        except:
            pass

    def __del__(self):
        for i in range(0, 4):
            self.pi.set_PWM_dutycycle(self.pins[i]['pwm'], 0)
        try:
            self.pi.clear_bank_1(0xffffffff)
        except:
            pass

    def con(self, v, i):
        if v != 0:
            v = ((1 if v > 0 else -1)) * int(self.vmin + abs(v)
                    * (self.vmax - self.vmin))
        if v > self.vmax:
            v = self.vmax
        if v < -self.vmax:
            v = -self.vmax
        pv = self.pins[i]['v']
        r = [0, 0]
        r[(0 if v < 0 else 1)] = 1 << self.pins[i]['dir']
        if self.pins[i]['init']:
            t = r[1]
            r[1] = r[0]
            r[0] = t
        if pv != v and pv != -v:
            self.pi.set_PWM_dutycycle(self.pins[i]['pwm'], abs(v))
            self.pins[i]['v'] = v
        return r

    def set(*m):
        l = len(m)
        if l == 3:
            a = [0, 1, 0, 1]
        elif l == 5:
            a = [0, 1, 2, 3]
        else:
            a = [0, 1, 2, 3]
            m = [0, 0, 0, 0, 0]
        if a:
            cl = 0
            st = 0
            for i in range(0, 4):
                r = m[0].con(m[a[i] + 1], i)
                cl = cl | r[0]
                st = st | r[1]
            if cl:
                m[0].pi.clear_bank_1(cl)
            if st:
                m[0].pi.set_bank_1(st)


if __name__ == '__main__':

    import time

    import pigpio

    import motor

    pi = pigpio.pi()
    m = Motor(pi)


			
