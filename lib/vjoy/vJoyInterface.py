"""
Python interface for http://vjoystick.sourceforge.net/ (vJoyInterface.dll)
"""

import ctypes
import os

class Axis(object):
    X = 0x30
    Y = 0x31
    Z = 0x32
    RX = 0x33
    RY = 0x34
    RZ = 0x35
    SL0 = 0x36
    SL1 = 0x37
    WHL = 0x38
    POV = 0x39

class VjdStat(object):
	VJD_STAT_OWN = 0  # The  vJoy Device is owned by this application.
	VJD_STAT_FREE = 1 # The  vJoy Device is NOT owned by any application (including this one).
	VJD_STAT_BUSY = 2 # The  vJoy Device is owned by another application. It cannot be acquired by this application.
	VJD_STAT_MISS = 3 # The  vJoy Device is missing. It either does not exist or the driver is down.
	VJD_STAT_UNKN = 4 # Unknown

class vJoyInterface(object):
    """
    Low level interface to the vJoyInterface.dll library
    """
    
    vJoyInterface_dll = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), "VJoyInterface.dll"))

    functions = {
        # General driver data
        'GetvJoyVersion' : {'arguments' : [], 'returns' : ctypes.c_short},
        'vJoyEnabled' : {'arguments' : [], 'returns' : ctypes.c_bool},
        'GetvJoyManufacturerString' : {'arguments' : [], 'returns' : ctypes.c_wchar_p},
        'GetvJoyProductString' : {'arguments' : [], 'returns' : ctypes.c_wchar_p},
        'GetvJoySerialNumberString' : {'arguments' : [], 'returns' : ctypes.c_wchar_p},
        
        # vJoy Device properties
        # Get the number of buttons defined in the specified VDJ
        'GetVJDButtonNumber' : {'arguments' : [ctypes.c_uint], 'returns' : ctypes.c_int},
        # Get the number of descrete-type POV hats defined in the specified VDJ
        'GetVJDDiscPovNumber' : {'arguments' : [ctypes.c_uint], 'returns' : ctypes.c_int},
        # Get the number of descrete-type POV hats defined in the specified VDJ
        'GetVJDContPovNumber' : {'arguments' : [ctypes.c_uint], 'returns' : ctypes.c_int},
        # Test if given axis defined in the specified VDJ
        'GetVJDAxisExist' : {'arguments' : [ctypes.c_uint, ctypes.c_int], 'returns' : ctypes.c_bool},
        # Get logical Maximum value for a given axis defined in the specified VDJ
        'GetVJDAxisMax' : {'arguments' : [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p], 'returns' : ctypes.c_bool}, # argument 3 needs to be passed by reference
        # Get logical Minimum value for a given axis defined in the specified VDJ
        'GetVJDAxisMin' : {'arguments' : [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p], 'returns' : ctypes.c_bool}, # argument 3 needs to be passed by reference
        
        # Write access to vJoy Device - Basic
        # Acquire the specified vJoy Device.
        'AcquireVJD' : {'arguments' : [ctypes.c_uint], 'returns' : ctypes.c_bool},
        # Relinquish the specified vJoy Device.
        'RelinquishVJD' : {'arguments' : [ctypes.c_uint], 'returns' : None},
        # 'UpdateVJD' : {} - unimplemented - we won't be updating the position data with this function. We will use the robust approach - refer to the vjoy documentation for further details.
        # Get the status of the specified vJoy Device.
        'GetVJDStatus' : {'arguments' : [ctypes.c_uint], 'returns' : ctypes.c_int},
        
        # Reset functions
        # Reset all controls to predefined values in the specified VDJ
        'ResetVJD' : {'arguments' : [ctypes.c_uint], 'returns' : ctypes.c_bool},
        # Reset all controls to predefined values in all VDJ
        'ResetAll' : {'arguments' : [], 'returns' : None},
        # Reset all buttons (To 0) in the specified VDJ
        'ResetButtons' : {'arguments' : [ctypes.c_uint], 'returns' : ctypes.c_bool},
        # Reset all POV Switches (To -1) in the specified VDJ
        'ResetPovs' : {'arguments' : [ctypes.c_uint], 'returns' : ctypes.c_bool},

        # Write data
        # Write Value to a given axis defined in the specified VDJ
        'SetAxis' : {'arguments' : [ctypes.c_long, ctypes.c_uint, ctypes.c_uint], 'returns' : ctypes.c_bool},
        # Write Value to a given button defined in the specified VDJ
        'SetBtn' : {'arguments' : [ctypes.c_bool, ctypes.c_uint, ctypes.c_uint], 'returns' : ctypes.c_bool},
        # 'SetDiscPov' - unimplemented
        # 'SetContPov' - unimplemented
    }

    @classmethod
    def init(cls):
        """
        Static class initializer.
        Defines the methdos in cls.functions dictionary
        """
        for function_name in cls.functions:
            function = getattr(cls.vJoyInterface_dll, function_name)
            if 'arguments' in cls.functions[function_name]:
                function.argtypes = cls.functions[function_name]['arguments']
            if 'returns' in cls.functions[function_name]:
                function.restype = cls.functions[function_name]['returns']
            setattr(cls, function_name, function)

vJoyInterface.init()

#print vJoyInterface.GetvJoyVersion()
#print vJoyInterface.vJoyEnabled()
#print vJoyInterface.GetvJoyManufacturerString()
#print vJoyInterface.GetvJoyProductString()
#print vJoyInterface.GetvJoySerialNumberString()
#print vJoyInterface.GetVJDStatus(1)

#print vJoyInterface.GetVJDButtonNumber(1)



#_tprintf("Vendor: %S\nProduct :%S\nVersion Number:%S\n",\
#TEXT(GetvJoyManufacturerString()),\
#TEXT(GetvJoyProductString()),\
#TEXT(GetvJoySerialNumberString()));

