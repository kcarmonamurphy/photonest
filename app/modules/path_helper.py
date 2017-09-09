'''
path helper module

app_path: path relative to the application
- /app/gallery/album/photo.jpg 				(file_app_path)
- /app/gallery/album/ 						(dir_app_path)

gallery_path: path including the gallery folder
- /gallery/album/photo.jpg 					(file_gallery_path)
- /gallery/album/ 							(dir_gallery_path)

relative_path: passed into the view functions, path relative to gallery folder
- album/photo.jpg							(file_relative_path)
- album/									(dir_relative_path)

thumbnail_app_path: for finding the thumbnail
- /app/gallery/album/.photonest/photo.jpg	(file_thumbnail_app_path)
- /app/gallery/album/.photonest/			(dir_thumbnail_app_path)

uri: web resource to load mime type image
- http://domain.com/gallery/album/photo.jpg?raw=1
'''

from django.conf import settings
import os


def getGalleryPathFromAppPath(app_path):
	""" Converts an app_path to a gallery_path

	Args:
		app_path (string)

	Returns:
		gallery_path (string)

	"""
	return app_path[app_path.find('/' + settings.GALLERY_PREFIX):]

def getAppPathFromRelativePath(relative_path):
	""" Converts a relative_path to an app_path

	Args:
		relative_path (string)

	Returns:
		app_path (string)

	"""
	return os.path.join(settings.GALLERY_BASE_DIR, relative_path)


def getDirAppPathFromFileAppPath(file_app_path):
	""" Get the directory app_path for a given file app_path

	Args:
		app_path (string)

	Returns:
		app_path (string)

	"""
	dir_app_path = os.path.dirname(file_app_path)
	assert (dir_app_path + '/' != file_app_path), \
		'file_app_path shouldn\'t be a directory'
	return dir_app_path

def getThumbnailAppPathFromDirAppPath(dir_app_path):
	""" Get the thumbnail_app_path for thumbnails
	for a given dir_app_path

	Args:
		dir_app_path (string)

	Returns:
		dir_thumbnail_app_path (string)

	"""
	return os.path.join(dir_app_path, '.photonest')




