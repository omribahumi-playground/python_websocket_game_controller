#!/usr/bin/python
import os
import tornado
from lib.vjoy.VirtualJoystick import *
from lib.JoystickDispatcher import *
from lib.RpcHandler import *

def main():
    vjoy = VirtualJoystick(1)
    # position all axis on center
    for axe in [Axis.X, Axis.Y, Axis.Z]:
        vjoy.axe[axe].value = int(0.50*vjoy.axe[axe].max)
    
    # TODO: Add support for multiple joysticks
    application = tornado.web.Application([
        (r"/websocket/joystick/1",
            WebSocketRpcHandler.wrap(JoystickDispatcher), {'vjoy' : vjoy}),
        (r"/post/joystick/1",
            PostRpcHandler.wrap(JoystickDispatcher), {'vjoy' : vjoy}),
        (r"/(.*)", tornado.web.StaticFileHandler,
            {"path": os.path.join(os.path.dirname(__file__), "static"),
            "default_filename" : "index.html"})
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
