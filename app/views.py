import json
from django.http import HttpResponse

from app.path import GalleryPath

from app.heavy import heavy_get
from app.peek import peek_get

def get(request, path):
    gallery_path = GalleryPath(path)
    heavy_get(gallery_path)
    data = peek_get(gallery_path)

    return HttpResponse(
      json.dumps(data),
      content_type='application/json'
    )

def peek(request, path):
    gallery_path = GalleryPath(path)
    data = peek_get(gallery_path)
    
    return HttpResponse(
      json.dumps(data),
      content_type='application/json'
    )