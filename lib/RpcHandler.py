#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

"""
    This module enables us to serve an RPC interface for JavaScript/HTML5
    clients on a tornado server instance.
    
    I encountered a problem developing this module, seems like I can't serve
    a WebSocket and POST calls with the same class, so I created two
    interfaces: one that subclasses WebSocketHandler and one that subclasses
    RequestHandler.
    
    The RPC exposed object needs to subclass RpcHandler and to be wrapped with
    one or more of the WebSocketRpcHandler and PostRpcHandler classes.
    However, it can't subclass both at the same time. Because of that fact,
    I created a wrapping function that wraps the class within another class 
    (see RpcHandlerWrapper class), so you can create copies of the RpcHandler
    class wrapped with both (or any other to come in the future) easily.
    
    Example:
    import tornado
    
    class MyRpcHandler(RpcHandler):
        @RpcHandler.expose
        def sum(self, a, b):
            return a + b
    
    application = tornado.web.Application([
        (r"/websocket", WebSocketRpcHandler.wrap(MyRpcHandler)),
        (r"/post", PostRpcHandler.wrap(MyRpcHandler))
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
"""

import json
import types
import traceback
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler

class RpcHandlerWrapper(object):
    """Subclass this class to make your class a wrapping class"""
    
    @classmethod
    def wrap(cls, wrapped):
        """Use this function to wrap a RpcHandler class with another class."""
        if cls == RpcHandlerWrapper:
            raise Exception(
                "Method should only be called on a subclasses of " +
                cls.__class__.__name__)
        if not issubclass(wrapped, RpcHandler):
            raise Exception("Argument wrapped must be a subclass " +
                "of RpcHandler")

        class WrappedRpcHandlerClass(cls):
            def __init__(self, *args, **kwargs):
                cls.__init__(self, wrapped, *args, **kwargs)
        
        return WrappedRpcHandlerClass

class WebSocketRpcHandler(WebSocketHandler, RpcHandlerWrapper):
    def __init__(self, rpc_handler, *args, **kwargs):
        if not issubclass(rpc_handler, RpcHandler):
            raise Exception("Argument rpc_handler must be a subclass of " +
                "RpcHandler")
        self.rpc_handler = rpc_handler()
        WebSocketHandler.__init__(self, *args, **kwargs)
    
    def initialize(self, *args, **kwargs):
        self.rpc_handler.initialize(*args, **kwargs)
    
    def on_message(self, message):
        self.write_message(json.dumps(self.rpc_handler.dispatch(message)))

class PostRpcHandler(RequestHandler, RpcHandlerWrapper):
    def __init__(self, rpc_handler, *args, **kwargs):
        if not issubclass(rpc_handler, RpcHandler):
            raise Exception("Argument rpc_handler must be a subclass of " +
                "RpcHandler")
        self.rpc_handler = rpc_handler()
        RequestHandler.__init__(self, *args, **kwargs)

    def initialize(self, *args, **kwargs):
        self.rpc_handler.initialize(*args, **kwargs)
    
    def post(self):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(self.rpc_handler.dispatch(self.request.body)))

class RpcHandler(object):
    @staticmethod
    def expose(func):
        func.exposed = True
        return func
    
    def dispatch(self, message):
        print message
        
        try:
            data = json.loads(message)
            if not 'method' in data:
                msg = 'No method specified in message %r' % (message,)
                print msg
                return {'error' : msg}
            elif not hasattr(self, data['method']):
                msg = 'No such method %s' % (data['method'],)
                print msg
                return {'error' : msg}
            elif not hasattr(getattr(self, data['method']), 'exposed'):
                msg = 'Method %s not exposed to the websocket' % \
                    (data['method'],)
                print msg
                return {'error' : msg}
            else:
                method = getattr(self, data['method'])
                args = data['args'] if 'args' in data else []
                kwargs = data['kwargs'] if 'kwargs' in data else {}
                
                return_value = method(*args, **kwargs)
                
                return {'return_value' : return_value}
        except Exception, ex:
            traceback.print_exc()
            
            # we have to return a reply for all messages to prevent callback
            # queue from stacking up on the client
            return {'exception' : str(ex)}

__all__ = ['WebSocketRpcHandler', 'PostRpcHandler', 'RpcHandler']
