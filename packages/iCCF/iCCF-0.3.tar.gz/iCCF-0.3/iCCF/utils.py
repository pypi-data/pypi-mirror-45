import os
import re
import numpy as np

_c = 299792.458


# from https://stackoverflow.com/a/30141358/1352183
def running_mean(x, N=2):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / N


# from https://stackoverflow.com/a/16090640
def natsort(s):
    return [
        int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)
    ]


def doppler_shift_wave(wave, rv, f=1.0+1.55e-8):
    """ 
    Doppler shift the wavelength array `wave` by the radial velocity `rv` [km/s].
    Note: positive values for `rv` indicate a red-shift. Negative values 
    indicate a blue-shift.

    Parameters
    ----------
    wave : array or float
        Original wavelength to be shifted
    rv : float
        Radial velocity [in km/s]
    """
    return wave * f * (1 + rv / _c)


def numerical_gradient(rv, ccf):
    """
    Return the gradient of the CCF.

    Parameters
    ----------
    rv : array
        The velocity values where the CCF is defined.
    ccf : array
        The values of the CCF profile.

    Notes
    -----
    The gradient is computed using the np.gradient routine, which uses second
    order accurate central differences in the interior points and either first
    or second order accurate one-sides (forward or backwards) differences at
    the boundaries. The gradient has the same shape as the input array.
    """
    return np.gradient(ccf, rv)


def get_orders_mean_wavelength(wave, order='all', log=True):
    """
    wave : array
        The wavelength "matrix" (order o, wavelength w)
    order : 'all' or int, optional
        If 'all', calculate mean wavelength for all orders, otherwise calculate
        only for the order `order`.
    log : bool, optional
        Whether to calculate mean log wavelength or mean wavelength.
    """
    if order == 'all':
        if log:
            return np.exp(np.log(wave).mean(axis=1))
        else:
            return wave.mean(axis=1)
    else:
        if log:
            return np.exp(np.log(wave[order,:]).mean())
        else:
            return wave[order,:].mean()


def find_myself():
    """ Return the path to iCCF's source. """
    thisdir = os.path.dirname(os.path.realpath(__file__))
    topdir = os.path.dirname(thisdir)
    return topdir


def load_example_data():
    """ Load the example CCF stored in iCCF/example_data """
    topdir = find_myself()
    return np.load(os.path.join(topdir, 'example_data', 'CCF1.npy'))
