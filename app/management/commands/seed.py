import os
import magic
import json
from datetime import datetime
import pytz

from app.metadata import MetaData
from app.path import Path

from app.thumbnails import generate_thumbnails_if_missing

from app.models import Folder, Image

from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):

    def handle(self, *args, **options):

        parse_path(Path(''))

def parse_path(path):

    print("PARSE_PATH ****", path.gallery.dir, path.gallery.base)

    parent, _ = Folder.objects.get_or_create(
        uri=path.gallery.dir
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
            last_modified=get_last_modified_datetime(path.app.file),
            parent=parent
        )
        image.save()

    elif path.isdir():

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
                    last_modified=get_last_modified_datetime(child_path.app.file),
                    parent=parent
                )
                image.save()

                print(os.path.getmtime(path.app.file))

def get_last_modified_datetime(path):
    epoch_time = os.path.getmtime(path)
    date_time = datetime.utcfromtimestamp(epoch_time)
    return timezone.make_aware(date_time, timezone=pytz.UTC)

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