import numpy as np

def max_bpcs_complexity(ncols, nrows):
    return ((nrows-1)*ncols) + ((ncols-1)*nrows)

# Fungsi menentukan nilai kompleksitas dari gambar
def arr_bpcs_complexity(arr):
    nrows, ncols = arr.shape
    max_complexity = max_bpcs_complexity(nrows, ncols)
    nbit_changes = lambda items, length: sum([items[i] ^ items[i-1] for i in range(1, length)])
    k = 0
    for row in arr:
        k += nbit_changes(row, ncols)
    for col in arr.transpose():
        k += nbit_changes(col, nrows)
    return (k*1.0)/max_complexity

# Fungsi untuk mengembalikan array ke dalam bentuk papan catur
def checkerboard(h, w):
    re = np.r_[ int(w/2)*[0,1] + ([0] if w%2 else [])]
    ro = 1-re
    return np.row_stack(int(h/2)*(re,ro) + ((re,) if h%2 else ()))

# Fungsi untuk melakukan konjugasi terhadap array
def conjugate(arr):
    wc = checkerboard(arr.shape[0], arr.shape[1]) # white pixel at origin
    bc = 1-wc # black pixel at origin
    return np.array([[wc[i,j] if arr[i,j] else bc[i,j] for j, cell in enumerate(row)] for i, row in enumerate(arr)])
