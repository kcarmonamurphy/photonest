from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render

from django.conf import settings
import os
import magic
import json

from django.template import loader

from .metadata import MetaData
from .thumbnails import *
from .path import Path

from subprocess import check_output

def figure(request):

    context = dict(json.loads(request.body))

    if context.get('type') == 'image':
        return HttpResponse(loader.render_to_string(
            'image.html',
            context
        ))

    if context.get('type') == 'folder':
        return HttpResponse(loader.render_to_string(
            'folder.html',
            context
        ))

    if context.get('type') == 'index_image':
        return HttpResponse(loader.render_to_string(
            'image.html',
            context
        ))

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

    # LOAD FIGURE
    if request.GET.get('figure'):
        return figure(request)

    if request.GET.get('item_template'):
        return item_template(request)

    path = Path(relative_path)

    # GET ASSETS
    if request.GET.get('raw'):
        return raw(request, path)
    if request.GET.get('thumbnail'):
        return thumbnail(request, path)

    # MODIFY METADATA
    if request.GET.get('metadata'):
        return metadata(request, path)

    return render(request, 'main.html', {})

def template(request, template):

    if template == 'item':
        print(HttpResponse(loader.render_to_string(
            'item.html'
        )))
        return HttpResponse(loader.render_to_string(
            'item.html'
        ))

