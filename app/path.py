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

    def __init__(self, relative_path):


        self._relative_path = relative_path

        self._gallery_path = os.path.join(
            '/',
            settings.GALLERY_PREFIX,
            self._relative_path
            )

        self._app_path = os.path.join(
            settings.GALLERY_BASE_DIR,
            self._relative_path
            )

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

    @property
    def app(self):
        return self._app_path

    @property
    def relative(self):
        return self._relative_path

    @property
    def gallery(self):
        return self._gallery_path

    @property
    def thumbnail(self):
        return self._thumbnail_path


        
 