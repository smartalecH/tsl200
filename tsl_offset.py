import numpy as np

def tsl_offset(pwr_dBm, wavelength):
    p = [ 6.06756910e-06, -3.76165439e-02,  8.74451768e+01, -9.03383850e+04, 3.49947251e+07] # valid for 1530 to 1580 nm
    pwr_cal = np.polyval(p,wavelength)
    pwr = pwr_dBm - pwr_cal
    return pwr


