"""
# path.app: path relative to the application
# - /app/gallery/album/photo.jpg                                (path.app.file)
# - /app/gallery/album/                                         (path.app.dir)

# gallery_path: path including the gallery folder
# - /gallery/album/photo.jpg                                    (path.gallery.file)
# - /gallery/album/                                             (path.gallery.dir)

# relative_path: passed into the view functions, path relative to gallery folder
# - album/photo.jpg                                             (path.relative.file)
# - album/                                                      (path.relative.dir)

# thumbnail_app_path: for finding the thumbnail
# - /app/gallery/album/.photonest/photo.jpg_thumbnail_256       (path.thumbnail.small)
# - /app/gallery/album/.photonest/photo.jpg_thumbnail_512       (path.thumbnail.medium)
# - /app/gallery/album/.photonest/                              (path.thumbnail.dir)

# uri: web resource to load mime type image
# - http://domain.com/gallery/album/photo.jpg?raw=1
"""

from django.conf import settings
from django.http import Http404
import os

from pathlib import Path as ConcretePath
from pathlib import PurePath

'''
PurePath.name
PurePath.parent
'''

class Path():
    """
    Module for representing the different paths that are
    used by the various functions in the app
    """

    '''
    Initialization of Class
    -----------------------
    '''

    def __init__(self, path):
        self._path = PurePath(path)
        self._app_path = ConcretePath(settings.GALLERY_BASE_DIR).joinpath(path)

    '''
    Public Methods
    ----------------
    '''

    def is_file(self):
        return self._app_path.is_file()

    def is_dir(self):
        return self._app_path.is_dir()

    @property
    def name(self):
        return self._path.name

    @property
    def parent(self):
        return self._path.parent

    def thumbnail(self, size="small"):
        if not self.is_file():
            raise Exception('can\'t get thumbnail of folder')

        thumbnail_filename = self.name + settings.THUMBNAIL_PREFIX + str(settings.THUMBNAIL_SIZES[size])
        
        return self.parent.joinpath(
            settings.THUMBNAILS_FOLDER, thumbnail_filename)   

    @property
    def file(self):
        assert self._path is not None, (
            "property must be called on path.app,"
            "path.relative, or path.gallery"
            )
        return self._path

    @property
    def dir(self):
        assert self._path is not None, (
            "property must be called on path.app,"
            "path.relative, or path.gallery"
            )
        # return os.path.dirname(self._path)
        if self.isfile():
            return os.path.dirname(self._path)
        elif self.isdir():
            return os.path.dirname(self._path + '/')
        else:
            raise Http404("Not a file nor a dir")

    # @property
    # def parent(self):
    #     assert self._path is not None, (
    #         "property must be called on path.app,"
    #         "path.relative, or path.gallery"
    #         )
    #     return os.path.abspath(os.path.join(self._path, os.path.pardir))

    @property
    def base(self):
        assert self._path is not None, (
            "property must be called on path.app,"
            "path.relative, or path.gallery"
            )
        # return os.path.basename(self._path)
        if self.isfile():
            return os.path.basename(self._path)
        elif self.isdir():
            return os.path.basename(self._path + '/')
        else:
            raise Http404("Not a file nor a dir")



 