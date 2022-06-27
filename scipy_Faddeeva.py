import numpy as np
from scipy import special

x = np.loadtxt('x.txt')
y = np.loadtxt('y.txt')
rp, ip = special.efc(x+1j*y).real, special.erf(x+1j*y).imag
rp_ref = np.loadtxt('rp_ref.txt')
ip_ref = np.loadtxt('ip_ref.txt')

scipy_re_err = np.abs((rp_ref - rp)/rp)
scipy_im_err = np.abs((ip_ref - ip)/ip)
np.savetxt('scipy_re_err.txt', scipy_re_err)
np.savetxt('scipy_im_err.txt', scipy_im_err)