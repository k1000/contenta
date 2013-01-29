/*
# CKEDITOR Edit-In Place jQuery Plugin.
# Created By Dave Earley.
# www.Dave-Earley.com
*/

/* modded by earthchie.com */
$(function(){
	$('.editable').each(function(){
		var id = $(this).attr('id');
		if(id == undefined || id == ''){
			id = 'content_'+Math.floor(Math.random() * 99999999);
			$(this).attr('id',id);
		}
		
		// default
		$('#'+id+'.editable:not(.simple,.full)').ckeip({
			e_url: $(this).data('handler'), // action file which handle $_POST['content']
			ckeditor_config : {
				width:'100%',
				toolbar:
				[
					['Bold','Italic','Underline','Strike','Subscript','Superscript'],
					['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
					['NumberedList','BulletedList'],
					['TextColor','BGColor' ],
					['RemoveFormat' ],'/',
					[ 'Format','Font','FontSize' ],
					['Outdent','Indent'],
					[ 'Link','Unlink','-','ShowBlocks'],'/',
					['NewPage'],
					['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar' ],
					['Cut','Copy','Paste','PasteText','PasteFromWord'],
					['Undo','Redo','-','Source','-','Maximize']
				],
			}
		});
		
		$('#'+id+'.full.editable').ckeip({
			e_url: $(this).data('handler'), // action file which handle $_POST['content']
			ckeditor_config : {
				width:'100%'
			}
		});
		
		$('#'+id+'.simple.editable').ckeip({
			e_url: $(this).data('handler'), // action file which handle $_POST['content']
			ckeditor_config : {
				width:'100%',
				toolbar:
				[
					['Bold','Italic','Underline'],
					['Maximize']
				]
			}
		});
		
	});
});

$.fn.ckeip = function (options, callback) {
    var original_html = $(this);
    var defaults = {
        e_height: '10',
        data: {},
		e_url: '',
        e_hover_color: '#eeeeee',
        ckeditor_config: '',
        e_width: '50',
		e_add_text: '<i>Double click to add text...</i>'
    };
    var settings = $.extend({}, defaults, options);

    return this.each(function () {
        var eip_html = $(this).html();
		eip_html = eip_html.replace(settings.e_add_text,'');
		var u_id = Math.floor(Math.random() * 99999999);

        $(this).before("<div id='ckeip_" + u_id + "'  style='display:none;'><textarea id ='ckeip_e_" + u_id + "' cols='" + settings.e_width + "' rows='" + settings.e_height + "'  >" + eip_html + "</textarea><input type='button' value='Save' id='save_ckeip_" + u_id + "' /> <input type='button' value='Cancel' id='cancel_ckeip_" + u_id + "' /></div>");

        var editor = CKEDITOR.replace('ckeip_e_' + u_id + '');
        //$('#ckeip_e_' + u_id + '').ckeditor(settings.ckeditor_config);

        $(this).bind("dblclick", function () {

            $(this).hide();
            $('#ckeip_' + u_id + '').show();

        });

        $(this).hover(function () {
            $(this).css({
                backgroundColor: settings.e_hover_color
            });
        }, function () {
            $(this).css({
                backgroundColor: ''
            });
        });


        $("#cancel_ckeip_" + u_id + "").click(function () {
            $('#ckeip_' + u_id + '').hide();
            $(original_html).html(editor.getData());
            $(original_html).fadeIn();
            return false;
        });

        $("#save_ckeip_" + u_id + "").click(function () {
            var ckeip_html = editor.getData();
			if(ckeip_html === ""){
				ckeip_html = '<i>'+settings.e_add_text+'</i>';
			}
            $.post("/save" + location.pathname, {
                content: ckeip_html,
                data: settings.data
            }, function (response) {
                if (typeof callback == "function") callback(response);

                $(original_html).html(ckeip_html);
                $('#ckeip_' + u_id + '').hide();
                $(original_html).fadeIn();

            });
            return false;

        });

    });
};