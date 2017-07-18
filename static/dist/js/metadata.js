function updateMetadataSidebar($galleryObject) {
	// grab index of galleryObject
	index = $galleryObject.attr('id').split('-')[1];
	
	// show active metadata in sidebar
	$metadataObjectsArray.removeClass('active');
	$metadataObject = $metadataObjectsArray.filter('#metadata-' + index);
	$metadataObject.addClass('active');

	$('.metadata-image.active').submit(function(e) {

		console.log('hello');
		e.preventDefault();

		var data = {
			'file-name': $(this).find('.file-name input').val(),
			'title': $(this).find('.title input').val(),
			'description': $(this).find('.description input').val(),
			'keywords': $(this).find('.keywords input').val()
		}
		
		console.log(data);
	});
}