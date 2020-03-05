import matplotlib.animation as animation
import numpy as np
from tsl200 import TSL200
from tsl200 import laser_init
from matplotlib import pyplot as plt
import piplates.DAQC2plate as DAQC2
from v_to_dbm import v_to_dbm
import time

x = np.arange(0, 2*np.pi, 0.1)
y = np.sin(x)

laser_source = 0
laser_cw = 1550.0
laser_dbm = 7

laser = laser_init(0)
laser.set_wavelength(laser_cw)
laser.set_power_dBm(laser_dbm)
laser.on()

delay = 30e-3
buffer = 5 # Time to remember

data = np.zeros((int(buffer/delay),))
time_buff = np.linspace(0,buffer,int(buffer/delay))

I = 1

fig = plt.figure()
line, = plt.plot(time_buff,data,linewidth=2)
plt.xlabel('Time (s)')
plt.ylim([-90,0])
#plt.ylim(-1,5)
plt.ylabel('Power (dBm)')
plt.grid(True)
plt.tight_layout()

def animate(i):
    # Left shift data
    data[0:-1] = data[1:]
    
    # Record current time
    data[-1] = v_to_dbm(DAQC2.getADC(0,0),laser_cw*1e-3)
    
    line.set_ydata(data)
    
    return [line]


# We'd normally specify a reasonable "interval" here...
ani = animation.FuncAnimation(fig, animate, range(1, 200), 
                              interval=0, blit=True)
plt.show()

laser.close()

