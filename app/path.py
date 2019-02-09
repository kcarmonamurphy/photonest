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

    def __init__(self, path):
        """
        Constructor method for class. Rules for creating a GalleryPath
        object are that it must be a relative path off the GALLERY_BASE_DIR,
        it must exist and must not point to a file up the directory tree

        Parameters:
            path: a string
        """

        if ".." in str(path):
            raise Exception('cannot traverse backwards')

        # `_path` variable represents /api/v1/get/{path}
        # PurePath does not check if path exists in file system
        self._path = PurePath(path)

        if self._path.is_absolute():
            raise Exception('absolute paths not allowed')

        # `_app_path` represents full path from app root
        # if `_path` is "desk", `_app_path` is "/app/gallery/desk"
        # ConcretePath does not check if path exists in file system
        self._app_path = ConcretePath(settings.GALLERY_BASE_DIR).joinpath(path)

        if not self._app_path.exists():
            raise Exception('path does not exist')

    @property
    def relative_path(self):
        """
        Returns a path string relative to the gallery URL

        Examples:

        GalleryPath('desk') -> 'desk'
        GalleryPath('') -> '.'
        GalleryPath('../') -> Exception('cannot traverse backwards')
        """
        return str(self._path)

    @property
    def resource_name(self):
        """
        Returns the resource name as a string
        
        Examples:

        GalleryPath('desk') -> 'desk'
        GalleryPath('') -> ''
        GalleryPath('../') -> Exception('cannot traverse backwards')
        """
        return self._path.name

    @property
    def parent_relative(self):
        """
        Returns the parent path as a string relative to gallery URL
        
        Examples:

        GalleryPath('models/1.jpg') -> 'models'
        GalleryPath('1.jpg') -> '.'
        GalleryPath('.') -> '.'
        GalleryPath('../') -> Exception('cannot traverse backwards')
        """
        return str(self._path.parent)

    def is_file(self):
        """
        Does the path point to a file?
        
        Returns:
          Boolean
        """
        return self.app.is_file()

    def is_dir(self):
        """
        Does the path point to a directory?
        
        Returns:
          Boolean
        """
        return self.app.is_dir()

    @property
    def app(self):
        """
        Returns a PosixPath or WindowsPath path relative to the application root.
        
        Examples:

        GalleryPath('desk') -> PosixPath('/app/gallery/desk')
        GalleryPath('') -> PosixPath('/app/gallery/')
        GalleryPath('../') -> Exception('cannot traverse backwards')
        """
        return self._app_path

    @property
    def thumbnail_dir(self):
        """
        Return the absolute path to a thumbnail fplder

        Examples:
        
        /app/gallery/album/.photonest/
        """
        return self.app.parent.joinpath(
            settings.THUMBNAILS_FOLDER)

    def thumbnail(self, size="small"):
        """
        Return the absolute path to a thumbnail file

        Examples:

        /app/gallery/album/.photonest/photo.jpg_thumbnail_256  
        /app/gallery/album/.photonest/photo.jpg_thumbnail_512
        """

        if not self.is_file():
            raise Exception('can\'t get thumbnail of folder')

        thumbnail_filename = self.resource_name + settings.THUMBNAIL_PREFIX + str(settings.THUMBNAIL_SIZES[size])
        
        return self.app.parent.joinpath(
            settings.THUMBNAILS_FOLDER, thumbnail_filename)   
 