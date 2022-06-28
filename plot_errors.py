import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib
# import seaborn as sns


def load_errors(filename, err_lim):
    #filnames - list of str txt files names
    content = np.loadtxt(filename)
    content[content<err_lim] = err_lim

    return content

def convert_to_square_2d(arr):
    square_shape = int(np.sqrt(len(arr))), int(np.sqrt(len(arr)))
    arr = arr.reshape(square_shape)

    return arr


def plot_error(ax, x,y,z, title, vextr=None, n_orders_div=1):
    # fig, ax = plt.subplots(figsize=(8,6))
    if vextr is not None:
        z = np.clip(a=z, a_min=vextr[0], a_max=vextr[1])
        n_orders = int(np.ceil(np.abs(np.log10(vextr[0]) -
                                      np.log10(vextr[1])))) // n_orders_div #// 2 + 1
        cmap_idv = matplotlib.colors.ListedColormap(sns.color_palette("RdBu_r", n_orders))
        im  = ax.imshow(
            #np.vectorize(mpmath.log10)(z).astype(np.float64),
            z.astype(np.float64),
            origin="lower",extent=[exp_min,exp_max,exp_min,exp_max],aspect='auto',
            norm=LogNorm(vmin=vextr[0], vmax=vextr[1]),
            cmap=cmap_idv)
    else:
        im = ax.imshow(np.vectorize(mpmath.log10)(z).astype(np.float64),
                       origin="bottom",extent=[exp_min,exp_max,exp_min,exp_max],aspect='auto',
                       cmap=cmap_std)

    ax.set_title(title)
    ax.set_xlabel('real')
    ax.set_ylabel('imaginary')
    ax.set_xticklabels([ "$10^{" + str(i) + "}$" for i in range(exp_min, exp_max + 1, 2)])
    ax.set_yticklabels([ "$10^{" + str(i) + "}$" for i in range(exp_min, exp_max + 1, 2)])
    ax.grid(True, c='black', ls='--')

    return im


def get_extr(z):
    return [10**np.floor(np.log10(np.min(z.astype(np.float64)))),
            10**np.ceil(np.log10(np.max(z.astype(np.float64))))]


err_lim = 1e-16
x, y = np.loadtxt('x.txt'), np.loadtxt('y.txt')
x = convert_to_square_2d(x)
y = convert_to_square_2d(y)
py_rp_err, py_ip_err = load_errors('rp_err.txt', err_lim), load_errors('ip_err.txt', err_lim)
# fort_MIT_re_err, fort_MIT_im_err = load_errors('MIT_re_err.txt', err_lim), load_errors('MIT_im_err.txt', err_lim)
print('max_MIT_re_err = ')
print(max(py_rp_err))
print('max_MIT_im_err = ')
print(max(py_ip_err))
# fort_MIT_re_err = convert_to_square_2d(fort_MIT_re_err)
# fort_MIT_im_err = convert_to_square_2d(fort_MIT_im_err)
# scipy_re_err, scipy_im_err = load_errors('scipy_re_err.txt', err_lim), load_errors('scipy_im_err.txt', err_lim)
# scipy_re_err = convert_to_square_2d(scipy_re_err)
# scipy_im_err = convert_to_square_2d(scipy_im_err)
# Zaghoul_re_err, Zaghoul_im_err = load_errors('Zaghoul_re_err.txt', err_lim), load_errors('Zaghoul_im_err.txt', err_lim)
# print('max_Zaghoul_re_err = ')
# print(max(Zaghoul_re_err))
# print('max_Zaghoul_im_err = ')
# print(max(Zaghoul_im_err))
# Zaghoul_re_err = convert_to_square_2d(Zaghoul_re_err)
# Zaghoul_im_err = convert_to_square_2d(Zaghoul_im_err)

cmap_std = matplotlib.colors.ListedColormap(sns.color_palette("RdBu_r", 16))
exp_min = -8
exp_max = 8
# implementations = [fort_MIT_re_err, fort_MIT_im_err, Zaghoul_re_err, Zaghoul_im_err]
# impls_str = ['Johnson real error', 'Johnson image error', 'Zaghoul real error', 'Zaghoul image error']

fig = plt.figure(figsize=(12,7*2))
fig.tight_layout()
fig.subplots_adjust(hspace = .3, wspace=.2)
for i in range(4):
    ax = fig.add_subplot(2,2,i+1)
    im = plot_error(ax,x,y,implementations[i], title=impls_str[i], vextr=[err_lim, 10**-11])

cb_ax = fig.add_axes([0.92, 0.1, 0.01, 0.8])
cbar = fig.colorbar(im, cax=cb_ax)
cbar.set_label('relative error', labelpad=10, rotation=270)
plt.show()

