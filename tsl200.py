import pyvisa
import sys
from time import sleep

def laser_init(idx=0):
    #view resources, find the GPIB
    rm = pyvisa.ResourceManager()
    rl = rm.list_resources()

    GPIB_list = [item for item in rl if item[0:4] == 'GPIB']
    if len(GPIB_list) == 0:
        sys.exit("No GPIB Instrument Found -- Chris Conrey.")
    else:
        my_GPIB = GPIB_list[idx]

    #construct a laser object with resource corresp. to laser's GPIB input
    device = rm.open_resource(my_GPIB)
    my_laser = TSL200(device)
    print("SUCCESSFUL CONSTRUCTION")
    print(my_laser.device)
    
    return my_laser

class TSL200:
    def __init__(self, device, terminator="\r"):
        """
        Connect to the TSL200. Address is the serial port, baudrate
        can be set on the device, terminator is the string the marks
        the end of the command.
        """
        self.device = device
        
        #if sys.version_info.major >= 3: # Python 3 compatibility: convert to bytes
            #terminator = terminator.encode("ASCII")
        self.terminator = terminator
        
    def write(self, command):
        """
        Write a command to the TSL220. Returns the response (if any).
        """

        # Convert to bytes (Python 3 compatibility)
        #if sys.version_info.major >= 3:
            #command = command.encode("ASCII")

        # Write the command
        response = self.device.query(command + self.terminator)

        return response

    def _set_var(self, name, precision, val):
        """
        Generic function to set a floating-point variable on the
        laser, or return the current value.
        """

        if val is not None:
            command = ("{}{:."+str(precision)+"f}").format(name, val)
        else:
            command = name
        print(command)
        response = self.write(command)
        return float(response)

    def on(self):
        """Turn on the laser diode"""

        self.is_on = True
        self.write("LO")

    def off(self):
        """Turn off the laser diode"""

        self.is_on = False
        self.write("LF")

    def set_wavelength(self, val=None):
        """
        Tune the laser to a new wavelength. If a value is not
        specified, return the current one. Units: nm.
        """

        return self._set_var("WA", 4, val)
    
    def set_power_dBm(self, val=None):
        """
        Set the output optical power in decibel-milliwatts. If a value
        is not specified, return the current one.
        """

        return self._set_var("OP", 2, val)


