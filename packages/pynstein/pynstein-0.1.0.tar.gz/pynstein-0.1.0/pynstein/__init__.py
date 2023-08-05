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


def fvel(V):
    '''
    fvel(3-velocity)

    Returns a 4-velocity.
    '''
    units = V[0].unit
    g0 = gam(V)
    c = const.c.to(units).value
    v4 = g0 * [c, V[0].value, V[1].value, V[2].value] * units
    if fmag(v4) == const.c:
        return v4
    else:
        print('Magnitude of 4-velocity is not c.' +
              ' Make sure input is a 3-velocity.')


def tvel(V):
    '''
    fvel(4-velocity)

    Returns a 3-velocity.
    '''
    units = V[0].unit
    g0 = (V[0] / const.c).decompose()
    v3 = [(V[1] / g0).value, (V[2] / g0).value, (V[3] / g0).value] * units
    if tmag(v3) <= const.c:
        return v3
    else:
        print("Velocity greater than c. Something's fishy.")


def vadd(V, v):
    units = V[0].unit
    g0 = gam(v)
    deno = (1 - v / const.c ** 2 * V[0]).decompose()
    vxp = ((V[0] - v) / deno).to(units)
    vyp = ((V[1] / g0) / deno).to(units)
    vzp = ((V[2] / g0) / deno).to(units)
    return [vxp, vyp, vzp]


def invadd(V, v):
    units = V[0].unit
    g0 = gam(v)
    deno = (1 + v / const.c ** 2 * V[0]).decompose()
    vxp = ((V[0] + v) / deno).to(units)
    vyp = ((V[1] / g0) / deno).to(units)
    vzp = ((V[2] / g0) / deno).to(units)
    return [vxp, vyp, vzp]


def tmag(U):
    return np.sqrt(np.abs(U[0] ** 2 + U[1] ** 2 + U[2] ** 2))


def fmag(U):
    return np.sqrt(np.abs(U[0] ** 2 - U[1] ** 2 - U[2] ** 2 - U[3] ** 2))
