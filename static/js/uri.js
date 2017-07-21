function setFileURI($galleryObject) {
	fileURI = $galleryObject.find('a').attr('href');
	history.replaceState(null, null, fileURI);
}

function revertToBaseURI() {
	baseURI = $('base').attr('href');
	history.replaceState(null, null, baseURI);
}

// Create a closure
(function(){
    var $fnAddClass = jQuery.fn.addClass;

    jQuery.fn.addClass = function(){
        var result = $fnAddClass.apply(this, arguments);

        if (arguments[0] == 'active') {

        	if (this.hasClass('gallery-image')) {
        		activeGalleryImage(this);
        	}
        	if (this.hasClass('gallery-folder')) {
        		activeGalleryFolder(this);
        	}
        }
        return result;
    }
})();

function activeGalleryImage($galleryImage) {
	updateMetadataSidebar($galleryImage);
	if (!isGalleryClosed()) setFileURI($galleryImage);
}

function activeGalleryFolder($galleryFolder) {
	updateMetadataSidebar($galleryFolder);
}