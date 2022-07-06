from cerf import *

from scipy import special
import time


def cerf_py_jit(Z):
    rp, ip = [], []
    for z in Z:
        result = cerf_jit(z)
        rp.append(result.real)
        ip.append(result.imag)

    return rp, ip


def cerf_py(Z):
    rp, ip = [], []
    for z in Z:
        result = cerf(z)
        rp.append(result.real)
        ip.append(result.imag)

    return rp, ip

def cerf_scipy(Z):
    rp, ip = [], []
    for z in Z:
        result = special.wofz(z)
        rp.append(result.real)
        ip.append(result.imag)

    return rp, ip


is_time_measure_needed = True

Z = [
    624.2+1j*-0.26123,
    -0.4+1j*3.0,
    0.6+1j*2.,
    -1.+1j*1.,
    -1.+1j*-9.,
    -1.+1j*9.,
    -0.0000000234545+1j*1.1234,
    -3.+1j*5.1,
    -53+1j*30.1,
    0.0+1j*0.12345,
    11+1j*1,
    -22+1j*-2,
    9+1j*-28,
    21+1j*-33,
    1e5+1j*1e5,
    1e14+1j*1e14,
    -3001+1j*-1000,
    1e160+1j*-1e159,
    -6.01+1j*0.01,
    -0.7+1j*-0.7,
    2.611780000000000e+01+1j*4.540909610972489e+03,
    0.8e7+1j*0.3e7,
    -20+1j*-19.8081,
    1e-16+1j*-1.1e-16,
    2.3e-8+1j*1.3e-8,
    6.3+1j*-1e-13,
    6.3+1j*1e-20,
    1e-20+1j*6.3,
    1e-20+1j*16.3,
    9+1j*1e-300,
    6.01+1j*0.11,
    8.01+1j*1.01e-10,
    28.01+1j*1e-300,
    10.01+1j*1e-200,
    10.01+1j*-1e-200,
    10.01+1j*0.99e-10,
    10.01+1j*-0.99e-10,
    1e-20+1j*7.01,
    -1+1j*7.01,
    5.99+1j*7.01,
    1+1j*0,
    55+1j*0,
    -0.1+1j*0,
    1e-20+1j*0,
    0+1j*5e-14,
    0+1j*51
]


# ----- time measuring --------
if is_time_measure_needed:
    print('---- args -> 10 000 times----------')
    sum = 0
    for z in Z:
        for i in range(10000):
            start = time.time()
            cerf(z)
            sum += time.time() - start
    print(f'Py {sum} [s]')

    sum = 0
    for z in Z:
        for i in range(10000):
            start = time.time()
            cerf_jit(z)
            sum += time.time() - start
    print(f'Py jit {sum} [s]')

    sum = 0
    for z in Z:
        for i in range(10000):
            start = time.time()
            special.wofz(z)
            sum += time.time() - start
    print(f'scipy {sum} [s]')

    print('---- 10 000 times -> args ----------')
    sum = 0
    for i in range(10000):
        start = time.time()
        cerf_py(Z)
        sum += time.time() - start
    print(f'Py {sum} [s]')

    sum = 0
    for i in range(10000):
        start = time.time()
        cerf_py_jit(Z)
        sum += time.time() - start
    print(f'Py jit {sum} [s]')

    sum = 0
    for i in range(10000):
        start = time.time()
        cerf_scipy(Z)
        sum += time.time() - start
    print(f'scipy {sum} [s]')

# ------ py implementation ---------
rp, ip = cerf_py_jit(Z)
np.savetxt('../data/py_rp.txt', rp)
np.savetxt('../data/py_ip.txt', ip)
# ----- scipy ----
rp, ip = cerf_scipy(Z)
np.savetxt('../data/scipy_rp.txt', rp)
np.savetxt('../data/scipy_ip.txt', ip)
