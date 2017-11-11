import os
import magic
import json

from .metadata import MetaData
from .path import Path

from .thumbnails import generate_thumbnails_if_missing

def parse_path(path, message):
    
    # if url specifies an image, send that data to browser
    # right away, so that photoswipe can load it while
    # the rest of the directory loads
    if path.isfile() and mimetype_is_image(path.app.file):

        md = MetaData(path.app.file)
        message.reply_channel.send({
            "text": json.dumps({
                'type': 'index_image',
                'uri': path.gallery.file,
                'name': os.path.basename(path.app.file),
                'index': 'show',
                'size': md.getImageSize(),
                'metadata': get_metadata(md)
            })
        }, immediately=True)

    # counters for scandir
    file_index = 0
    dir_index = 0

    # scan the directory specified in the path for all photos
    # and folders, send this info to browser via websockets
    for child in os.scandir(path.app.dir):

        child_path = Path(child.path, "app")

        if not child.name.startswith('.') and child.is_dir():

            message.reply_channel.send({
                "text": json.dumps({
                    'type': 'folder',
                    'uri': child_path.gallery.dir,
                    'name': child.name,
                    'index': dir_index
                })
            }, immediately=True)

            dir_index+=1

        if not child.name.startswith('.') and child.is_file() and mimetype_is_image(child.path):

            md = MetaData(child_path.app.file)
            generate_thumbnails_if_missing(child)

            message.reply_channel.send({
                "text": json.dumps({
                    'type': 'image',
                    'uri': child_path.gallery.file,
                    'name': child.name,
                    'index': file_index,
                    'size': md.getImageSize(),
                    'metadata': get_metadata(md)
                })
            }, immediately=True)

            file_index+=1

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