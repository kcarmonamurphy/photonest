function configureSubmit() {
	$('.metadata-image').submit(function(e) {

		e.preventDefault();

		var data = {
			'file-name': $(this).find('.file-name input').val(),
			'title': $(this).find('.title input').val(),
			'description': $(this).find('.description input').val(),
			'keywords': getKeywordChips($(this))
		}
		
		console.log(data);
	});

	$('.metadata-folder').submit(function(e) {

		e.preventDefault();

		var data = {
			'folder-name': $(this).find('.folder-name input').val()
		}
		
		console.log(data);
	});
}

function updateMetadataSidebar($galleryObject) {
	// grab index of galleryObject
	metadataType = $galleryObject.attr('id').split('-')[1];
	index = $galleryObject.attr('id').split('-')[2];

	console.log($galleryObject);
	
	// show active metadata in sidebar
	$metadataObjectsArray.removeClass('active');
	$metadataObject = $metadataObjectsArray.filter('#m' + '-' + metadataType + '-' + index);
	$metadataObject.addClass('active');
}

function initKeywordChips() {
	$('.keywords').each(function() {
		chips = [];
		$(this).find('.chip span').each(function() {
			chips.push({ tag: $(this).text() });
		});
		$(this).find('.chips').material_chip({
			data: chips
		});
	});
}

function getChipText(chip) {
	return $(chip).contents().filter(function(){ 
	  	return this.nodeType == 3; 
	})[0].nodeValue
}


function getKeywordChips($metadataForm) {
	chips = [];
	$metadataForm.find('.chip').each(function() {
		chips.push(getChipText(this));
	});
	return chips;
}