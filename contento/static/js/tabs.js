(function($) {
	$(document).ready(function() {
		var tabs = {};
		var tab_ele = "<ul class='tabs'>";
		$(".tab").each( function(){
			var tabbed = $(this);
			var h2 = tabbed.find("h2");
			var title = h2.html().trim();
			h2.remove();
			var index = ( typeof grappelli === "undefined" )? 2 : 1;
			var cls = tabbed.attr('class').split(" ")[index];
			tabs[cls] = {title: title, ele: tabbed};
			tab_ele += "<li class='"+ cls +"'><a href='#" +cls +"' >"+title+"</a></li>";
			tabbed.hide();
		});
		tab_ele += "</ul>";
		for (first in tabs) break;
		var first_tab = tabs[first];
		var current_tab = first_tab.ele;
		// current_tab.children(":first-child").addClass("active");
		first_tab.ele
			.show()
			.before(tab_ele); //.find("a").click(function(){ alert(this)});
		$(".tabs a").click(function(){
			current_tab.hide();
			$(".tabs a").removeClass("active");
			var tab_head = $(this);
			tab_head.addClass("active");
			current_tab_id = tab_head.parent().attr("class");
			current_tab = tabs[current_tab_id].ele;
			current_tab.show();
		});
		$(".tabs a:first").addClass("active");
	});
})(django.jQuery);