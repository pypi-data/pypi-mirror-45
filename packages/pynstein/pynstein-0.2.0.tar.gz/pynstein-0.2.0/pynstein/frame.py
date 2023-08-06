import numpy as np
import astropy.units as u
from astropy.units import cds
import astropy.constants as const
import pynstein.funcs as f


class frame:
    def __init__(self, name=None, vf=None):
        if name is None:
            self.name = "Home"
        else:
            self.name = name
        if vf is None:
            self.u = 0 * u.m / u.s
            self.g = 1
        else:
            self.u = f.tmag(vf)
            self.g = f.gam(vf)
