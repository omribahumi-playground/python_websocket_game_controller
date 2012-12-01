#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import json
import types
import traceback
from tornado import websocket

class WebSocketRpcHandler(websocket.WebSocketHandler):
    @staticmethod
    def expose(func):
        func.exposed = True
        return func
    
    def on_message(self, message):
        print message
        
        try:
            data = json.loads(message)
            if not 'method' in data:
                msg = 'No method specified in message %r' % (message,)
                print msg
                self.write_message(json.dumps({'error' : msg}))
            elif not hasattr(self, data['method']):
                msg = 'No such method %s' % (data['method'],)
                print msg
                self.write_message(json.dumps({'error' : msg}))
            elif not hasattr(getattr(self, data['method']), 'exposed'):
                msg = 'Method %s not exposed to the websocket' % (data['method'],)
                print msg
                self.write_message(json.dumps({'error' : msg}))
            else:
                method = getattr(self, data['method'])
                args = data['args'] if 'args' in data else []
                kwargs = data['kwargs'] if 'kwargs' in data else {}
                
                return_value = method(*args, **kwargs)
                
                self.write_message(json.dumps({'return_value' : return_value}))
        except Exception, ex:
            # we have to return a reply on all messages to prevent callback queue from stacking up on the client
            self.write_message(json.dumps({'exception' : str(ex)}))
            traceback.print_exc()

__all__ = ['WebSocketRpcHandler']
