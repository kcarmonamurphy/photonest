import os
import magic
import json

import pdb

from app.metadata import MetaData
from app.path import Path

from app.thumbnails import generate_thumbnails_if_missing

from app.models import Folder, Image

from django.core.management.base import BaseCommand

from .seed import parse_path as pp
from .seed import get_last_modified_datetime

from django.db.models.base import ObjectDoesNotExist

class Command(BaseCommand):

    def handle(self, *args, **options):

        check(Path(''))

def check(path):
    
    if path.isfile() and mimetype_is_image(path.app.file):
        if is_image_inconsistent(path):
            pp(path)

    is_folder_inconsistent(path)

    # scan the directory specified in the path for all photos
    # and folders, send this info to browser via websockets
    

def is_folder_inconsistent(path):
    folder = Folder.objects.get(pk=path.gallery.dir)

    db_folders = set(folder.folders.all().values_list('uri', flat=True))
    db_images = set(folder.images.all().values_list('uri', flat=True))

    fs_folders = set()
    fs_images = set()

    parse_set = set()
    delete_folder_set = set()
    delete_image_set = set()

    for child in os.scandir(path.app.dir):

        child_path = Path(child.path, path_type="app")

        if not child.name.startswith('.') and child.is_dir():
            fs_folders.add(child_path.gallery.dir)

        if not child.name.startswith('.') and child.is_file() and mimetype_is_image(child.path):
            fs_images.add(child_path.gallery.file)

    for missing_from_db_gallery_path in list(fs_folders - db_folders):
        parent_directory_gallery_path = missing_from_db_gallery_path.rsplit('/', 1)[0][1:]
        # path = Path(parent_directory_gallery_path, path_type='gallery')
        parse_set.add(parent_directory_gallery_path)

    for missing_from_db_gallery_path in list(fs_images - db_images):
        # path = Path(missing_from_db_gallery_path[1:], path_type='gallery')
        parse_set.add(missing_from_db_gallery_path[1:])

    for missing_from_fs_gallery_path in list(db_folders - fs_folders):
        path = Path(missing_from_fs_gallery_path[1:], path_type='gallery')
        delete_folder_set.add(path)

    for missing_from_fs_gallery_path in list(db_images - fs_images):
        path = Path(missing_from_fs_gallery_path[1:], path_type='gallery')
        delete_image_set.add(path)


    for parse_path in list(parse_set):
        print("pp " + parse_path)
        # pdb.set_trace()
        pp(Path(parse_path, path_type="gallery"))

    for folder_path in list(delete_folder_set):
        print("folder " + folder_path.gallery.file)
        Folder.objects.get(pk=folder_path.gallery.file).delete()

    for image_path in list(delete_image_set):
        print("image " + image_path.gallery.file)
        Image.objects.get(pk=image_path.gallery.file).delete()

    # pp(path)
    # Folder.objects.get(pk=path.gallery.dir).delete()

    # try:
    #     folder = Folder.objects.get(pk=child_path.gallery.dir)
    # except ObjectDoesNotExist:
    #     pp(path)

def is_image_inconsistent(path):
    image = Image.objects.get(pk=path.gallery.file)

    if image.last_modified != get_last_modified_datetime(path.app.file):
        return True
    return False

def mimetype_is_image(path):
    '''
    Accepts a vlue of os.DirEntry
    '''
    mime_type = magic.from_file(path, mime=True)
    mime_category = mime_type.split('/')
    if mime_category[0] == 'image':
        return True
    return False
