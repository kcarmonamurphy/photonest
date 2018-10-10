"""
# path.app: path relative to the application
# - /app/gallery/album/photo.jpg
# - /app/gallery/album/                          

# path.gallery: passed into the view functions, path relative to gallery folder
# - album/photo.jpg                                
# - album/                                                

# path.thumbnail(): for finding the thumbnail
# - /app/gallery/album/.photonest/photo.jpg_thumbnail_256  
# - /app/gallery/album/.photonest/photo.jpg_thumbnail_512      
# - /app/gallery/album/.photonest/                        

# uri: web resource to load mime type image
# - http://domain.com/gallery/album/photo.jpg?raw=1
"""

from django.conf import settings
from django.http import Http404
import os

from pathlib import Path as ConcretePath
from pathlib import PurePath

class GalleryPath():
    """
    Module for representing the different paths that are
    used by the various functions in the app
    """

    '''
    Initialization of Class
    -----------------------
    '''

    def __init__(self, path):

        if ".." in str(path):
            raise Exception('cannot traverse backwards')

        self._path = PurePath(path)

        if self._path.is_absolute():
            raise Exception('absolute paths not allowed')

        self._app_path = ConcretePath(settings.GALLERY_BASE_DIR).joinpath(path)

        if not self._app_path.exists():
            raise Exception('path does not exist')

    '''
    Public Methods
    ----------------
    '''

    @property
    def app(self):
        return self._app_path

    @property
    def gallery(self):
        return self._path

    @property
    def name(self):
        return self.gallery.name

    @property
    def parent(self):
        return self.gallery.parent

    @property
    def app_parent(self):
        return self.app.parent

    def is_file(self):
        return self.app.is_file()

    def is_dir(self):
        return self.app.is_dir()

    @property
    def thumbnail_dir(self):
        return self.app_parent.joinpath(
            settings.THUMBNAILS_FOLDER)

    def thumbnail(self, size="small"):
        if not self.is_file():
            raise Exception('can\'t get thumbnail of folder')

        thumbnail_filename = self.name + settings.THUMBNAIL_PREFIX + str(settings.THUMBNAIL_SIZES[size])
        
        return self.app_parent.joinpath(
            settings.THUMBNAILS_FOLDER, thumbnail_filename)   
 