import json
from django.http import HttpResponse

from app.path import GalleryPath

from app.heavy import heavy_get
from app.light import light_get

def get(request, path):
  gallery_path = GalleryPath(path)
  heavy_get(gallery_path)
  data = light_get(gallery_path)

  return HttpResponse(
    json.dumps(data),
    content_type='application/json'
  )

def peek(request, path):
  # convert peek request to not use GalleryPath class
  # since it slows down the response time by making a call
  # to the file system
  gallery_path = GalleryPath(path)
  data = light_get(gallery_path)

  return HttpResponse(
    json.dumps(data),
    content_type='application/json'
  )