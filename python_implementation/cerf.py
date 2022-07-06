import math
import cmath
import sys
import numpy as np
from numba import njit


@njit
def cerf_jit(z):
    if z == 0:
        res = 1
        return res

    z_orig = z
    z = abs(z.real) + abs(z.imag)*1j

    if abs(z) > 10:
        res = 1j*z*(0.5124242/(z**2-0.2752551) + 0.05176536/(z**2-2.724745))
    elif z.imag < 1 and abs(z) < 4:
        acc = z
        for n in range(1,500):
            last = z**(2*n+1)/(math.gamma(n+1)*(2*n+1))
            acc = acc + last
            # if abs(last) < sys.float_info.epsilon: break
            if abs(last) < 2.22e-16: break

        res = cmath.exp(-z**2)*(1 + 2j*acc/math.sqrt(math.pi))

    else:
        old = 1e6
        h1 = 1
        h2 = 2*z
        u1 = 0
        u2 = 2*math.sqrt(math.pi)
        for n in range(1, 300):
            h3 = h2*z - n*h1
            u3 = u2*z - n*u1
            h1 = h2
            h2 = 2*h3
            u1 = u2
            u2 = 2*u3
            new = u3/h3
            if abs((new-old)/old) < 5e-6: break
            elif not np.isfinite(new):
                new = old
                break
            old = new
        res = 1j*new/math.pi

    if z_orig.real < 0:
        if z_orig.imag >= 0:
            res = np.conj(res)
        else:
            res = 2*cmath.exp(-z**2) - res
    elif z_orig.imag < 0:
        res = np.conj(2*cmath.exp(-z**2) - res)

    return res


def cerf(z):
    if z == 0:
        res = 1
        return res

    z_orig = z
    z = abs(z.real) + abs(z.imag)*1j

    if abs(z) > 10:
        res = 1j*z*(0.5124242/(z**2-0.2752551) + 0.05176536/(z**2-2.724745))
    elif z.imag < 1 and abs(z) < 4:
        acc = z
        for n in range(1,500):
            last = z**(2*n+1)/(math.factorial(n)*(2*n+1))
            acc = acc + last
            if abs(last) < sys.float_info.epsilon: break
        res = cmath.exp(-z**2)*(1 + 2j*acc/math.sqrt(math.pi))

    else:
        old = 1e6
        h1 = 1
        h2 = 2*z
        u1 = 0
        u2 = 2*math.sqrt(math.pi)
        for n in range(1, 300):
            h3 = h2*z - n*h1
            u3 = u2*z - n*u1
            h1 = h2
            h2 = 2*h3
            u1 = u2
            u2 = 2*u3
            new = u3/h3
            if abs((new-old)/old) < 5e-6: break
            elif not np.isfinite(new):
                new = old
                break
            old = new
        res = 1j*new/math.pi

    if z_orig.real < 0:
        if z_orig.imag >= 0:
            res = np.conj(res)
        else:
            res = 2*cmath.exp(-z**2) - res
    elif z_orig.imag < 0:
        res = np.conj(2*cmath.exp(-z**2) - res)

    return res

# loop1(1.0+1j*1.0)