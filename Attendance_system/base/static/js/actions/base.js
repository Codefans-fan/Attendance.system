/**
 * create by :fky 
 * create date: 2016-01-26
 */

//base
function show_table_list(){
	var src = $("#attend_viewer").attr("src");
	var patt=new RegExp("id=(.+)");
	var uid =patt.exec(src);
	if(uid != null){
		$("#attend_viewer").attr("src",uid[0]);
	}
}

function show_calendar(){
	var src = $("#attend_viewer").attr("src");
	var patt=new RegExp("id=(.+)");
	var uid =patt.exec(src);
	if(uid != null){
		//calendar don't show all 
		if(!isNaN(uid[1])){
			$("#attend_viewer").attr("src","type=1&"+uid[0]);
		}else{
			alert("calendar is not support for all list.");
		}
	}
}

function show_charts(){
	var src = $("#attend_viewer").attr("src");
	var patt=new RegExp("id=(.+)");
	var uid =patt.exec(src);
	if(uid != null){
		$("#attend_viewer").attr("src","type=2&"+uid[0]);
	}
}


// attend app
function attend_show_table_list(userid){
	$("#attend_viewer").attr("src","id="+userid);
}


