import numpy as np
import astropy.units as u
from astropy.units import cds
import astropy.constants as const
import pynstein.funcs as f
import pynstein.frame as fr
import pynstein.fvec


class fvel(pynstein.fvec):
    def __init__(self, v, wrt=fr.frame()):
        if np.size(v) <= 3:
            self.unit = v[0].unit
            while np.size(v) < 3:
                v = np.append(v.to(self.unit).value, 0) * self.unit
            self.gamma = f.gam(v)
            self.frame = wrt
            self.zero = (self.gamma * const.c).to(self.unit)
            self.one = (self.gamma * v[0]).to(self.unit)
            self.two = (self.gamma * v[1]).to(self.unit)
            self.three = (self.gamma * v[2]).to(self.unit)
            self.vec = [self.zero.value, self.one.value,
                        self.two.value, self.three.value] * self.unit
            self.mag = f.fmag(self.vec)
        elif np.size(v) == 4:
            self.gamma = f.gam(v[1:4])
            self.unit = v[0].unit
            self.frame = wrt
            self.zero = (v[0]).to(self.unit)
            self.one = (v[1]).to(self.unit)
            self.two = (v[2]).to(self.unit)
            self.three = (v[3]).to(self.unit)
            self.vec = [self.zero.value, self.one.value,
                        self.two.value, self.three.value] * self.unit
            self.mag = f.fmag(self.vec)
        else:
            print("Must have 4 or fewer components")

    #def __add__(self, other):
    #    if self.frame == other.frame:
    #
    #        g0 = f.gam(other.v)
    #        deno = (1 - other.v / const.c ** 2 * self.x).decompose()
    #        vxp = ((self.x - other.v) / deno).to(self.u)
    #        vyp = ((self.y / g0) / deno).to(self.u)
    #        vzp = ((self.z / g0) / deno).to(self.u)
    #        new = [vxp, vyp, vzp]
    #        print(new)
    #        return self.__class__(new, wrt=self.frame)
    #    else:
    #        print("Velocities in different frames. Feature Coming Soon!")
