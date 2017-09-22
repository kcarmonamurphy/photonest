from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render

from django.conf import settings
import os
import magic
import json

from .metadata import MetaData
from .thumbnails import *
from .path import Path

from subprocess import check_output

def _buildContext(root_path):

    file_entries = []
    dir_entries = []
    file_index = 0
    dir_index = 0
    image_index = None

    for child in os.scandir(root_path.app.dir):

        child_path = Path(child.path, "app")

        if not child.name.startswith('.') and child.is_dir():

            dir_entries.append({
                'uri': child_path.gallery.dir,
                'name': child.name,
                'index': dir_index
            })
            dir_index+=1

        if not child.name.startswith('.') and child.is_file():

            generateThumbnailsIfNotPresent(child)

            md = MetaData(child_path.app.file)
            mime_type = magic.from_file(child.path, mime=True)
            mime_category = mime_type.split('/')
            if mime_category[0] == 'image':

                if root_path.app.file == child_path.app.file:
                    image_index = file_index

                file_entries.append({
                    'uri': child_path.gallery.file,
                    'name': child.name,
                    'index': file_index,
                    'size': md.getImageSize(),
                    'metadata': _getMetadata(md)
                })
                file_index+=1
            
    context = {
        'file_entries': file_entries,
        'dir_entries': dir_entries,
        'base_url': root_path.gallery.dir,
        'image_index': image_index
    }
    
    return context

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

def metadata(request, path):

    data = json.loads(request.POST.get('data'))

    md = MetaData(path.app.file)

    md.setTitle(data.get('title'))
    md.setDescription(data.get('description'))
    md.setKeywords(data.get('keywords'))

    if md.write():
        return JsonResponse({'status':'200'})

    return JsonResponse({'status': '500'})

def raw(request, path):

    try:
        with open(path.app.file, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    except IOError:
        raise Exception("issue opening image")

def thumbnail(request, path):

    try:
        with open(path.thumbnail.small, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    except IOError:
        return raw(request, path)


def index(request, relative_path):

    path = Path(relative_path)

    # GET ASSETS
    if request.GET.get('raw'):
        return raw(request, path)
    if request.GET.get('thumbnail'):
        return thumbnail(request, path)

    # MODIFY METADATA
    if request.GET.get('metadata'):
        return metadata(request, path)

    context = _buildContext(path)

    return render(request, 'main.html', context)

