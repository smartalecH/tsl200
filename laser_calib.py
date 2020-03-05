from tsl200 import laser_init
import numpy as np
import time
from matplotlib import pyplot as plt
import piplates.DAQC2plate as DAQC2
from v_to_dbm import v_to_dbm


sleep = 50e-3

my_laser = laser_init()
my_laser.on()

M = 100
N = 300
wavelength = np.linspace(1530,1580,N)
data = [0]*N
my_laser.set_wavelength(1530)
time.sleep(8)
for wn,w in enumerate(wavelength):
    my_laser.set_wavelength(w)
    time.sleep(sleep)
    for m in range(M):
        data[wn] += v_to_dbm(DAQC2.getADC(0,0),w*1e-3)
    data[wn] = data[wn]/M + 6.4
    print("OK")

data = data[2:-1]
wavelength = wavelength[2:-1]
p = np.polyfit(wavelength, data,4)
print(p)


plt.figure()
plt.plot(wavelength, data)
plt.plot(wavelength, np.polyval(p,wavelength))
plt.show()
