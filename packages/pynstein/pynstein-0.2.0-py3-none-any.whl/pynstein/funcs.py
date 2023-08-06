import numpy as np
import astropy.units as u
from astropy.units import cds
import astropy.constants as const


def gam(v):
    '''
    gam(velocity)

    Returns the gamma factor for a given input velocity.
    '''
    try:
        magv = np.sqrt(sum(i**2 for i in v))
    except(TypeError):
        magv = v

    try:
        gam = 1 / np.sqrt(1 - magv ** 2 / const.c ** 2)
        return gam
    except(u.UnitsError):
        print('ERROR: Input must have units of velocity.')


def lor(A, v):
    units = A[0].unit
    b0 = v / const.c
    g0 = gam(v)
    Ap0 = g0 * (A[0].to(units) - b0 * A[1].to(units)).value
    Ap1 = g0 * (A[1].to(units) - b0 * A[0].to(units)).value
    Ap2 = A[2].to(units).value
    Ap3 = A[3].to(units).value
    return [Ap0, Ap1, Ap2, Ap3] * units


def inlor(A, v):
    units = A[0].unit
    b0 = v / const.c
    g0 = gam(v)
    Ap0 = g0 * (A[0].to(units) + b0 * A[1].to(units)).value
    Ap1 = g0 * (A[1].to(units) + b0 * A[0].to(units)).value
    Ap2 = A[2].to(units).value
    Ap3 = A[3].to(units).value
    return [Ap0, Ap1, Ap2, Ap3] * units


def tmag(U):
    mag = (0 * U.unit) ** 2
    if np.size(U) == 1:
        return U
    elif np.size(U) <= 3:
        for i in U:
            mag += i ** 2
        return np.sqrt(mag)
    else:
        print("Must be a 3-vector")
        return


def fmag(U):
    return np.sqrt(np.abs(U[0] ** 2 - U[1] ** 2 - U[2] ** 2 - U[3] ** 2))
