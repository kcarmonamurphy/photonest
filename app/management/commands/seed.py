import os
import magic
import json

from app.metadata import MetaData
from app.path import Path

from app.thumbnails import generate_thumbnails_if_missing

from app.models import Folder, Image

from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):

        parse_path(Path('desk'))

def parse_path(path):

    parent, _ = Folder.objects.get_or_create(
        uri=path.gallery.dir,
        name=path.gallery.base
    )
    parent.save()
    
    if path.isfile() and mimetype_is_image(path.app.file):

        md = MetaData(path.app.file)
        image = Image(
            uri=path.gallery.file,
            name=path.gallery.base,
            size=md.getImageSize(),
            title=md.getTitle(),
            description=md.getDescription(),
            parent=parent
        )
        image.save()

    # scan the directory specified in the path for all photos
    # and folders, send this info to browser via websockets
    for child in os.scandir(path.app.dir):

        child_path = Path(child.path, "app")

        if not child.name.startswith('.') and child.is_dir():

            folder = Folder(
                uri=child_path.gallery.dir,
                name=child.name,
                parent=parent
            )
            folder.save()

        if not child.name.startswith('.') and child.is_file() and mimetype_is_image(child.path):

            md = MetaData(child_path.app.file)
            generate_thumbnails_if_missing(child)

            image = Image(
                uri=child_path.gallery.file,
                name=child.name,
                size=md.getImageSize(),
                title=md.getTitle(),
                description=md.getDescription(),
                parent=parent
            )
            image.save()

def mimetype_is_image(path):
    '''
    Accepts a vlue of os.DirEntry
    '''
    mime_type = magic.from_file(path, mime=True)
    mime_category = mime_type.split('/')
    if mime_category[0] == 'image':
        return True
    return False

def get_metadata(md):
    return {
        'Title': md.getTitle(),
        'Description': md.getDescription(),
        'Keywords': md.getKeywords(),
        'read_only': {
            'Image Size': md.getImageSize(),
            'File Size': md.getFileSize(),
            'File Type': md.getFileType(),
            'Modify Date': md.getModifyDate(),
            'Create Date': md.getCreateDate(),
            'Make': md.getMake(),
            'Model': md.getModel(),
            'Megapixels': md.getMegapixels(),
            'Shutter Speed': md.getShutterSpeed(),
            'GPS Position': md.getGPSPosition(),
        }
    }