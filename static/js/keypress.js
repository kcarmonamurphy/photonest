function galleryKeyboardShortcuts() {
	var flexClasses = ['flex-1', 'flex-2', 'flex-3', 'flex-4', 'flex-5', 'flex-6', 'flex-8', 'flex-10'];

	var listener = new window.keypress.Listener();

	listener.simple_combo("shift _", function() {
	    flexShrink(flexClasses);
	});

	listener.simple_combo("shift +", function() {
	    flexGrow(flexClasses);
	});

	listener.simple_combo("right", function() {
		selectThumbnailRight();
	});

	listener.simple_combo("left", function() {
		selectThumbnailLeft();
	});

	listener.simple_combo("down", function() {
		selectThumbnailDown();
	});

	listener.simple_combo("up", function() {
		selectThumbnailUp();
	});

	listener.simple_combo("enter", function() {
		activeImageThumbnail = $(".gallery-image.active");
		if (activeImageThumbnail.length) {
			launchPhotoSwipe(activeImageThumbnail);
		}
		activeFolderThumbnail = $(".gallery-folder.active");
		if (activeFolderThumbnail.length) {
			window.location = activeFolderThumbnail.find('a').attr("href");
		}
	});

	$('input, textarea')
	    .bind("focus", function() { listener.stop_listening(); })
    	.bind("blur", function() { listener.listen(); });

    return listener;
}

function selectThumbnailUp() {
	activeThumbnail = $(".gallery-image.active, .gallery-folder.active");
	flexClass = $("#flex-container").attr("class");
	itemsPerRow = flexClass.split("-")[1];
	upThumbnail = activeThumbnail.prevAll().eq(itemsPerRow-1);
	if (upThumbnail.length) {
		upThumbnail.addClass("active");
		activeThumbnail.removeClass("active");
		scrollIntoViewIfNeeded(upThumbnail);
	}
}

function selectThumbnailDown() {
	activeThumbnail = $(".gallery-image.active, .gallery-folder.active");
	flexClass = $("#flex-container").attr("class");
	itemsPerRow = flexClass.split("-")[1];
	downThumbnail = activeThumbnail.nextAll().eq(itemsPerRow-1)
	if (downThumbnail.length) {
		downThumbnail.addClass("active");
		activeThumbnail.removeClass("active");
		scrollIntoViewIfNeeded(downThumbnail);
	}
}

function selectThumbnailLeft() {
	activeThumbnail = $(".gallery-image.active, .gallery-folder.active");	leftThumbnail = activeThumbnail.prev();
	if (leftThumbnail.length) {
		leftThumbnail.addClass("active");
		activeThumbnail.removeClass("active");
		scrollIntoViewIfNeeded(leftThumbnail);
	}
}

function selectThumbnailRight() {
	activeThumbnail = $(".gallery-image.active, .gallery-folder.active");
	rightThumbnail = activeThumbnail.next();
	if (rightThumbnail.length) {
		rightThumbnail.addClass("active");
		activeThumbnail.removeClass("active");
		scrollIntoViewIfNeeded(rightThumbnail);
	}
}

function scrollIntoViewIfNeeded(target) {
	padding = 40;
    img = $(target).find('img')[0];
    imgRect = img.getBoundingClientRect();
    galleryRect = document.getElementById("gallery").getBoundingClientRect();
    if (imgRect.bottom + padding > galleryRect.bottom) {
        $(img).parents(".gallery-image, .gallery-folder")[0].scrollIntoView(false);
    }
    if (imgRect.top + padding < galleryRect.top) {
        $(img).parents(".gallery-image, .gallery-folder")[0].scrollIntoView();
    } 
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