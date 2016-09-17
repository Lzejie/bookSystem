
	window.onload=function(){
	var me = document.getElementById("me");
	var me_list = document.getElementById("me_list");
	me.onmouseover = function(){
		me_list.style.display = "block";
	};
	me_list.onmouseover = function(){
		me_list.style.display = "block";
	};
	me.onmouseout = function(){
		me_list.style.display = "none";
	};
	me_list.onmouseout = function(){
		me_list.style.display = "none";
	};//me_list结束

	var message = document.getElementById("message");
	var message_list = document.getElementById("message_list");
	message.onmouseover = function(){
		message_list.style.display = "block";
	};
	message_list.onmouseover = function(){
		message_list.style.display = "block";
	};
	message.onmouseout = function(){
		message_list.style.display = "none";
	};
	message_list.onmouseout = function(){
		message_list.style.display = "none";
	};//message_list结束
}