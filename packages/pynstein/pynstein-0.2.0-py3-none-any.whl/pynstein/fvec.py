import numpy as np
import astropy.units as u
from astropy.units import cds
import astropy.constants as const
import pynstein.funcs as f
import pynstein.frame as fr


class fvec:
    def __init__(self, v, wrt=fr.frame()):
        self.unit = v[0].unit
        self.zero = v[0].to(self.unit)
        self.one = v[1].to(self.unit)
        self.two = v[2].to(self.unit)
        self.three = v[3].to(self.unit)
        self.vec = [self.zero.value, self.one.value,
                    self.two.value, self.three.value] * self.unit

    def to(self, wrt):
        g0 = f.gam(wrt.u)
        deno = (1 - wrt.u / const.c ** 2 * self.frame.u).decompose()
        vrel = ((self.frame.u - wrt.u) / deno).decompose()
        return self.__class__(f.lor(self.vec, vrel), wrt=wrt)

    def _repr_latex_(self):
        return self.vec._repr_latex_()

    def __repr__(self):
        return self.vec.__repr__()

    def __str__(self):
        return self.vec.__str__()
