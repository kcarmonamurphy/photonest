'''
path helper module

abs_path: path relative to the application
- /app/gallery/album/photo.jpg

gallery_path: path including the gallery folder
- /gallery/album/photo.jpg

path: passed into the view functions, path of image relative to gallery folder
- album/photo.jpg

uri: web resource to load mime type image
- http://domain.com/gallery/album/photo.jpg?raw=1
'''



from django.conf import settings
import os

# get a URI for image or folder in gallery
def getGalleryURI(path):
	gallery_path = path[path.find('/' + settings.GALLERY_PREFIX):]
	return gallery_path