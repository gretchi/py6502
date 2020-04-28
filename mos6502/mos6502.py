


class MOS6502MPU(object):
    def __init__(self):
        # Init registers
        self._A  = 0x00
        self._X  = 0x00
        self._Y  = 0x00
        self._S  = 0x00
        self._P  = 0x00
        self._PC = 0x0000


    def reset(self):
        # Init registers
        self.A  = 0x00
        self.X  = 0x00
        self.Y  = 0x00
        self.S  = 0x00
        self.P  = 0x00
        self.PC = 0x0000


    def step(self):
        pass


    def run(self):
        pass


    def _decode(self):
        pass




    def _set_flag_register_from_acc(self, value):
        c = int(value > 0xFF)
        z = value & 0xFF
        n = value & 0x80
        self._set_flag_register(n, 0, 0, 0, 0, 0, z, c)



    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, value):
        self._A = value & 0xFF

    @property
    def X(self):
        return self._X

    @X.setter
    def X(self, value):
        self._X = value & 0xFF

    @property
    def Y(self):
        return self._Y

    @Y.setter
    def Y(self, value):
        self._Y = value & 0xFF

    @property
    def S(self):
        return self._S

    @S.setter
    def S(self, value):
        self._S = value & 0xFF

    @property
    def P(self):
        return self._P

    @P.setter
    def P(self, value):
        self._P = value & 0xFF

    def _set_flag_register(self, n=0, v=0, r=0, b=0, d=0, i=0, z=0, c=0):
        p_buf = 0x00
        p_buf += int(bool(n)) << 7
        p_buf += int(bool(v)) << 6
        p_buf += int(bool(r)) << 5
        p_buf += int(bool(b)) << 4
        p_buf += int(bool(d)) << 3
        p_buf += int(bool(i)) << 2
        p_buf += int(bool(z)) << 1
        p_buf += int(bool(c)) << 0
        self._P = p_buf

    @property
    def PC(self):
        return self._PC

    @PC.setter
    def PC(self, value):
        self._PC = value & 0xFFFF
