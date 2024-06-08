import itertools
from logger import log
from functools import reduce

#Melakukan Iterasi Grid
def get_next_grid_dims(arr, dims):
    nrows, ncols = arr.shape[0], arr.shape[1]
    rows_per_grid, cols_per_grid = dims[0], dims[1]

    def get_inds(total_length, grid_length):
        lefts = range(0, total_length, grid_length)
        rights = [min(total_length, left+grid_length) for left in lefts]
        return list(zip(lefts, rights))
    xs = get_inds(nrows, rows_per_grid)
    ys = get_inds(ncols, cols_per_grid)

    nlayers = len(arr.shape)-2
    assert nlayers > 0
    inds = [range(arr.shape[i+2]) for i in range(nlayers)]
    zs = itertools.product(*inds)
    ngrids = reduce(lambda x,y: x*y, [len(x) for x in inds], 1)*len(xs)*len(ys)
    log.critical('Found {0} grids'.format(ngrids))
    i = 0
    for z in zs:
        for (xleft, xright) in xs:
            for (yleft, yright) in ys:
                i += 1
                if i % 10000 == 0:
                    log.critical('Grid {0} of {1}'.format(i, ngrids))
                yield [slice(xleft, xright), slice(yleft, yright)] + list(z)

if __name__ == '__main__':
    pass
