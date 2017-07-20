$(document).ready(function() {



	// defome global jQuery objects
	$imageObjectsArray = $('.gallery-image');
	$folderObjectsArray = $('.gallery-folder');
	$galleryObjectsArray = $('.gallery-image, .gallery-folder');
	$metadataObjectsArray = $('.metadata-image, .metadata-folder');

	// highlight first thumbnail and show associated metadata
	initActiveGalleryObject();
	initKeywordChips();

	// initialize interaction controls
	initKeyboardControls();
	initClickControls();
	configureSubmit();



});

function initActiveGalleryObject() {
	$galleryObjectsArray.first().addClass('active');
	$metadataObjectsArray.first().addClass('active')
}

function initClickControls() {
	$galleryObjectsArray.find('a').click(function(e) {
		highlightActiveGalleryObject(e, this);
	});

	$imageObjectsArray.dblclick(function() {
		launchPhotoSwipe($(this));
	});

	$folderObjectsArray.dblclick(function() {
		folderURI = $(this).find('a').attr("href");
		window.location.href = folderURI;
	});

	var tapped=false
	$imageObjectsArray.on("touchstart",function(e){
	    if(!tapped){ //if tap is not set, set up single tap
	      tapped=setTimeout(function(){
	          tapped=null
	          //insert things you want to do when single tapped
	          highlightActiveGalleryObject(e, this);
	      },300);   //wait 300ms then run single click code
	    } else {    //tapped within 300ms of last tap. double tap
	      clearTimeout(tapped); //stop single tap callback
	      tapped=null
	      //insert things you want to do when double tapped
	      launchPhotoSwipe($(this));
	    }
    	e.preventDefault()
	});
}

function highlightActiveGalleryObject(e, target) {
	// prevent click from loading image in browser
	e.preventDefault();

	// change active thumbnail
	$galleryObject = $(target).parents('figure');
	$galleryObjectsArray.removeClass('active');
	$galleryObject.addClass('active');

	updateMetadataSidebar($galleryObject);

	// uri = [location.href, $galleryObject.find('figcaption').text()].join('/');
	// history.replaceState(null, null, uri);
}

function launchPhotoSwipe($galleryImage) {
	$("#photoswipe-container").show();
	photoIndex = $galleryImage.attr('id').split('-')[2];
	pswp = initPhotoSwipe(photoIndex);
	pswp.init();

	pswp.listen('close', function() { 
		$("#photoswipe-container").fadeOut(500);
	});

	pswp.listen('afterChange', function() {
		$imageObjectsArray.removeClass("active");
		$imageObject = $imageObjectsArray.filter("#" + pswp.currItem.el.id);

		$imageObject.addClass("active");
		updateMetadataSidebar($imageObject);
	});

	return pswp;
}

function getPhotoSwipeItems() {
	var images = $(".gallery-image");
	var items = [];

	images.each(function(index) {
		a = $(this).find('a').first();
		img = a.children('img').first();
		size = a.attr('data-size').split('x');

		item = {
			w: parseInt(size[0], 10),
			h: parseInt(size[1], 10),
			src: a.attr('href') + '?raw=1',
			msrc: img.attr('src'),
			el: this
		}

		items.push(item);
	});
	
	return items;
}

function initPhotoSwipe(index) {

	var pswpElement = document.querySelectorAll('.pswp')[0];

	var items = getPhotoSwipeItems();

	var index = parseInt(index, 10);

	// define options (if needed)
	var options = {
		index: index,
	    modal: false,
	    closeOnScroll: false,
	    escKey: true,
	    history: false,
	    preload: [4,4],
	    getThumbBoundsFn: function(index) {
            var thumbnail = items[index].el.getElementsByTagName('img')[0];
                rect = thumbnail.getBoundingClientRect();
            return {x:rect.left, y:rect.top - $('header').height(), w:rect.width};
        }
	};

	// Initializes and opens PhotoSwipe
	return new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, items, options);
}