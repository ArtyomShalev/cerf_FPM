#this script allows to calculate Faddeeva function for 1 quarter of complex plane (1e-8, 1e8)

import mpmath as mp
import numpy as np
from timeit import default_timer as timer


def init_arrs(arr_names, arr_len, max_str_len):
    lines = []
    line = (f'complex(dp):: {arr_names[0]}({arr_len})')
    i = 1
    while True:
        line += (f',{arr_names[i]}({arr_len})')
        if (len(line) > max_str_len):
            line += '&'
            lines.append(line)
            line = ''
        i += 1
        if (i == len(arr_names)):
            lines.append(line)
            break
    if (lines[-1][-1] == '&'):
        lines[-1] = lines[-1][:-1] #remove last char &
    lines.append('')
    return lines


def declar_arrs(arr_names, arr_len, x, y, wr, wi):
    lines = []
    for arr_name in arr_names:
        if (arr_name[-4:] == 'args'):
            lines.append((f'{arr_name} = (/cmplx({x[0]}_dp,{y[0]}_dp,dp)&'))
            for i in range(1,arr_len):
                lines.append((f',cmplx({x[i]}_dp,{y[i]}_dp,dp)&'))
            lines[-1] = lines[-1][:-1] + '/)'
            lines.append('')
        if (arr_name[-4:] == 'refs'):
            lines.append((f'{arr_name} = (/cmplx({wr[0]}_dp,{wi[0]}_dp,dp)&'))
            for i in range(1,arr_len):
                lines.append((f',cmplx({wr[i]}_dp,{wi[i]}_dp,dp)&'))
            lines[-1] = lines[-1][:-1] + '/)'
            lines.append('')
    return lines


def cerf(X, Y):
    RP = []
    IP = []
    for x, y in zip(X, Y):
        z = mp.mpc(x, y)
        w = mp.erf(z)
        RP.append(w.real)
        IP.append(w.imag)
    return RP, IP


def results_to_one_str(RP, IP, output_dps):
    string = ''
    for rp, ip in zip(RP, IP):
        string += mp.nstr(rp, output_dps)+mp.nstr(ip, output_dps)
    return string


def results_postprocessing(RP, IP, output_dps):
    RP_processed = []
    IP_processed = []
    for rp, ip in zip(RP, IP):
        RP_processed.append(mp.nstr(rp, output_dps))
        IP_processed.append(mp.nstr(ip, output_dps))
    return RP_processed, IP_processed


start = timer()
single_arg_calculation = False
output_dps = 30
accuracy_dps = 30
mp.mp.dps = accuracy_dps
max_str_len = 100
exp_min = -8
exp_max = 8
npts = 10
r = 10**np.linspace(exp_min, exp_max, npts)
arr_names = ['erf_w_args', 'erf_w_refs']
# arr_names_extra = ['erf_w_extra_args']
args_refs_filename = 'erf_mpmath.f90'
x, y = np.meshgrid(r,r)
x = np.reshape(x, npts**2)
y = np.reshape(y, npts**2)
#--- if single args are needed to be calculated (old_version) -------
if single_arg_calculation:
    x = [1.0]
    y = [0.0]
    rp, ip = mp.erf(x+1j*y)
    old_string = results_to_one_str(rp, ip, output_dps)
    accuracy_dps = int(accuracy_dps*1.41)
    mp.mp.dps = accuracy_dps
    rp, ip = mp.erf(x+1j*y)
    new_string = results_to_one_str(rp, ip, output_dps)
#-------------------------------------------------------------------
else:
    RP, IP = cerf(x,y)
    old_string = results_to_one_str(RP, IP, output_dps)
    accuracy_dps = int(accuracy_dps*1.41)
    mp.mp.dps = accuracy_dps
    RP, IP = cerf(x,y)
    new_string = results_to_one_str(RP, IP, output_dps)
    counter = 0
    while(new_string != old_string):
        counter += 1
        if counter >= 5: break
        print('Calculating with more precision')
        old_string = new_string
        accuracy_dps = int(accuracy_dps*1.41)
        mp.mp.dps = accuracy_dps
        RP, IP = cerf(x,y)
        new_string = results_to_one_str(RP, IP, accuracy_dps)

# ---- if reference data are needed only in txt format ---------
# output_dps = 30
# with open('wr_ref.txt', 'w') as f:
#     for line in wr:
#         f.write(mp.nstr(line, output_dps))
#         f.write('\n')
#
# with open('wi_ref.txt', 'w') as f:
#     for line in wi:
#         f.write(mp.nstr(line, output_dps))
#         f.write('\n')
# --------------------------------------------------------
    RP, IP = results_postprocessing(RP, IP, output_dps)
    arr_init_lines = init_arrs(arr_names, len(x), max_str_len)
    arr_declar_lines = declar_arrs(arr_names, len(x), x, y, RP, IP)
    lines = arr_init_lines + arr_declar_lines
    with open(args_refs_filename, 'w') as f:
        for line in lines:
            f.write(line)
            f.write('\n')
    np.savetxt('x.txt', x)
    np.savetxt('y.txt', y)

end = timer()
print('Time for generating test args and refs [s]', end-start)



