function isFormDirty($form) {

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

	var isDirty = false;
	for (var key in formInputs) {
	  if (formInputs.hasOwnProperty(key) && (origFormInputs[key] != formInputs[key])) {
	    console.log('INPUT CHANGED: ---------\n' + key + " / " + origFormInputs[key] + " / " + formInputs[key]);
	    isDirty = true;
	  }
	}

	return isDirty;
}

function updateOriginalFormInputs($form) {
	$form.find('.file-name input')[0].defaultValue = $form.find('.file-name input').val();
	$form.find('.title input')[0].defaultValue = $form.find('.title input').val();
	$form.find('.description input')[0].defaultValue = $form.find('.description input').val();
	$form.find('.keywords input[type="hidden"]')[0].defaultValue = JSON.stringify(getKeywordChips($form));
}

function dirtyFormHandlers() {

	$('.metadata-image').on('input', function() {

		$form = $(this);

		if (isFormDirty($form)) {
			$form.find('[type=submit]').removeClass('disabled');
		} else {
			$form.find('[type=submit]').addClass('disabled');
		}

	});

	$('.chips').on('chip.add chip.delete', function() {

		$form = $(this).parents('.metadata-image');

		if (isFormDirty($form)) {
			$form.find('[type=submit]').removeClass('disabled');
		} else {
			$form.find('[type=submit]').addClass('disabled');
		}

	});
}


function configureSubmit() {

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

				updateOriginalFormInputs($form);
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

	$('.chips').click(function() {
		$(this).find('.input')[0].style.setProperty('width', '120px', 'important');
	});
	$('.chips .input').focus(function() {
		$(this)[0].style.setProperty('width', '120px', 'important');
		$(this).parent().siblings('label').addClass('active');
	});

	$('.chips .input').blur(function() {
	    $(this)[0].style.setProperty('width','0','important');
	    if (!$(this).siblings('.chip').length) {
	    	$(this).parent().siblings('label').removeClass('active');
	    }
	}).blur();
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