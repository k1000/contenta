(function($) {
	$(document).ready(function() {
		/// preview
		$(".module.aligned").first().next().before("<div id='preview'></div>");
		function get_preview(){
			var url = $('#id_translation_from option:selected').html();
			$.getJSON("/json" + url, function(data) {
				var page = data[0];
				$("#preview").html("<h1>" + page.fields.title + "</h1><div>" + page.content_rndr + "</div>" );
			});
		}
		get_preview();
		$("#id_translation_from").change(function(){
			get_preview();
		});

		/// preview
		$("#id_parent").next().after("<div id='show_parent_link'></div>");
		function show_parent_link(){
			var url = $('#id_parent option:selected').html();
			$("#show_parent_link").html("Parent url: <a href='"+ url + "' target='blank'>" + url + "</a>" );
		}
		show_parent_link();
		$("#id_parent").change(function(){
			show_parent_link();
		});

		// CKEDITOR
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