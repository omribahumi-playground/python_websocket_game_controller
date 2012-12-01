#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from lib.vjoy.vJoyInterface import *
from lib.websocket.WebSocketRpcHandler import *

def maprange(s, a1, a2, b1, b2):
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

class JoystickDispatcher(WebSocketRpcHandler):
    """
    This class dispatches commands to the VirtualJoystick interface
    """

    # dictionary that maps all Axis attributes strings to their corresponding values
    _axis = dict([(attr, getattr(Axis, attr)) for attr in [attr for attr in dir(Axis) if not attr.startswith('_')]])

    def initialize(self, vjoy):
        self.vjoy = vjoy

    @WebSocketRpcHandler.expose
    def axe(self, axe, value):
        if not axe in self._axis:
            print 'Unknown axe %r' % (axe,)
        elif not self._axis[axe] in self.vjoy.axe:
            print "vJoy doesn't support axe %r" % (axe,)
        else:
            axe = self.vjoy.axe[self._axis[axe]]
            axe.value = maprange(value, -10, 10, axe.min, axe.max);
            return True
    
    @WebSocketRpcHandler.expose
    def button(self, button, pressed):
        self.vjoy.button[button-1].pressed = pressed
        return True
        
    @WebSocketRpcHandler.expose
    def buttons(self):
        return len(self.vjoy.button)
        
__all__ = ['JoystickDispatcher']
