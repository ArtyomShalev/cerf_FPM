from cerf import *

import math


def check_for_inf(num, denom):
    #function checks for +inf or -inf value in numerator or denominator
    if abs(num) == math.inf or abs(denom) == math.inf:
        return True
    else:
        return False


def calculate_rel_error(value, reference):
    # calculating relative errors https://en.wikipedia.org/wiki/Relative_change_and_difference
    num = value - reference
    denom = max(value, reference)
    if check_for_inf(num, denom):
        return math.nan
    else:
        return abs(num/denom)


X = np.loadtxt('x.txt')
Y = np.loadtxt('y.txt')
# generators for rp and ip
rp_gen = (cerf(x+1j*y).real for x, y in zip(X,Y))
ip_gen = (cerf(x+1j*y).imag for x, y in zip(X,Y))
# converting to numpy arrays
rp = np.fromiter(rp_gen, float)
ip = np.fromiter(ip_gen, float)
# loading references
rp_ref = np.loadtxt('rp_ref.txt')
ip_ref = np.loadtxt('ip_ref.txt')
# calculate relative errors
rp_err, ip_err = [], []
for i in range(len(rp)):
    rp_err.append(calculate_rel_error(rp[i], rp_ref[i]))
    ip_err.append(calculate_rel_error(ip[i], ip_ref[i]))

np.savetxt('rp_err.txt', rp_err)
np.savetxt('ip_err.txt', ip_err)


