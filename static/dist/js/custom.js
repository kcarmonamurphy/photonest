$(document).ready(function() {

	flexListener = galleryKeyboardShortcuts();

	$(".gallery-image").first().addClass("active");

	$(".gallery-image a").click(function(e) {
		e.preventDefault();

		$(".gallery-image").removeClass("active");
		$(this).parents(".gallery-image").addClass("active");
	});

	$(".gallery-image").dblclick(function() {
		launchPhotoSwipe(this);
	});


	var tapped=false
	$(".gallery-image").on("touchstart",function(e){
	    if(!tapped){ //if tap is not set, set up single tap
	      tapped=setTimeout(function(){
	          tapped=null
	          //insert things you want to do when single tapped
	      },300);   //wait 300ms then run single click code
	    } else {    //tapped within 300ms of last tap. double tap
	      clearTimeout(tapped); //stop single tap callback
	      tapped=null
	      //insert things you want to do when double tapped
	    }
    	e.preventDefault()
	});

});

function launchPhotoSwipe(galleryImage) {
	$("#photoswipe-container").show();
	photoIndex = $(galleryImage).attr('id');
	var pswp = initPhotoSwipe(photoIndex);
	pswp.init();

	pswp.listen('close', function() { 
		$("#photoswipe-container").fadeOut(500);
	});
	
	photoSwipeKeyboardShortcuts(flexListener, pswp);
}

function photoSwipeKeyboardShortcuts(flexListener, pswp) {
	var pswpKeypressListener = new window.keypress.Listener();

	pswpKeypressListener.simple_combo("shift _", function() {
	    pswp.zoomTo(pswp.getZoomLevel()/1.5, {x:pswp.viewportSize.x/2,y:pswp.viewportSize.y/2}, 50, false, function(now) {
		});
	});

	pswpKeypressListener.simple_combo("shift +", function() {
	    pswp.zoomTo(pswp.getZoomLevel()*1.5, {x:pswp.viewportSize.x/2,y:pswp.viewportSize.y/2}, 50, false, function(now) {
		});
	});

	$('input, textarea')
    	.bind("focus", function() { pswpKeypressListener.stop_listening(); })
		.bind("blur", function() { pswpKeypressListener.listen(); });

	flexListener.stop_listening();

	pswp.listen('close', function() {
		flexListener.listen();
	});
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
			src: a.attr('href'),
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
	    getThumbBoundsFn: function(index) {
            var thumbnail = items[index].el.getElementsByTagName('img')[0];
                rect = thumbnail.getBoundingClientRect();
            return {x:rect.left, y:rect.top - $('header').height(), w:rect.width};
        }
	};

	// Initializes and opens PhotoSwipe
	return new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, items, options);
}