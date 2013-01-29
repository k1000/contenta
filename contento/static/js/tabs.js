(function($) {
	$(document).ready(function() {

		$(".module.aligned").first().next().after("<div id='preview'></div>");
		function get_preview(){
			var url = $('#id_translation_from option:selected').html();
			$.getJSON("/json" + url, function(data) {
				var page = data[0].fields;
				$("#preview").html("<h1>" + page.title + "</h1><div>" + page.content + "</div>" );
			});
		}
		get_preview();
		$("#id_translation_from").change(function(){
			get_preview();
		});
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