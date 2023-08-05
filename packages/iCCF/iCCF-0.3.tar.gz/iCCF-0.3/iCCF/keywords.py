import numpy as np
from astropy.io import fits

def getRV(fitsfile, keyword=None):
    hdul = fits.open(fitsfile)
    if keyword is not None:
        return hdul[0].header[keyword]
    
    # need to look for it
    fail = ValueError(f'Could not find any RV keyword in header of "{fitsfile}"')
    
    try: return hdul[0].header['HIERARCH ESO QC CCF RV']
    except KeyError: pass
    
    try: return hdul[0].header['HIERARCH ESO DRS CCF RVC']
    except KeyError: pass

    raise fail

def getRVarray(fitsfile, keywords=None):
    hdul = fits.open(fitsfile)

    try:
        sta, ste, n = (hdul[0].header['HIERARCH ESO RV START'],
                       hdul[0].header['HIERARCH ESO RV STEP'],
                       hdul[1].header['NAXIS1'])
    except KeyError:
        try:
            sta, ste, n = (hdul[0].header['CRVAL1'],
                           hdul[0].header['CDELT1'],
                           hdul[0].header['NAXIS1'])
        except KeyError:
            raise KeyError
    finally:
        return sta + ste * np.arange(n)


def getBJD(fitsfile, keyword=None):
    hdul = fits.open(fitsfile)
    if keyword is not None:
        return hdul[0].header[keyword]
    
    # need to look for it
    fail = ValueError(f'Could not find any BJD keyword in header of "{fitsfile}"')
    
    try: return hdul[0].header['HIERARCH ESO QC BJD'] - 24e5
    except KeyError: pass
    
    try: return hdul[0].header['HIERARCH ESO DRS BJD'] - 24e5
    except KeyError: pass

    try: return hdul[0].header['MJD-OBS']
    except KeyError: pass

    raise fail


def get_wave(fitsfile):
    """ 
    Try to get the wavelength "matrix" of all the orders in the s2d spectra
    """
    if '_wave' in fitsfile: # this should have it
        pass

    hdul = fits.open(fitsfile)
    if hdul[0].header['INSTRUME'] == 'ESPRESSO':
        if not 'S2D' in hdul[0].header['PIPEFILE']:
            raise ValueError('for ESPRESSO, please provide the `s2d` fits file')
        wave = hdul[4].data
        return wave
    else:
        pass
        # find wave keyword
