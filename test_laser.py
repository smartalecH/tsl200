from tsl200 import laser_init
import numpy as np
import time
from matplotlib import pyplot as plt
import piplates.DAQC2plate as DAQC2
from v_to_dbm import v_to_dbm
from tsl_offset import tsl_offset

sleep = 50e-3

my_laser = laser_init()
my_laser.on()

N = 300
wavelength = np.linspace(1530,1600,N)
data = [None]*N
power = [None]*N
my_laser.set_wavelength(1530)
time.sleep(4)
for wn,w in enumerate(wavelength):
    my_laser.set_wavelength(w)
    time.sleep(sleep)
    data[wn] = v_to_dbm(DAQC2.getADC(0,0),w*1e-3)
    data[wn] = tsl_offset(data[wn],w)
    power[wn] = my_laser.set_power_dBm(0)
    print("Data recorded")
    
plt.figure()
plt.plot(wavelength,data)
plt.show()
