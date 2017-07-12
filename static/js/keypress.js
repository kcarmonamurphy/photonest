$(document).ready(function() {
	var flexClasses = ['flex-one', 'flex-two', 'flex-three', 'flex-four', 'flex-five', 'flex-six', 'flex-eight', 'flex-ten'];

	var listener = new window.keypress.Listener();

	listener.simple_combo("shift _", function() {
	    flexShrink(flexClasses);
	});

	listener.simple_combo("shift +", function() {
	    flexGrow(flexClasses);
	});

	$('input, textarea')
	    .bind("focus", function() { listener.stop_listening(); })
    	.bind("blur", function() { listener.listen(); });
});


function flexShrink(flexClasses) {
	var flexClass = $('#flex-container').attr('class').match(/flex-*/).input
	var index = $.inArray( flexClass, flexClasses );
	if (index > -1) {
		$('#flex-container').attr('class', flexClasses[index+1]);
	}
}

function flexGrow(flexClasses) {
	var flexClass = $('#flex-container').attr('class').match(/flex-*/).input
	var index = $.inArray( flexClass, flexClasses );
	if (index > -1) {
		$('#flex-container').attr('class', flexClasses[index-1]);
	}
}