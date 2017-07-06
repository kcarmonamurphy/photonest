from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

from django.conf import settings
import os

from modules.metadata import MetaData

def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")

def folder(request):
    
    return HttpResponse("view image");

def photo(request):
    
    return HttpResponse("view image");

def metadata(request, filename):

    # try:
    filepath = os.path.join(settings.PHOTO_LIBRARY_DIR, filename)
    # file = open(filepath, 'r')

    md = MetaData(filepath)
    hello = md.getImageSize()
    
    context = {'filename': filename, 'output': hello}
    # except:
    #     raise Http404("File not found")


    return render(request, 'metadata.html', context)

