from django.conf import settings
import os
import magic
import json

from .metadata import MetaData
from .thumbnails import *
from .path import Path

from subprocess import check_output

# Connected to websocket.connect
def ws_add(message, relative_path):
    # Accept the connection
    message.reply_channel.send({"accept": True})

# Connected to websocket.receive
def ws_message(message, relative_path):

    print("hello")

    path = Path(relative_path)

    parse_path(path, message)

# Connected to websocket.disconnect
def ws_disconnect(message):
    pass
    # message.discard(message.reply_channel)

def parse_path(path, message):

    file_index = 0
    dir_index = 0
    image_index = None

    for child in os.scandir(path.app.dir):

        child_path = Path(child.path, "app")

        if not child.name.startswith('.') and child.is_dir():

            print(child.name)

            message.reply_channel.send({
                "text": json.dumps({
                    'uri': child_path.gallery.dir,
                    'name': child.name,
                    'index': dir_index
                })
            }, immediately=True)

            dir_index+=1

        if not child.name.startswith('.') and child.is_file():

            generateThumbnailsIfNotPresent(child)

            print(child.name)

            md = MetaData(child_path.app.file)
            mime_type = magic.from_file(child.path, mime=True)
            mime_category = mime_type.split('/')
            if mime_category[0] == 'image':

                if path.app.file == child_path.app.file:
                    image_index = file_index

                message.reply_channel.send({
                    "text": json.dumps({
                        'uri': child_path.gallery.file,
                        'name': child.name,
                        'index': file_index,
                        'size': md.getImageSize(),
                        'metadata': _getMetadata(md)
                    })
                }, immediately=True)

                file_index+=1

def _getMetadata(md):
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
