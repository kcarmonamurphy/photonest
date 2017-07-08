from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

from django.conf import settings
import os

from modules.metadata import MetaData

def folder(request, path):

    file_paths = []
    dir_paths = []
    for _, dirs, files in os.walk(path):
        for name in files:
            file_paths.append(name)
        for name in dirs:
            dir_paths.append(name)

    context = {
        'folder_path': path,
        'dir_paths': dir_paths,
        'file_paths': file_paths
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
        red = Image.new('RGBA', (1, 1), (255,0,0,0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response

def metadata(path):

    md = MetaData(path)

    return {
        "image_size": md.getImageSize()
    }


def path(request, path):

    try:
        full_path = os.path.join(settings.GALLERY_DIR, path)
    except:
        raise Exception('bad path')

    if os.path.isdir(full_path):
        return folder(request, full_path)

    if os.path.isfile(full_path):
        return photo(request, full_path)

    raise Http404("Haven't found shit")

