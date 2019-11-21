const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });

	
var connections = {}

function sendAll( group ){
    var wsarray = connections[group];
    var wsarray2 = [];
    var x = JSON.stringify( data);
    for (var i=0; i< wsarray.length; i++){
        var ws = wsarray[i];
        try{
           ws.send( x );
            //console.log( x );
        }catch(e){continue;}
        wsarray2.push(ws);    
    }
    connections[group] = wsarray2;
}

wss.on('connection', function connection(ws) {
    ws.on('message', function incoming(message) {
        data = JSON.parse( message);
        group = data.group;
        wsarray = connections[group];
        if (! wsarray){
            wsarray = connections[group] = [];
        }
        if (wsarray.indexOf(ws) <0){
            wsarray.push(ws);
        }
        sendAll( group );
     });  
});


