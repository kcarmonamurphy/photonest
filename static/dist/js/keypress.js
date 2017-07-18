function initKeyboardControls() {
	var flexClasses = ['flex-1', 'flex-2', 'flex-3', 'flex-4', 'flex-5', 'flex-6', 'flex-8', 'flex-10'];

	var listener = new window.keypress.Listener();

	listener.simple_combo("shift _", function() {
	    zoomOut(flexClasses);
	});

	listener.simple_combo("shift +", function() {
	    zoomIn(flexClasses);
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
		enter();
	});

	$('input, textarea')
	    .bind("focus", function() { listener.stop_listening(); })
    	.bind("blur", function() { listener.listen(); });
}

function isGalleryOpen() {
	return ($('#photoswipe-container').css('display') == 'block')
}

function enter() {
	if (!isGalleryOpen()) {
		activeImageThumbnail = $(".gallery-image.active");
		if (activeImageThumbnail.length) {
			launchPhotoSwipe(activeImageThumbnail);
		}
		activeFolderThumbnail = $(".gallery-folder.active");
		if (activeFolderThumbnail.length) {
			window.location.href = activeFolderThumbnail.find('a').attr("href");
		}
	}
}

function selectThumbnailUp() {
	if (!isGalleryOpen()) {
		$activeThumbnail = $(".gallery-image.active, .gallery-folder.active");
		flexClass = $("#flex-container").attr("class");
		itemsPerRow = flexClass.split("-")[1];
		$upThumbnail = $activeThumbnail.prevAll().eq(itemsPerRow-1);
		if ($upThumbnail.length) {
			$upThumbnail.addClass("active");
			$activeThumbnail.removeClass("active");
			scrollIntoViewIfNeeded($upThumbnail);
			
			updateMetadataSidebar($upThumbnail);
		}
	}
}

function selectThumbnailDown() {
	if (!isGalleryOpen()) {
		$activeThumbnail = $(".gallery-image.active, .gallery-folder.active");
		flexClass = $("#flex-container").attr("class");
		itemsPerRow = flexClass.split("-")[1];
		$downThumbnail = $activeThumbnail.nextAll().eq(itemsPerRow-1)
		if ($downThumbnail.length) {
			$downThumbnail.addClass("active");
			$activeThumbnail.removeClass("active");
			scrollIntoViewIfNeeded($downThumbnail);

			updateMetadataSidebar($downThumbnail);
		}
	}
}

function selectThumbnailLeft() {
	if (isGalleryOpen()) {
		pswp.prev()
	} else {
		$activeThumbnail = $(".gallery-image.active, .gallery-folder.active");
		$leftThumbnail = $activeThumbnail.prev();
		if ($leftThumbnail.length) {
			$leftThumbnail.addClass("active");
			$activeThumbnail.removeClass("active");
			scrollIntoViewIfNeeded($leftThumbnail);

			updateMetadataSidebar($leftThumbnail);
		}
	}
}

function selectThumbnailRight() {

	if (isGalleryOpen()) {
		pswp.next()
	} else {
		$activeThumbnail = $(".gallery-image.active, .gallery-folder.active");
		$rightThumbnail = $activeThumbnail.next();
		if ($rightThumbnail.length) {
			$rightThumbnail.addClass("active");
			$activeThumbnail.removeClass("active");
			scrollIntoViewIfNeeded($rightThumbnail);

			updateMetadataSidebar($rightThumbnail);
		}
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

function zoomOut(flexClasses) {

	if (isGalleryOpen()) {
		pswp.zoomTo(pswp.getZoomLevel()/1.5, {x:pswp.viewportSize.x/2,y:pswp.viewportSize.y/2}, 50, false, function(now) {
		});
	} else {
		var flexClass = $('#flex-container').attr('class').match(/flex-*/).input
		var index = $.inArray( flexClass, flexClasses );
		if (index > -1) {
			$('#flex-container').attr('class', flexClasses[index+1]);
		}
	}
}

function zoomIn(flexClasses) {

	if (isGalleryOpen()) {
		pswp.zoomTo(pswp.getZoomLevel()*1.5, {x:pswp.viewportSize.x/2,y:pswp.viewportSize.y/2}, 50, false, function(now) {
		});
	} else {
		var flexClass = $('#flex-container').attr('class').match(/flex-*/).input
		var index = $.inArray( flexClass, flexClasses );
		if (index > -1) {
			$('#flex-container').attr('class', flexClasses[index-1]);
		}
	}
}