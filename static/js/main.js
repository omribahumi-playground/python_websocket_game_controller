var Point = function (x, y)
{
	this.x = x;
	this.y = y;
}

Point.prototype = {
	set: function(x, y){
		this.x = x;
		this.y = y;
	},
	copy: function(){
		return new Point(this.x, this.y);
	},
	sub: function(other){
		this.x -= other.x;
		this.y -= other.y;
	},
	add: function(other){
		this.x += other.x;
		this.y += other.y;
	}
};

function canvasDrawCircle(context, x, y, lineWidth, strokeStyle, radius)
{
	context.beginPath();
	context.lineWidth = lineWidth;
	context.strokeStyle = strokeStyle;
	context.arc(x, y, radius, 0, Math.PI*2, true);
	context.stroke();
}

$(document).ready(function(){
	var leftTouchId = -1, rightTouchId = -1;
	var leftPointBegin = new Point(0, 0);
	var canvas = document.getElementById('joycanvas');
	var context = canvas.getContext('2d');

	window.onorientationchange = window.onresize = function(){
		canvas.width = window.innerWidth;
		canvas.height = window.innerHeight;
	};
	window.onresize();
	
	var wsrpc = new WebRpc(
		"ws://" + window.location.host + "/websocket/joystick/1",
		"/post/joystick/1"
	);
	
	var oldX = 0, oldY = 0;
	
	wsrpc.onopen = function(){
		canvas.addEventListener('touchstart', function(e){
			e.preventDefault();
			
			for (var i=0; i < e.changedTouches.length; i++)
			{
				var touch = e.changedTouches[i]; 
				if (leftTouchId == -1 && touch.clientX < this.width/2)
				{
					leftTouchId = touch.identifier;
					leftPointBegin.set(touch.clientX, touch.clientY);
					canvasDrawCircle(context, leftPointBegin.x,
						leftPointBegin.y, 6, "cyan", 40);
					canvasDrawCircle(context, leftPointBegin.x,
						leftPointBegin.y, 2, "cyan", 60);
				}
				else if (rightTouchId == -1 && touch.clientX > this.width/2)
				{
					rightTouchId = touch.identifier;
					wsrpc.call('button', [1, true], {}, null);
				}
			}
		});
		
		
		canvas.addEventListener('touchmove', function(e){
			e.preventDefault();
			
			for (var i=0; i < e.changedTouches.length; i++)
			{
				var touch = e.changedTouches[i];
				if (touch.identifier == leftTouchId)
				{
					context.clearRect(0, 0, canvas.width, canvas.height);
					var leftPointCurrent = new Point(touch.clientX,
						touch.clientY);
					canvasDrawCircle(context, leftPointBegin.x,
						leftPointBegin.y, 6, "cyan", 40);
					canvasDrawCircle(context, leftPointBegin.x,
						leftPointBegin.y, 2, "cyan", 60);
					canvasDrawCircle(context, leftPointCurrent.x,
						leftPointCurrent.y, 2, "cyan", 60);
					leftPointCurrent.sub(leftPointBegin);
					var x = Math.max(-10,
						Math.min(10, parseInt(leftPointCurrent.x/5)));
					var y = Math.max(-10,
						Math.min(10, parseInt(leftPointCurrent.y/5)));
					if (x != oldX)
					{
						wsrpc.call('axe', ['X', x], {}, null);
						oldX = x;
					}
					if (y != oldY)
					{
						wsrpc.call('axe', ['Y', y], {}, null);
						oldY = y;
					}
					break;
				}
			}
		});
		
		canvas.addEventListener('touchend', function(e){
			e.preventDefault();
			
			for (var i=0; i < e.changedTouches.length; i++)
			{
				var touch = e.changedTouches[i];
				if (touch.identifier == leftTouchId)
				{
					context.clearRect(0, 0, canvas.width, canvas.height);
					leftTouchId = -1;
					oldX = 0, oldY = 0;
					wsrpc.call('axe', ['X', 0], {}, null);
					wsrpc.call('axe', ['Y', 0], {}, null);
				} else if (touch.identifier == rightTouchId) {
					rightTouchId = -1;
					wsrpc.call('button', [1, false], {}, null);
				}
			}
		});
	};
});
