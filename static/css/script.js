$(document).ready(function() {
	// initialize page, selecting Shorten Link tab
	$('#tabs a[href="#linkShortTab"]').tab('show');

	var x=document.getElementById("geolocation");
	$('#geolocationButton').click( function getLocation() {
  		if (navigator.geolocation) {
    			navigator.geolocation.getCurrentPosition(showPosition);
  		}
  		else {
      			x.innerHTML="Geolocation is not supported by this browser.";}

		function showPosition(position) {
  		x.innerHTML="Latitude: " + position.coords.latitude + "<br>Longitude: " + position.coords.longitude;  
		console.log(position);
		}
	});

	$(window).load(function() {

		navigator.geolocation.getCurrentPosition(appendGeo);

		function appendGeo(loc) {
			$('.lat').prop("value",loc.coords.latitude);
			$('.long').prop("value",loc.coords.longitude);
		}
	}); 

/*
	var node = document.getElementById('column1');
	node.ontouchmove = function(e){
  		if(e.touches.length == 1){ // Only deal with one finger
    		var touch = e.touches[0]; // Get the information for finger #1
    		var node = touch.target; // Find the node the drag started from
    		node.style.position = "absolute";
    		node.style.left = touch.pageX + "px";
    		node.style.top = touch.pageY + "px";
  		}
	}
*/

	//touch color change column1
	var column1 = document.getElementById('column1');
	var clicksColumn1 = 0;
	column1.addEventListener('touchstart', function(event) {	
	
		if ( clicksColumn1%2 === 0 ) { 
			column1.style.backgroundColor ='#555555';
		}
		else {
                	column1.style.backgroundColor ='black';
		}		
		clicksColumn1++;	
	});

	// touch color change column2
        var column2 = document.getElementById('column2');
        var column2kids = column2.childNodes;
	var clicksColumn2 = 0;
        column2.addEventListener('touchstart', function(event) {
        	if ( clicksColumn2%2 === 0 ) {
                        column2.style.backgroundColor ='#555555';
                        column2kids[1].style.color ='white';
                }
                else {
                        column2.style.backgroundColor ='black';
                        column2kids[1].style.color ='red';
                }
                clicksColumn2++; 
        });

	// touch color change column3
        var column3 = document.getElementById('column3');
	var clicksColumn3 = 0;
        column3.addEventListener('touchstart', function(event) {
		if ( clicksColumn3%2 === 0 ) {
                        column3.style.backgroundColor ='#555555';
                }
                else {
                        column3.style.backgroundColor ='black';
                }
                clicksColumn3++;            
        });	

	// Column movement is buggy in portrait viewing!!
	column1.ontouchmove = function(event) {
                var touch = event.touches[0];
		var window_width = $(window).width();
		column1.style.left = touch.pageX-125 + "px";
		column1.style.position = "absolute";

		column2.style.position = "";
		column3.style.position = "";

		if ( touch.pageX+125 < window_width/3 ) { 
                column2.style.float = "right";
		column3.style.float = "right";
		}
		
		if ( touch.pageX+125 > window_width/3 && touch.pageX+125 < window_width*(2/3) ) {
		column2.style.float = "left";
		column3.style.float = "right";
		}
		
		if ( touch.pageX+125 > window_width*(2/3) ) {       
                column2.style.float = "left";
                column3.style.float = "left";
                }
        }

        column2.ontouchmove = function(event) {
                var touch = event.touches[0];
                var window_width = $(window).width();
                column2.style.left = touch.pageX-125 + "px";
                column2.style.position = "absolute";

                column1.style.position = "";
                column3.style.position = "";

                if ( touch.pageX+125 < window_width/3 ) {
                column1.style.float = "right";
                column3.style.float = "right";
                }
                                                                
                if ( touch.pageX+125 > window_width/3 && touch.pageX+125 < window_width*(2/3) ) {
                column1.style.float = "left";
                column3.style.float = "right";
                }
                
                if ( touch.pageX+125 > window_width*(2/3) ) {                            
                column1.style.float = "left";
                column3.style.float = "left";
                }
        }

        column3.ontouchmove = function(event) {
                var touch = event.touches[0];
                var window_width = $(window).width();
                column3.style.left = touch.pageX-125 + "px";
                column3.style.position = "absolute";

                column1.style.position = "";
                column2.style.position = "";

                if ( touch.pageX+125 < window_width/3 ) {
                column1.style.float = "right";
                column2.style.float = "right";
                }
                                                                
                if ( touch.pageX+125 > window_width/3 && touch.pageX+125 < window_width*(2/3) ) {
                column1.style.float = "left";
                column2.style.float = "right";
                }
                
                if ( touch.pageX+125 > window_width*(2/3) ) {                            
                column1.style.float = "left";
                column2.style.float = "left";
                }
        }

	// Prevent scrolling
	document.body.addEventListener('touchmove', function(event) {
  	event.preventDefault();
	}, false); 

	// tab click animation for #linkShortTab
	$('#tabs a[href="#linkShortTab"]').click(function (e) {
  		e.preventDefault();
  		$(this).tab('show');
  		$('#shortDeleteTab').hide();
  		$('#linkShortAutoTab').hide();
  		$('#listShortsTab').hide();
  		$('#linkShortTab').show();
	});
	
	// tab click animation for #shortDeleteTab
	$('#tabs a[href="#shortDeleteTab"]').click(function (e) {
  		e.preventDefault();
  		$(this).tab('show');
  		$('#linkShortTab').hide();
  		$('#linkShortAutoTab').hide();
  		$('#listShortsTab').hide();
  		$('#shortDeleteTab').show();
	});
	
	// #linkShortAutoTab
	$('#tabs a[href="#linkShortAutoTab"]').click(function (e) {
  		e.preventDefault();
  		$(this).tab('show');
  		$('#linkShortTab').hide();
  		$('#linkShortAutoTab').show();
  		$('#listShortsTab').hide();
  		$('#shortDeleteTab').hide();
	});
	
	// #listShortsTab
	$('#tabs a[href="#listShortsTab"]').click(function (e) {
  		e.preventDefault();
  		$(this).tab('show');
  		$('#linkShortTab').hide();
  		$('#linkShortAutoTab').hide();
  		$('#listShortsTab').show();
  		$('#shortDeleteTab').hide();
	});
	
	// Short Input Validation
	$('#short').keyup( function() {
		var short = this.value;
		if ( /^[a-z]+$/i.test(short) || short === "" ) {
		$('#errorAlertShort').hide();
		$('#submitLink').prop("disabled","");	
    	} else { 
    	$('#errorAlertShort').show();
    	$('#submitLink').prop("disabled","disabled");
    	}
	});
	
	// Link Shorten Form Submission Handler
	$('#submitForm').submit(function() {
  	console.log($(this).serialize());
  	
  	$.post("/~arenold/server/create", $(this).serialize(), function(data) {
  		updatePage(data) }, "json");
  	
  	return false;
  	});
  	
  	$('#shortDel').keyup( function() {
		var short = this.value;
		$('#submitDel').prop("disabled","");
	});
  	
  	// Delete Short Form Submission Handler
  	$('#deleteShort').submit(function() {
  	var shortDel = $('#shortDel').val();
  	$.ajax({
  		url: "/~arenold/server/"+shortDel,
  		type: "DELETE"
  		});
  	return false;
  	});
  	
  	// Initialize Automatic Short
  	$('#shortAuto').prop("value",createShort);
  	  	
  	// Link Shorten With No Short Submission Handler
	$('#submitURLForm').submit(function() {
  	$.post("/~arenold/server/create", $(this).serialize(), function(data) {
  		updatePage(data) }, "json");
  	
  	return false;
  	});
  	
  	//List Shorts GET request
  	$.get('/~arenold/server/123456789a', function(data) {
  	console.log(data);
  	updateListShorts(data);
	});

	//Trending Urls GET request
	$.get('/~arenold/server/trending_urls', function(data) {
	console.log(data);
	updateTrendingUrls(data);
  	});
});

// Function to update page after Link Shorten Form Submission
function updatePage(data) {
	$('#modalHead').html("Your Link for "+data['short']);
	$('#shortLink').prop("href",data['link'].toString());
	$('#shortLink').html(data['link']);
	$('#linkModal').modal('show');
}

function updateTrendingUrls(data) {
	for (var i = 0; i < data.trending_urls.length; i++ ) {
        console.log(data.trending_urls[i]['url'])
	$('#trendingUrls').append("<tr><td><a href='/~arenold/server/"+data.trending_urls[i]['short']+"'>"+data.trending_urls[i]['url']+"</a></td><td>"+data.trending_urls[i]['clicks']+"</td></tr>");
	}
}

function updateListShorts(data) {
	for (var i = 0; i < data.db.length; i++) {
   	 //console.log(data.db[i][0]);
   	 //console.log(data.db[i][1]);
   	 //console.log(data.clicks[i][1]);
   	 var short = data.db[i][0];
   	 var url = data.db[i][1];
   	 var clickNum = data.clicks[i][1];
   	 $('#listShorts').append("<tr><td>"+short+"</td><td>"+url+"</td><td>"+clickNum+"</td></tr>");
	}
}

function createShort() {
	
	var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 8; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}
