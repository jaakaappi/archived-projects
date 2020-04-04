var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
   socket.emit('request_control');
   console.log('request_control');
});

socket.on('status', function(data){
   console.log(data);
});

function send_move(direction){
   socket.emit('move', direction);
}
