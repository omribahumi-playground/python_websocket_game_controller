python_web socket_game_controller
================================

Virtual joystick controlled through a web socket.
This projects gives you a web socket API to control a virtual joystick on your PC.
With a proper phone implementation, you can control any game supporting a joystick with your phone.
I've included a sample HTML5 application for demonstration.

Dependencies
------------
First, you'll need python-tornado installed for the code to run.
Second, you'll have to configure a virtual joystick. Grab the drivers from http://vjoystick.sourceforge.net/
You won't be needing the SDK.

Architecture
------------
This project actually contains several projects (I might split them to their own repositories soon):
* lib.vjoy
    * vJoyInterface.py - Low level interface to the vJoyInterface.dll (obtained from vjoystick sourceforge project SDL)
    * VirtualJoystick.py - Object oriented implementation for the vJoyInterface.py low level interface
* lib.websocket
    * WebSocketRpcHandler.py - RPC over WebSocket implementation for tornado
    * JoystickDispatcher.py - The exposed methods to the RPC over WebSocket clients

Usage
-----
The idea is simple - the client dispatches method calls to the JoystickDispatcher, which control the VirtualJoystick class that sends messages to the driver through the DLL.
Once running it, it defaults to listen on port 8888 and serve the static files on the root directory.
Simply run it and access http://<your_internal_ip_address>/ from your mobile phone. Don't forget connect your phone to Wifi first.

Known issues
------------
* Phone goes to sleep when not touching the screen (happens if you only use the gyroscope and not the on-screen buttons for a few seconds)
* Phone orientation changes when tilting it

TODO
----
* Better documentation
* Support for multiple clients and joysticks
* Create separate repositories for lib.websocket.WebSocketRpcHandler and lib.vjoy.*
* Write a native wrapper to be able to keep the phone awake and prevent it from changing orientation
