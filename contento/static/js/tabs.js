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

		var editors = [];
		function set_editor(){
			$("textarea").each(function(n, obj) {
				if (obj.id.match(/content/)) {
					CKEDITOR.replace(obj.id);
					editors.push(obj);
					// fck.BasePath = "/static/fckeditor/" ;
					//fck.ReplaceTextarea() ;
				}
			});
		}

		$(".field-service select").change(function(){
			var that = $(this);
			var service_name = that.val();
			if (service_name !== null){
				var serv_desc = window.service_descriptions[service_name];
				var serv_default = window.service_defaults[service_name];
				var next = that.next();
				if (next.length > 0){
					next.html("<p>"+serv_desc+"</p>");
				} else {
					that.after("<p>"+serv_desc+"</p>");
				}
			}
		});

		if (CKEDITOR) {
			// Added by Roger Hu 02/27/2010
			CKEDITOR.config.filebrowserBrowseUrl = '/admin/filebrowser/browse?pop=3';
			var render = $("#id_render_with");
			if (render.val() == "1"){
				set_editor();
			}

			render.change( function(){
				if ($(this).val() == "1"){
					set_editor();
				} else {
					for (var i = editors.length - 1; i >= 0; i--) {
						CKEDITOR.remove(editors[i]);
					}
				}
			});
		}
	});
})(django.jQuery);