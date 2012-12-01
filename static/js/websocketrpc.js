function WebsocketRpc(url){
	this.callbacks = [];
	
	this.ws = new WebSocket(url);
	
	// websocket callbacks override "this" variable, we'll keep it on the "owner" variable.
	var owner = this;
	
	this.ws.onopen = function(){
		if (owner.onopen != undefined)
		{
			owner.onopen.call(this);
		}
	};
	this.ws.onclose = function(){
		if (this.onclose != undefined)
		{
			this.onclose.call(this);
		}
	};
	this.ws.onmessage = function(message){
		var callback = owner.callbacks.shift();
		var reply = JSON.parse(message.data);
		if ('error' in reply)
		{
			console.log('Error occured while trying to execute a WebsocketRpc call: ' + reply.error);
		}
		else if ('exception' in reply)
		{
			console.log('An exception occured while trying to execute a WebsocketRpc call: ' + reply.exception);
		}
		else if (callback != null)
		{
			callback(reply.return_value);
		}
	};
	
	this.call = function(function_name, function_args, function_kwargs, callback){
		// we're pushing the callback anyways, if it's null the handle_message will discard it
		this.callbacks.push(callback);
		
		this.ws.send(JSON.stringify({
			method: function_name,
			args: function_args,
			kwargs: function_kwargs
		}));
	};
};