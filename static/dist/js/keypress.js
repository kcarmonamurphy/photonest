function galleryKeyboardShortcuts() {
	var flexClasses = ['flex-one', 'flex-two', 'flex-three', 'flex-four', 'flex-five', 'flex-six', 'flex-eight', 'flex-ten'];

	var listener = new window.keypress.Listener();

	listener.simple_combo("shift _", function() {
	    flexShrink(flexClasses);
	});

	listener.simple_combo("shift +", function() {
	    flexGrow(flexClasses);
	});

	listener.simple_combo("right", function() {
		activeGalleryImage = $(".gallery-image.active");
		if (activeGalleryImage.next().length) {
			activeGalleryImage.next().addClass("active");
			activeGalleryImage.removeClass("active");
		}
	});

	listener.simple_combo("left", function() {
		activeGalleryImage = $(".gallery-image.active");
		if (activeGalleryImage.prev().length) {
			activeGalleryImage.prev().addClass("active");
			activeGalleryImage.removeClass("active");
		}
	});

	listener.simple_combo("enter", function() {
		activeGalleryImage = $(".gallery-image.active");
		launchPhotoSwipe(activeGalleryImage);
	});

	$('input, textarea')
	    .bind("focus", function() { listener.stop_listening(); })
    	.bind("blur", function() { listener.listen(); });

    return listener;
}


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