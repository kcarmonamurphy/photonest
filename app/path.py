from django.conf import settings
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
            self._relative_path = path

            self._gallery_path = os.path.join(
                '/',
                settings.GALLERY_PREFIX,
                self._relative_path
                )

            self._app_path = os.path.join(
                settings.GALLERY_BASE_DIR,
                self._relative_path
                )

        elif path_type == 'app':

            self._app_path = path

            self._gallery_path = path[path.find('/' + settings.GALLERY_PREFIX):]

        if os.path.basename(self._app_path):
            self._thumbnail_path = os.path.join(
                os.path.dirname(self._app_path), 
                settings.THUMBNAILS_FOLDER,
                os.path.basename(self._app_path) + '_thumbnail_256'
                )

    '''
    Public Methods
    ----------------
    '''

    def isfile(self):
        return os.path.isfile(self._app_path)

    def isdir(self):
        return os.path.isdir(self._app_path)

    @property
    def app(self):
        self._path = self._app_path
        return self

    @property
    def relative(self):
        self._path = self._relative_path
        return self

    @property
    def gallery(self):
        self._path = self._gallery_path
        return self

    @property
    def thumbnail(self):
        return self._thumbnail_path

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
        return os.path.dirname(self._path)

    @property
    def base(self):
        assert self._path is not None, (
            "property must be called on path.app,"
            "path.relative, or path.gallery"
            )
        return os.path.basename(self._path)

 