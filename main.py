#!/usr/bin/python
import tornado
import os
from lib.vjoy.VirtualJoystick import *
from lib.websocket.JoystickDispatcher import *

def main():
    vjoy = VirtualJoystick(1)
    # position all axis on center
    for axe in [Axis.X, Axis.Y, Axis.Z]:
        vjoy.axe[axe].value = int(0.50*vjoy.axe[axe].max)
    
    # TODO: Add support for multiple joysticks    
    application = tornado.web.Application([
        (r"/joystick/1", JoystickDispatcher, {'vjoy' : vjoy}),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static"), "default_filename" : "index.html"})
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
