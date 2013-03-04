(function($) {
	$(document).ready(function() {
		/// preview
		$(".module.aligned").first().next().before("<div id='preview'></div>");
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

		// show_parent_link
		$("#id_parent").next().after("<div id='show_parent_link'></div>");
		function show_parent_link(){
			var url = $('#id_parent option:selected').html();
			$("#show_parent_link").html("Parent url: <a href='"+ url + "' target='blank'>" + url + "</a>" );
		}
		show_parent_link();
		$("#id_parent").change(function(){
			show_parent_link();
		});

		// service desription
		function set_desc(that){
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
			return that
		}
		$(".field-service select").change(function(){
			set_desc($(this));
		}).each( function(){ 
		    set_desc($(this));
		});

		// CKEDITOR
		function set_editor(){
			return CKEDITOR.replace("id_content");
		}

		if (CKEDITOR) {
			var editor;
			CKEDITOR.config.filebrowserBrowseUrl = '/admin/filebrowser/browse?pop=3';
			CKEDITOR.config.protectedSource.push( /'"/g );   // quotes for django tags
			CKEDITOR.config.entities = false;
			var render = $("#id_render_with");
			if (render.val() == "1"){
				editor = set_editor();
			}
			
			render.change( function(){
				if ($(this).val() == "1"){
					if (editor){
						$("#cke_id_content").show();
						$("#id_content").hide();
					} else {
						editor = set_editor();
					}
				} else {
					$("#id_content").show().css('visibility', 'visible');
					$("#cke_id_content").hide();
				}
			});
		}
	});
})(django.jQuery);