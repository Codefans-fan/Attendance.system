/**
 * create by :fky 
 * create date: 2016-01-26
 */

// attend app
function attend_show_table_list(userid){
	$("#attend_table_listview").attr("src","id="+userid);
}

function attend_show_calendar(userid){
	$("#attend_table_listview").attr("src","type=1&id="+userid);
}