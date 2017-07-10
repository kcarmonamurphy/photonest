$(document).ready(function() {

	var pswp;
	

	$(".button-collapse").sideNav();

	$('main').height(
		$(document).height() - 
		$('header').outerHeight() - 
		$('footer').outerHeight()
	);



	$(".gallery-image").click(function() {
		$("#gallery").hide();
		pswp = initPhotoSwipe();
		pswp.init();

		pswp.listen('close', function() { 
			$("#gallery").show();
		});
	});




});

function initPhotoSwipe() {

	var pswpElement = document.querySelectorAll('.pswp')[0];

	// build items array
	var items = [
	    {
	        src: 'https://placekitten.com/600/400',
	        w: 600,
	        h: 400
	    },
	    {
	        src: 'https://placekitten.com/1200/900',
	        w: 1200,
	        h: 900
	    }
	];

	// define options (if needed)
	var options = {
	    // optionName: 'option value'
	    // for example:
	    index: 0, // start at first slide,
	    modal: false,
	    closeOnScroll: false,
	    escKey: false,
	    history: false,
	};

	// Initializes and opens PhotoSwipe
	return new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, items, options);
}