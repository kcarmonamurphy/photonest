from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

from django.conf import settings
import os
import magic

from modules.metadata import MetaData
from modules.path_helper import *

def folder(request, abs_path):

    file_entries = []
    dir_entries = []
    index = 0

    for entry in os.scandir(abs_path):

        if not entry.name.startswith('.') and entry.is_dir():
            dir_entries.append({
                'uri': getGalleryURI(entry.path),
                'name': entry.name
            })

        if not entry.name.startswith('.') and entry.is_file():
            md = MetaData(entry.path)
            mime_type = magic.from_file(entry.path, mime=True)
            mime_category = mime_type.split('/')
            if mime_category[0] == 'image':
                file_entries.append({
                    'uri': getGalleryURI(entry.path),
                    'name': entry.name,
                    'index': index,
                    'size': md.getImageSize()
                })
                index+=1
            

    context = {
        'folder_path': path,
        'file_entries': file_entries,
        'dir_entries': dir_entries
    }
    
    return render(request, 'main.html', context)

def photo(request, path):
 
    context = {'filename': path }

    return render(request, 'main.html', context)

def raw(request, path):

    full_path = os.path.join(settings.GALLERY_DIR, path)

    try:
        with open(full_path, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    except IOError:
        raise Exception("issue opening image")

def metadata(path):

    md = MetaData(path)

    return {
        "image_size": md.getImageSize()
    }


def path(request, path):

    if request.GET.get('raw'):
        return raw(request, path)
    if request.GET.get('metadata'):
        return metadata(path)

    try:
        abs_path = os.path.join(settings.GALLERY_DIR, path)
    except:
        raise Exception('bad path')

    if os.path.isdir(abs_path):
        return folder(request, abs_path)

    if os.path.isfile(abs_path):
        return photo(request, abs_path)

    raise Http404("Haven't found shit")

