
$(document).ready(function() {
	function getposts() {
	$.get("/twoposts", function(data) {
	    $("#leftpost").html(data['leftpost']['text']);
	    $("#leftpost").data("id", data['leftpost']['postid']);
	    $("#rightpost").html(data['rightpost']['text']);
	    $("#rightpost").data("id", data['rightpost']['postid']);
	}, "json");
	};
	getposts();
	$(document).keydown(function(event) {
		var winner;
		if(event.which == 37) {
			winner = "left";
		} else if (event.which == 39) {
			winner = "right";
		} else if (event.which == 38 || event.which == 40) {
			winner = "draw";
		} else {
			return false;
		}
		$.ajax({
		    type: "POST",
		    url: "/mash",
		    data: JSON.stringify({leftid:$("#leftpost").data("id"),rightid:$("#rightpost").data("id"),winner:winner}),
		    contentType: "application/json; charset=utf-8",
		    dataType: "json"
		});
		getposts();
	});
});
