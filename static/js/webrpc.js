/*
 * WebRpc implementation for the python_websocket_game_controller project
 * (http://github.com/omribahumi/)
 * Uses websockets for the RPC transport protocol with fallback to AJAX POST
 * calls.
 *
 * TODO: Replace jQuery with regular browser XHR. Make this code look better.
 */

function WebRpc(wsurl, posturl){
	// websocket callbacks override "this" variable with the websocket, we'll
	// keep it in the "owner" variable.
	var owner = this;
	
	this.callbacks = [];
	
	if (window.WebSocket != undefined)
	{
		this.ws = new WebSocket(wsurl);
		this.posturl = null;
	}
	else
	{
		this.ws = null;
		this.posturl = posturl;
		// delay the execution of this function until everything is finished
		setTimeout(function(){
			owner._onopen.call(owner);
		}, 0);
	}
	
	this._onopen = function(){
		if (this.onopen != undefined)
		{
			this.onopen.call(this);
		}
	};
	
	this._onclose = function(){
		if (this.onclose != undefined)
		{
			this.onclose.call(this);
		}
	};
	
	this._onmessage = function(message){
		var callback = owner.callbacks.shift();
		var reply = JSON.parse(message.data);
		if ('error' in reply)
		{
			console.log('Error occured while trying to execute a ' +
				'WebsocketRpc call: ' + reply.error);
		}
		else if ('exception' in reply)
		{
			console.log('An exception occured while trying to execute ' +
				'a WebsocketRpc call: ' + reply.exception);
		}
		else if (callback != null)
		{
			callback.call(this, reply.return_value);
		}
	};
	
	if (this.ws)
	{
		this.ws.onopen = function(){
			owner._onopen.call(owner);
		};
		this.ws.onclose = function(){
			owner._onclose.call(owner);
		};
		this.ws.onmessage = function(message){
			owner._onmessage.call(owner, message);
		};
	}
	
	this.call = function(function_name, function_args, function_kwargs,
	callback){
		// we're pushing the callback anyways, if it's null the
		// handle_message will discard it
		this.callbacks.push(callback);
		
		if (this.ws)
		{
			this.ws.send(JSON.stringify({
				method: function_name,
				args: function_args,
				kwargs: function_kwargs
			}));
		}
		else
		{
			jQuery.post(
				this.posturl,
				JSON.stringify({
					method: function_name,
					args: function_args,
					kwargs: function_kwargs
				}),
				function(data){
					owner._onmessage.call(owner, data);
				}
			);
		}
	};
};