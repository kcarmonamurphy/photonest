$(document).ready(function() {

	var pswp;

	$(".gallery-image").click(function() {
		$("#photoswipe-container").show();
		pswp = initPhotoSwipe(this.id);
		pswp.init();

		pswp.listen('close', function() { 
			$("#photoswipe-container").fadeOut(500);
		});
	});

	$(".gallery-image > a").click(function(e) {
		e.preventDefault();
	})

});

function getPhotoSwipeItems() {
	var images = $(".gallery-image");
	var items = [];

	images.each(function(index) {
		a = $(this).children('a').first();
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