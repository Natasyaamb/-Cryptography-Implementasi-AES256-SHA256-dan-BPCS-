# Mendapatkan besaran kapasitas pesan yang dapat disisipkan ke dalam file cover-image

import os.path

import numpy as np
import matplotlib.pyplot as plt

from logger import log
from act_on_image import ActOnImage
from bpcs_steg import arr_bpcs_complexity, conjugate, max_bpcs_complexity
from array_message import get_n_message_grids
from array_grid import get_next_grid_dims

# Fungsi untuk membuat histogram kompleksitas gambar
def histogram_of_complexity(arr, grid_size, alpha, comp_fcn):
    log.critical('Creating histograms of image complexity...')
    max_complexity = max_bpcs_complexity(*grid_size)
    vals = [arr_bpcs_complexity(arr[tuple(dims)]) for dims in get_next_grid_dims(arr, grid_size)]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ns, bins, patches = ax.hist(vals, 200, facecolor='red', alpha=0.75)

    navail = sum([n for n, bin in zip(ns, bins) if comp_fcn(bin, alpha)])
    return fig, navail, sum(ns)

# Fungsi untuk mengacak kompleksitas gambar
def rand_image_complexity(arr, alpha, comp_fcn, grid_size):
    n = 0
    for dims in get_next_grid_dims(arr, grid_size):
        grid = arr[dims]
        if comp_fcn(arr_bpcs_complexity(grid), alpha): # < or >
            n += 1
            init_grid = np.copy(grid)
            np.random.shuffle(init_grid.reshape(-1))
            arr[dims] = init_grid
    log.critical('Conjugated {0} grids'.format(n))
    return arr, n

# Fungsi untuk mendapatkan nilai kompleksitas dari gambar yang dibalik
def flip_image_complexity(arr, alpha, comp_fcn, grid_size):
    n = 0
    for dims in get_next_grid_dims(arr, grid_size):
        grid = arr[dims]
        if comp_fcn(arr_bpcs_complexity(grid), alpha): # < or >
            n += 1
            init_grid = np.copy(grid)
            arr[dims] = conjugate(grid)
            assert abs((1 - arr_bpcs_complexity(init_grid)) - arr_bpcs_complexity(grid)) < 0.01
            assert not(arr[dims].tolist() == init_grid.tolist() and alpha != 0.5)
    log.critical('Conjugated {0} grids'.format(n))
    return arr, n

# Kelas dari histogram kompleksitas gambar
class HistogramComplexityImage(ActOnImage):
    def modify(self, alpha, comp_fcn, grid_size=(8,8)):
        hist, navail, ntotal = histogram_of_complexity(self.arr, grid_size, alpha, comp_fcn)
        log.critical('{0} of {1} grids available with alpha of {2}'.format(navail, ntotal, alpha))
        nbits_per_grid = grid_size[0]*grid_size[1]
        nbytes = (get_n_message_grids([nbits_per_grid]*int(navail), int(navail))*nbits_per_grid)/8.0
        percent = nbytes*1.0/os.path.getsize(self.infile)
        log.critical('Approximately {0} bytes of storage space can fit in this vessel image.'.format(nbytes))
        log.critical('{0} byte message would utilize {1:.1%} of the vessel image.'.format(nbytes, percent))
        return hist

# Kelas pengkompleksan gambar
class ComplexifyImage(ActOnImage):
    def modify(self, alpha, grid_size=(8,8)):
        new_arr = np.array(self.arr, copy=True)
        return rand_image_complexity(new_arr, alpha, lambda x,thresh: x>=thresh, grid_size)

# Kelas penyederhanaan gambar
class SimplifyImage(ActOnImage):
    def modify(self, alpha, grid_size=(8,8)):
        new_arr = np.array(self.arr, copy=True)
        return rand_image_complexity(new_arr, alpha, lambda x,thresh: x<thresh, grid_size)

# Fungsi histogram
def histogram(infile, outfile, alpha, comp_fcn):
    x = HistogramComplexityImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    hist = x.modify(alpha, comp_fcn)
    if outfile is not None:
        hist.savefig(outfile)
        log.critical('Wrote histogram of image complexity to {0}'.format(outfile))

# Fungsi pengompleksan
def complexify(infile, outfile, alpha):
    x = ComplexifyImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    arr, stats = x.modify(alpha)
    x.write(outfile, arr)
    return stats

# Fungsi penyederhanaan
def simplify(infile, outfile, alpha):
    x = SimplifyImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    arr, stats = x.modify(alpha)
    x.write(outfile, arr)
    return stats

# Fungsi kapasitas
def capacity(infile, alpha=0.45, outfile=None):
    greater = lambda x,thresh: x>=thresh
    histogram(infile, outfile, alpha, greater)
