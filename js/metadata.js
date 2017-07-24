function configureSubmit() {

	$('.metadata-image').each(function() {
		$form = $(this);

		origFormInputs = {
			'file-name': $form.find('.file-name input').val(),
			'title': $form.find('.title input').val(),
			'description': $form.find('.description input').val(),
			'keywords': getKeywordChips($form)
		}
	});

	$('.metadata-image').on('input', function() {

		$form = $(this);

		var origFormInputs = {
			'file-name': $form.find('.file-name input')[0].defaultValue,
			'title': $form.find('.title input')[0].defaultValue,
			'description': $form.find('.description input')[0].defaultValue,
			'keywords': eval($form.find('.keywords input[type="hidden"]')[0].defaultValue).toString()
		}

		var formInputs = {
			'file-name': $form.find('.file-name input').val(),
			'title': $form.find('.title input').val(),
			'description': $form.find('.description input').val(),
			'keywords': getKeywordChips($form)
		}

		for (var key in formInputs) {
		  if (formInputs.hasOwnProperty(key)) {
		    console.log(key + " / " + origFormInputs[key] + " / " + formInputs[key]);
		  }
		}


	});

	$('.metadata-image').submit(function(e) {

		e.preventDefault();

		$form = $(this);

		var formInputs = {
			'file-name': $form.find('.file-name input').val(),
			'title': $form.find('.title input').val(),
			'description': $form.find('.description input').val(),
			'keywords': getKeywordChips($form)
		}

		var endpoint = $form.attr('action') + '?metadata=1';
		var data = { 'data': JSON.stringify(formInputs) }
		
		$.post(endpoint, data, function(resp) {
			if (resp.status == '200') {
				$form.css({backgroundColor:'#b2ff59'});
				$form.animate({backgroundColor: 'white'}, 2000);
				$form.removeClass('dirty');
				$form.find('[type=submit]').addClass('disabled');
			}
		});

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