import numpy as np
from astropy.io import fits

from .gaussian import gaussfit
from .keywords import get_wave, getRV, getRVarray
from .utils import get_orders_mean_wavelength


def each_order_rv(rv, ccfs, exclude_last=True):
    """
    Calculate RVs for each spectral order by fitting Gaussians to individual CCFs
    
    Parameters
    ----------
    rv : array
        Radial velocities where each CCF is defined
    ccfs : array
        The CCFs for each spectral order (order o, radial velocity rv)
    exclude_last : bool
        Whether to exclude the last index of ccfs (usually the sum of all other 
        CCFs) from the calculation.
    
    Returns
    -------
    rvs : array
        The center of a Gaussian fit to each order's CCF
    """
    last = -1 if exclude_last else None
    
    gen = (gaussfit(rv, ccf)[1] for ccf in ccfs[:last])
    rvs = np.fromiter(gen, dtype=float)

    return rvs


def rv_color(rv, ccfs, blue=slice(0,80), red=slice(80,-1), avoid_blue=0, gap=0):
    """
    Calculate the RV color by combining blue and red CCFs

    Parameters
    ----------
    rv : array
        Radial velocities where each CCF is defined
    ccfs : array
        The CCFs for each spectral order (order o, radial velocity rv)
    blue : slice
        A slice object with the start and stop indices of the blue orders. The
        default (0:80) is for ESPRESSO. For HARPS, use ...
    red : slice
        A slice object with the start and stop indices of the red orders. The
        default (80:-1) is for ESPRESSO. For HARPS, use ...
    avoid_blue : int
        How many orders to skip in the bluest part of the spectrum. This will 
        be added to the beginning of the `blue` slice
    gap : int or tuple
        If an integer, the number of orders to remove from the "middle" for both
        blue and red parts. If a tuple, the number of orders to remove from the 
        blue and red, respectively
    """
    if isinstance(gap, tuple):
        gap_blue, gap_red = gap
    elif isinstance(gap, int):
        gap_blue = gap_red = gap
    else:
        raise ValueError(f"`gap` should be int or tuple, got {gap}")

    blue = slice(blue.start + avoid_blue, blue.stop - gap_blue)
    red = slice(red.start + gap_red, red.stop)

    ccf_blue = ccfs[blue, :].sum(axis=0)
    ccf_red = ccfs[red, :].sum(axis=0)
    
    rv_blue = gaussfit(rv, ccf_blue)[1]
    rv_red = gaussfit(rv, ccf_red)[1]
    print(rv_blue, rv_red)



def chromatic_index(rv, ccfs, wave, rvpipe=None):
    """ 
    Calculate the chromatic index, as described in Zechmeister et al. (2018).

    Parameters
    ----------
    rv : array
        Radial velocities where each CCF is defined   
    """
    if isinstance(wave, str): # assume it's a filename
        wave = get_wave(wave)
    elif isinstance(wave, np.ndarray):
        pass
    else:
        raise ValueError('`wave` should be filename or array with wavelengths')
        
    mean_wave = get_orders_mean_wavelength(wave, log=True)
    rvs = each_order_rv(rv, ccfs)

    ind = ~np.isnan(rvs)
    p = np.polyfit(np.log(mean_wave[ind]), rvs[ind], 1)

    if rvpipe is None:
        rvpipe = gaussfit(rv, ccfs[-1])[1]

    beta = p[0]
    lv = np.exp(abs((p[1] - rvpipe)/p[0]))
    return beta, lv



def chromatic_index_from_files(s2dfile, ccffile):
    """ 
    Calculate the chromatic index, as described in Zechmeister et al. (2018).

    Parameters
    ----------
    s2dfile : str
        Filename of the S2D fits file
    ccffile : str
        Filename of the CCF fits file
    """
    wave = get_wave(s2dfile)
    mean_wave = get_orders_mean_wavelength(wave, log=True)
    
    rvpipe = getRV(ccffile)
    rv = getRVarray(ccffile)

    ccfs = fits.open(ccffile)[1].data
    rvs = each_order_rv(rv, ccfs)

    return chromatic_index(rv, ccfs, wave, rvpipe)
