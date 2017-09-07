from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render

from django.conf import settings
import os
import magic
import json

from modules.metadata import MetaData
from modules.path_helper import *

from subprocess import check_output

def hasThumbnail(file):
    
    dir_path = os.path.dirname(file.path)

    thumbnail_name = file.name + '_thumbnail_512'

    thumbnail_path = os.path.join(dir_path, '.photonest', thumbnail_name)

    # print(thumbnail_path)

    try:
        with open(thumbnail_path, "rb") as thumbnail:
            return True
    except IOError:
        return False

def generateThumbnail(file):

    dir_path = os.path.dirname(file.path)

    thumbnail_name = file.name + '_thumbnail_512'

    thumbnail_path = os.path.join(dir_path, '.photonest', thumbnail_name)

    print(file.path)
    print(thumbnail_path)

    try:
        output = check_output(["convert", file.path, "-strip", "-resize", "512x512", thumbnail_path])
        print(output)
    except:
        print("something went wrong")

def _buildContext(dir_path, file_path=None):

    file_entries = []
    dir_entries = []
    file_index = 0
    dir_index = 0
    image_index = None

    for entry in os.scandir(dir_path):

        if not entry.name.startswith('.') and entry.is_dir():
            dir_entries.append({
                'uri': getGalleryURI(entry.path),
                'name': entry.name,
                'index': dir_index
            })
            dir_index+=1

        if not entry.name.startswith('.') and entry.is_file():

            if not hasThumbnail(entry):
                generateThumbnail(entry)

            md = MetaData(entry.path)
            mime_type = magic.from_file(entry.path, mime=True)
            mime_category = mime_type.split('/')
            if mime_category[0] == 'image':

                if file_path == entry.path:
                    image_index = file_index

                file_entries.append({
                    'uri': getGalleryURI(entry.path),
                    'name': entry.name,
                    'index': file_index,
                    'size': md.getImageSize(),
                    'metadata': _getMetadata(md)
                })
                file_index+=1
            
    context = {
        'folder_path': path,
        'file_entries': file_entries,
        'dir_entries': dir_entries,
        'base_url': getGalleryURI(dir_path),
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

    full_path = os.path.join(settings.GALLERY_DIR, path)

    md = MetaData(full_path)

    md.setTitle(data.get('title'))
    md.setDescription(data.get('description'))
    md.setKeywords(data.get('keywords'))

    if md.write():
        return JsonResponse({'status':'200'})

    return JsonResponse({'status': '500'})

def raw(request, path):

    full_path = os.path.join(settings.GALLERY_DIR, path)

    try:
        with open(full_path, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    except IOError:
        raise Exception("issue opening image")

def thumbnail(request, path):

    thumbnail_512_path = path + "_thumbnail_512"

    full_path = os.path.join(settings.GALLERY_DIR, '.photonest', thumbnail_512_path)

    try:
        with open(full_path, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    except IOError:
        return raw(request, path)


def path(request, path):

    # GET
    if request.GET.get('raw'):
        return raw(request, path)
    if request.GET.get('thumbnail'):
        return thumbnail(request, path)

    # POST
    if request.GET.get('metadata'):
        return metadata(request, path)

    try:
        abs_path = os.path.join(settings.GALLERY_DIR, path)
    except:
        raise Exception('bad path')

    if os.path.isdir(abs_path):
        return _folder(request, abs_path)

    if os.path.isfile(abs_path):
        return _photo(request, abs_path)

    raise Http404("Haven't found shit")


def _photo(request, file_path):

    dir_path = os.path.dirname(file_path)

    context = _buildContext(dir_path, file_path)

    return render(request, 'main.html', context)

def _folder(request, dir_path):

    context = _buildContext(dir_path)

    return render(request, 'main.html', context)

