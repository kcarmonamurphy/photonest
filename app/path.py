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

class Path():
    """
    Module for representing the different paths that are
    used by the various functions in the app
    """

    '''
    Initialization of Class
    -----------------------
    '''

    def __init__(self, path, path_type='relative'):

        if path_type == 'relative':
            self._app_path = os.path.join(
                settings.GALLERY_BASE_DIR,
                path
            )

        elif path_type == 'gallery':
            self._app_path = os.path.join(
                settings.BASE_DIR,
                path
            )

        elif path_type == 'app':
            self._app_path = path

    '''
    Public Methods
    ----------------
    '''

    def isfile(self):
        return os.path.isfile(self._app_path)

    def isdir(self):
        return os.path.isdir(self._app_path)

    def isrootdir(self):
        return os.path.samefile(self._app_path, settings.GALLERY_BASE_DIR)

    @property
    def app(self):
        self._path = self._app_path
        return self

    @property
    def relative(self):
        self._path = os.path.relpath(self._app_path, settings.GALLERY_PREFIX)
        return self

    @property
    def gallery(self):
        self._path = self._app_path[self._app_path.find('/' + settings.GALLERY_PREFIX):]
        return self

    @property
    def thumbnail(self):
        if self.isfile():
            self._path = os.path.join(
                os.path.dirname(self._app_path), 
                settings.THUMBNAILS_FOLDER,
                os.path.basename(self._app_path)
                )
            return self
        else:
            raise Exception('can\'t get thumbnail of folder')

    @property
    def small(self):
        return self._path + '_thumbnail_' + str(settings.THUMBNAIL_SIZES['small'])

    @property
    def medium(self):
        return self._path + '_thumbnail_' + str(settings.THUMBNAIL_SIZES['medium'])

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



 