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

    full_path = os.path.join(settings.GALLERY_BASE_DIR, path)

    md = MetaData(full_path)

    md.setTitle(data.get('title'))
    md.setDescription(data.get('description'))
    md.setKeywords(data.get('keywords'))

    if md.write():
        return JsonResponse({'status':'200'})

    return JsonResponse({'status': '500'})

def raw(request, path):

    full_path = os.path.join(settings.GALLERY_BASE_DIR, path)

    try:
        with open(full_path, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    except IOError:
        raise Exception("issue opening image")

def thumbnail(request, file_relative_path):

    file_app_path = getAppPathFromRelativePath(file_relative_path)
    dir_app_path = getDirAppPathFromFileAppPath(file_app_path)
    dir_thumbnail_app_path = getThumbnailAppPathFromDirAppPath(dir_app_path)

    thumbnail_path_256 = os.path.join(
        dir_thumbnail_app_path, 
        os.path.basename(file_relative_path) + '_thumbnail_256'
    )

    try:
        with open(thumbnail_path_256, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    except IOError:
        return raw(request, file_relative_path)


def index(request, relative_path):

    # GET
    if request.GET.get('raw'):
        return raw(request, relative_path)
    if request.GET.get('thumbnail'):
        return thumbnail(request, relative_path)

    # POST
    if request.GET.get('metadata'):
        return metadata(request, relative_path)

    try:
        app_path = getAppPathFromRelativePath(relative_path)
    except:
        raise Exception('bad path')

    if os.path.isdir(app_path):
        return _folder(request, app_path)

    if os.path.isfile(app_path):
        return _photo(request, app_path)

    raise Http404("Haven't found shit")


def _photo(request, file_app_path):

    dir_app_path = getDirAppPathFromFileAppPath(file_app_path)

    context = _buildContext(dir_app_path, file_app_path)

    return render(request, 'main.html', context)

def _folder(request, dir_app_path):

    context = _buildContext(dir_app_path)

    return render(request, 'main.html', context)

