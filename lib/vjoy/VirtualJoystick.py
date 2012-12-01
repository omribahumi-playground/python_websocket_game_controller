import ctypes
from vJoyInterface import vJoyInterface, VjdStat, Axis

class VirtualJoystickException(Exception):
    pass

class Axe(object):
    def __init__(self, vjoy, axe):
        self.vjoy = vjoy
        self.axe = axe
        self._value = 0
        
        if not vJoyInterface.GetVJDAxisExist(self.vjoy.vjoyId, axe):
            raise VirtualJoystickException("Axe %d doesn't exists on vJoy id %d" % (axe, self.vjoy.vjoyId))
        else:
            self.min = ctypes.c_ulong()
            self.max = ctypes.c_ulong()
            vJoyInterface.GetVJDAxisMin(self.vjoy.vjoyId, self.axe, ctypes.byref(self.min))
            vJoyInterface.GetVJDAxisMax(self.vjoy.vjoyId, self.axe, ctypes.byref(self.max))
            self.min = self.min.value
            self.max = self.max.value
        
        self.value = self.min
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if not self.min <= value <= self.max:
            raise VirtualJoystickException("Axe %d on vJoy id %d can't reach %d. min=%d max=%d" % (self.axe, self.vjoy.vjoyId, value, self.min, self.max))
        else:
            self._value = value
            if not vJoyInterface.SetAxis(self._value, self.vjoy.vjoyId, self.axe):
                raise VirtualJoystickException("Unable to update axis state. vjoyId=%d axis=%d value=%d" % (self.vjoy.vjoyId, self.axis, self._value))

    def __str__(self):
        return "<%s axe=%d value=%d min=%d max=%d>" % (self.__class__.__name__, self.axe, self._value, self.min, self.max)
    
    def __repr__(self):
        return str(self)

class Button(object):
    def __init__(self, vjoy, button):
        self.vjoy = vjoy
        self.button = button
        self.pressed = False
    
    @property
    def pressed(self):
        return self._pressed
    
    @pressed.setter
    def pressed(self, value):
        self._pressed = value
        if not vJoyInterface.SetBtn(self._pressed, self.vjoy.vjoyId, self.button):
            raise VirtualJoystickException("Unable to update button state. vjoyId=%d button=%d pressed=%s" % (self.vjoy.vjoyId, self.button, self._pressed))
    
    def __str__(self):
        return '<%s button=%d pressed=%s>' % (self.__class__.__name__, self.button, self.pressed)
    
    def __repr__(self):
        return str(self)
    
class VirtualJoystick(object):
    def __init__(self, vjoyId):
        """
        Construct a VirtualJoystick instance
        vjoyId is the joystick ID as vjoystick defines it.
        This method makes sure the device is free to acquire and acquires it
        """
        if not vJoyInterface.vJoyEnabled():
            raise VirtualJoystickException("vJoy doesn't seem to be enabled on this system. Please download and install vJoy from http://vjoystick.sourceforge.net/")
        elif vJoyInterface.GetVJDStatus(vjoyId) != VjdStat.VJD_STAT_FREE:
            raise VirtualJoystickException("vJoy id %d doesn't seem to be available" % (vjoyId,))
        elif not vJoyInterface.AcquireVJD(vjoyId):
            raise VirtualJoystickException("Unable to acquire vjoyId %d" % (vjoyId,))
        else:
            self.vjoyId = vjoyId
            
            self.button = [Button(self, buttonId) for buttonId in xrange(1, vJoyInterface.GetVJDButtonNumber(self.vjoyId)+1)]
            self.axe = {}
            for axe in [getattr(Axis, axe) for axe in dir(Axis) if not axe.startswith('_')]:
                if not vJoyInterface.GetVJDAxisExist(self.vjoyId, axe):
                    continue
                else:
                    self.axe[axe] = Axe(self, axe)
    
    def __del__(self):
        """destructor"""
        vJoyInterface.RelinquishVJD(self.vjoyId)
    
    def __str__(self):
        return "<%s vjoyId=%d buttons=%s, axe=%s>" % (self.__class__.__name__, self.vjoyId, self.button, self.axe)
    
    def __repr__(self):
        return str(self)

__all__ = ['Axis', 'Axe', 'Button', 'VirtualJoystick']