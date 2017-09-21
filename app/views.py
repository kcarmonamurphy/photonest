from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render

from django.conf import settings
import os
import magic
import json

from .metadata import MetaData
from .path_helper import *
from .thumbnails import *
from .path import Path

from subprocess import check_output

def _buildContext(dir_path, file_path=None):

    file_entries = []
    dir_entries = []
    file_index = 0
    dir_index = 0
    image_index = None

    for entry in os.scandir(dir_path):

        if not entry.name.startswith('.') and entry.is_dir():
            dir_entries.append({
                'uri': getGalleryPathFromAppPath(entry.path),
                'name': entry.name,
                'index': dir_index
            })
            dir_index+=1

        if not entry.name.startswith('.') and entry.is_file():

            generateThumbnailsIfNotPresent(entry)

            md = MetaData(entry.path)
            mime_type = magic.from_file(entry.path, mime=True)
            mime_category = mime_type.split('/')
            if mime_category[0] == 'image':

                if file_path == entry.path:
                    image_index = file_index

                file_entries.append({
                    'uri': getGalleryPathFromAppPath(entry.path),
                    'name': entry.name,
                    'index': file_index,
                    'size': md.getImageSize(),
                    'metadata': _getMetadata(md)
                })
                file_index+=1
            
    context = {
        'file_entries': file_entries,
        'dir_entries': dir_entries,
        'base_url': getGalleryPathFromAppPath(dir_path),
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

    md = MetaData(path.app)

    md.setTitle(data.get('title'))
    md.setDescription(data.get('description'))
    md.setKeywords(data.get('keywords'))

    if md.write():
        return JsonResponse({'status':'200'})

    return JsonResponse({'status': '500'})

def raw(request, path):

    try:
        with open(path.app, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    except IOError:
        raise Exception("issue opening image")

def thumbnail(request, path):

    try:
        with open(path.thumbnail, "rb") as file:
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

    # SHOW GALLERY
    if path.isdir():
        return _folder(request, path)

    # SHOW IMAGE
    if path.isfile():
        return _photo(request, path)

    raise Http404("Haven't found shit")


def _photo(request, path):

    context = _buildContext(path.app.dir, path.app.file)

    return render(request, 'main.html', context)

def _folder(request, path):

    print('folder')

    context = _buildContext(path.app.dir)

    return render(request, 'main.html', context)

