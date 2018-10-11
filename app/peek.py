from app.path import GalleryPath

from django.conf import settings

from neo4j import GraphDatabase

from pathlib import PurePath

def peek_get(path):
  return "gotten"