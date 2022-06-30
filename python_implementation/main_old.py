from cerf import *

import math
from scipy import special


def measure_time(func, arg, iters):
    start, end = [], []
    for _ in range(iters):
        start.append(time.time())
        func(arg)
        end.append(time.time())
    start, end = np.array(start), np.array(end)
    average_time = sum(end - start)/len(end)

    #print(average_time, '[s]')
    return average_time


def check_for_inf(num, denom):
    #function checks for +inf or -inf value in numerator or denominator
    if abs(num) == math.inf or abs(denom) == math.inf:
        return True
    else:
        return False

def calculate_rel_error(value, reference, err_upper_limmit):
    # calculating relative errors https://en.wikipedia.org/wiki/Relative_change_and_difference
    num = value - reference
    denom = max(value, reference)
    if check_for_inf(num, denom) or abs(num/denom) > err_upper_limmit:
        return math.nan
    else:
        return abs(num/denom)


# is_time_measure_needed = False
#
# X = np.loadtxt('x.txt')
# Y = np.loadtxt('y.txt')
# # generators for rp and ip
# rp_gen = (cerf(x+1j*y).real for x, y in zip(X,Y))
# ip_gen = (cerf(x+1j*y).imag for x, y in zip(X,Y))
# for i in rp_gen:
#     print(i)
# # converting to numpy arrays
# rp = np.fromiter(rp_gen, float)
# ip = np.fromiter(ip_gen, float)
# # loading references
# rp_ref = np.loadtxt('rp_ref.txt')
# ip_ref = np.loadtxt('ip_ref.txt')
# # calculate relative errors
# rp_err, ip_err = [], []
# for i in range(len(rp)):
#     rp_err.append(calculate_rel_error(rp[i], rp_ref[i], 1))
#     ip_err.append(calculate_rel_error(ip[i], ip_ref[i], 1))
#
# np.savetxt('py_rp_err.txt', rp_err)
# np.savetxt('py_ip_err.txt', ip_err)
#
# # --- scipy erf ---------------------------------
# rp_gen = (special.erf(x+1j*y).real for x, y in zip(X,Y))
# ip_gen = (special.erf(x+1j*y).imag for x, y in zip(X,Y))
#
# # converting to numpy arrays
# rp = np.fromiter(rp_gen, float)
# ip = np.fromiter(ip_gen, float)
# # loading references
# rp_ref = np.loadtxt('rp_ref.txt')
# ip_ref = np.loadtxt('ip_ref.txt')
# # calculate relative errors
# rp_err, ip_err = [], []
# for i in range(len(rp)):
#     rp_err.append(calculate_rel_error(rp[i], rp_ref[i], 1))
#     ip_err.append(calculate_rel_error(ip[i], ip_ref[i], 1))
#
# np.savetxt('scipy_rp_err.txt', rp_err)
# np.savetxt('scipy_ip_err.txt', ip_err)
#
# if is_time_measure_needed:
#     import time
#     measure_time(cerf, 1+1j*1, iters=100)


print(cerf(10.0+1j*1.0))


