import numpy as np

def v_to_dbm(v,wavelength):
    
    A = -0.8541
    B = 2.6141
    C = 1.5068
    v_cal = A*wavelength**2 + B*wavelength + C
    p_dbm = 20*(v - v_cal)
    return p_dbm
