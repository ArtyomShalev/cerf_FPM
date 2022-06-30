from cerf import *

from scipy import special
import time

# def run_tests():
#     assert special.erf(1.0+1j*2.0) == -0.5366435657785664 + 1j*-5.0491437034470374

def measure_time(func, arg, iters):
    start, end = [], []
    for _ in range(iters):
        start.append(time.time())
        func(arg)
        end.append(time.time())
    start, end = np.array(start), np.array(end)
    average_time = sum(end - start)/len(end)

    # print(average_time, '[s]')

    return average_time

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

# ------ using generators -------
# results = (cerf(z) for z in Z)
# for result in results:
#     print(result)
# ------ using for loop ---------
# rp, ip = cerf_py(Z)
# np.savetxt('py_rp.txt', rp)
# np.savetxt('py_ip.txt', ip)
# ----- time measuring --------
if is_time_measure_needed:
    times = []
    for i in range(1000):
        start = time.time()
        cerf_py(Z)
        times.append(time.time() - start)
    print(min(times), 's')

# print('Py', sum(total_time_py)/len(total_time_py))
# print('Scipy', sum(total_time_scipy)/len(total_time_scipy))



# ----- scipy ----
rp, ip = cerf_scipy(Z)
np.savetxt('scipy_rp.txt', rp)
np.savetxt('scipy_ip.txt', ip)