


	// graphics variables 
 
var gCanvas = null; 
var ctx = null;
var div;

var mae =   {e: 10, x:5, y:6};
var filho = {e: 10, x:6, y:5};

var pop = [mae, filho];

	//size variables

var w, h;
var L = 15     	
var DX = 20;
w = h = L*DX;

var see = DX * 3;
var WALL =0;
		
var div, gCanvas, emae, efilho, afilho;

function inbounds( a ){ 
	if (a <0) return 0; 
	if (a>=L) return L-1; 
	return a;
 }
function rnd_int( X){	return Math.floor(Math.random() * X);  }
function rnd_item(a){ return a[ rnd_int( a.length )]} ;
function coin ( P){	return Math.random() < (P || 0.5);	}

function dist( a, b ){
	var dx = Math.abs( a.x - b.x);
	var dy = Math.abs( a.y - b.y);

	return Math.max( dx, dy) ;
}
function create_food(){
	return { e: rnd_int(5),
		 x: rnd_int( L), 
		 y: rnd_int( L) 	 
		};
}
function init() {

      gCanvas = $("#canvas")[0];		
  
      afilho = $("#afilho")[0];

//	console.log( gCanvas );
//	console.log( afilho );

      gCanvas.style.width = w + "px";
      gCanvas.style.height = h + "px";
      gCanvas.width = w;
      gCanvas.height = h;
      ctx = gCanvas.getContext("2d");   

	
	
		// place 3 initial positions

	for (var i=0; i< 3; i++){
		pop.push(   create_food() );
	}
	draw();

	function f( ev ) {
		//console.log(ev.which)
		switch ( ev.which ) {
			case 37: mae.x--;	break;
			case 38: mae.y--;	break;
			case 39: mae.x++;	break;
			case 40: mae.y++;	break;	
		}
		
		mae.x = inbounds( mae.x );
		mae.y = inbounds( mae.y );
		draw();
	}
	$('body'). keydown( 'keydown', f);
	

	setInterval(fstep , 10000 );
}



function draw(){
	ctx.clearRect(0, 0, w, h);
	var size = DX - 1;

	var light_red =  'rgb(256,192,192)'
	var light_blue = 'rgb(192,192,256)'
	var light_gray = 'rgb(192,192,192)';	
	var light_green = 'rgb(128,256,128)';
	var lighter_gray = 'rgb(202,202,202)';

	
	for (var i=2; i< pop.length; i++){
		var item = pop[i];
		if ( dist(item, mae  ) ==0) { 
			give( item, mae, item.e); pop[i] = item = create_food(); 
		}
		if ( dist(item, filho) ==0) { 
			give( item, filho, item.e); pop[i] = item = create_food();
		 }	
	}
		
	


	for (var i=0; i< pop.length; i++) {
		var item = pop[i];
		
			// points 50% red, 50% blue, first N_FOOD = green

				


					ctx.fillStyle = light_green;
		if ( item == mae )	ctx.fillStyle = light_red;	
		if ( item == filho)	ctx.fillStyle = light_blue;	
		if ( i >=2)		ctx.fillStyle = light_gray;
					
		var exibe =  $("#chkExibe")[0].checked;	
		if (exibe || (item == mae) || (dist(mae, item)<=3) ) {
			ctx.fillRect(item.x* DX, item.y*DX, size, size);	//draw it

			ctx.font = Math.floor(DX/2) + "px Verdana";
			ctx.fillStyle = false ? "black" : "white";
			if (item.e==0 && i<2)
				ctx.fillStyle = "red";
			ctx.fillText( item.e , item.x*DX +DX/10, item.y*DX+DX*0.6 );
		}

		if (item==mae)			//draw visual field
		{	
			ctx.strokeStyle = lighter_gray;
			ctx.strokeRect( item.x*DX-see, item.y*DX-see, see*2+ DX, see*2 + DX);	
		}
	}
}

function fstep(){
	var x = filho.x; var y = filho.y;

	x += rnd_int(3)-1;
	y += rnd_int(3)-1;
	/*
	if (filho.x > mae.x) if (coin(0.5)) x--;
	if (filho.x < mae.x) if (coin(0.5)) x++; 
	if (filho.y > mae.y) if (coin(0.5)) y--; 
	if (filho.y < mae.y) if (coin(0.5)) y++; 
	*/
	
	filho.x = inbounds( x );
	filho.y = inbounds( y );
	draw();

	if (dist( mae,filho) <= 3 ){
		if (Math.random() < 0.5) {
			afilho.innerHTML = "> "+ texto();
		} 	
		else if (Math.random() < 0.3) {
			var de = rnd_int(7)-3;	
			give( filho, mae, de );
			afilho.innerHTML = "give " + de;
			draw();	
		}
	}	
	if (coin(0.06)) { mae.e--;    check_e( mae ); }
	if (coin(0.06)) { filho.e--;  check_e(filho); }
}
function texto(){
	var txt = ""
	while( coin(0.7) ){
		txt = txt + ' '+ rnd_item( words );
	}
	return txt;
}
function givep(x){
	var de = x*$('#de')[0].value;
	if ( isNaN(de) ) return;	
	if (dist( mae,filho) <= 3 )
		give( mae, filho, de);
	draw();	
}

function check_e(a){
	a.e = Math.max(a.e, 0);
	a.e = Math.min(a.e, 20);
}

function give( a, b, e){
	if (a.e < e) return;
	if (e > 0)	a.e -= e;
	b.e += e;
	
	check_e( a );
	check_e( b );	
}

function step(){
		
}

function movebt(ch){
	switch ( ch ) {
		case 'left': 	mae.x--;	break;
		case 'up': 	mae.y--;	break;
		case 'right': 	mae.x++;	break;
		case 'down': 	mae.y++;	break;	
	}
		
	mae.x = inbounds( mae.x );
	mae.y = inbounds( mae.y );
	draw();

}
