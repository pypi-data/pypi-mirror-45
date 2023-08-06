"""Compute random deviates from arbitrary 1D and 2D distributions."""
import numpy as np
import numpy.random as random
from scipy import interpolate


def random_deviates_1d(x, f_x, num):
    """Compute random deviates from arbitrary 1D distribution.

    Uses Transformation method (Numerical Recepies, 7.3.2)
    """
    cumsum = f_x.cumsum()
    cumsum -= cumsum.min()
    cumsum /= cumsum.max()
    return np.interp(random.rand(num), cumsum, x)


def random_deviates_2d(fdist, x0, y0, num):
    """Compute random deviates from arbitrary 2D distribution.

    Uses acceptance/rejection method.
    Inputs:
        fdist: 2d array of relative probability
        x0: xaxis
        y0: yaxis
        num: number of points to choose
    outputs:
        x, y: vectors of length num
    """
    mx = (x0.max()-x0.min(), x0.min())
    my = (y0.max()-y0.min(), y0.min())
    fmax = fdist.max()

    xpts, ypts = [], []
    while len(xpts) < num:
        ux = random.rand(num)*mx[0] + mx[1]
        uy = random.rand(num)*my[0] + my[1]
        uf = random.rand(num)*fmax

        val = interpolate.interpn((x0, y0), fdist, (ux, uy))
        mm = uf < val
        xpts.extend(list(ux[mm]))
        ypts.extend(list(uy[mm]))

    xpts, ypts = xpts[0:num], ypts[0:num]
    un = xpts[0].unit
    xpts = np.array([i.value for i in xpts])*un
    un = ypts[0].unit
    ypts = np.array([i.value for i in ypts])*un
    return xpts, ypts
