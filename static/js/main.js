$(document).ready(function(){
	var wsrpc = new WebsocketRpc("ws://" + window.location.host +  "/joystick/1");
	
	wsrpc.onopen = function(){
		$('.joybutton').click(function(){
			var id = parseInt($(this).attr('data-id'));
			wsrpc.call('button', [id, true], {}, null);
			setTimeout(function(){
				wsrpc.call('button', [id, false], {}, null);
			}, 250);
		});
		
		var oldX = 0, oldY = 0;
		
		window.ondevicemotion = function(event) {
			var x = Math.round(event.accelerationIncludingGravity.x);
			var y = Math.round(event.accelerationIncludingGravity.y);

			if (x != oldX)
			{
				oldX = x;
				wsrpc.call('axe', ['X', x*-1], {}, null);
			}
			if (y != oldY)
			{
				oldY = y;
				wsrpc.call('axe', ['Y', y], {}, null);
			}
		};
	};
});
