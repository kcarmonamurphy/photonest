import os
import magic
import json
from datetime import datetime
import pytz
from django.utils import timezone

from app.metadata import MetaData
from app.path import GalleryPath

from django.conf import settings

from app.thumbnails import generate_thumbnails_if_missing

from neo4j import GraphDatabase
from neo4j.util import watch
import logging
from sys import stdout

from pathlib import PurePath

from app.graphmethods import GraphMethods
from app.fileutils import FileUtils


def heavy_get(path):
  '''
  Accepts a GalleryPath value
  '''
  print("PARSE_PATH ****", str(path.parent), path.name)

  driver = GraphDatabase.driver("bolt://db:7687", auth=("neo4j", "password"))

  with driver.session() as neo4j_session:

    if path.is_file() and FileUtils().mimetype_is_image(path.app):

      md = MetaData(path.app)
      neo4j_session.write_transaction(GraphMethods().add_image,
        uri=str(path.gallery),
        name=path.name,
        size=md.getImageSize(),
        title=md.getTitle(),
        description=md.getDescription(),
        last_modified=FileUtils().get_last_modified_datetime(path.app),
        parent_uri=str(path.parent)
      )

    elif path.is_dir():

      neo4j_session.write_transaction(GraphMethods().add_folder,
        uri=str(path.gallery),
        name=path.name,
        parent_uri=str(path.parent)
      )

      parse_dir(path)

    return "done"

def collect_existing_resources(path, neo4j_session):
  # collect current list of child uris

  resources = set()

  for resource in neo4j_session.read_transaction(GraphMethods().get_child_uris,
    uri=str(path.gallery)
  ):
    resources.add(resource["child.uri"])

  resources.discard('.')

  return resources

def exclude_unneeded_resources(existing_resources, parsed_resources):
  items_to_delete = existing_resources - parsed_resources

  print(items_to_delete)
  for uri in items_to_delete:
    neo4j_session.write_transaction(GraphMethods().delete_nodes_and_descendants,
      uri=uri
    )


def parse_dir(path):

  driver = GraphDatabase.driver("bolt://db:7687", auth=("neo4j", "password"))

  with driver.session() as neo4j_session:

    existing_resources = collect_existing_resources(path, neo4j_session)
    parsed_resources = set()

    # scan the directory specified in the path for all photos
    # and folders, send this info to browser via websockets
    for child in os.scandir(path.app):

      cpath = GalleryPath(
        PurePath(child.path).relative_to(settings.GALLERY_BASE_DIR)
      )

      if not cpath.name.startswith('.') and cpath.is_dir():

        neo4j_session.write_transaction(GraphMethods().add_folder,
          uri=str(cpath.gallery),
          name=cpath.name,
          parent_uri=str(cpath.parent)
        )
        parsed_resources.add(str(cpath.gallery))

      if not cpath.name.startswith('.') and cpath.is_file() and FileUtils().mimetype_is_image(cpath.app):

        md = MetaData(cpath.app)
        generate_thumbnails_if_missing(cpath)

        neo4j_session.write_transaction(GraphMethods().add_image,
          uri=str(cpath.gallery),
          name=cpath.name,
          size=md.getImageSize(),
          title=md.getTitle(),
          description=md.getDescription(),
          last_modified=FileUtils().get_last_modified_datetime(cpath.app),
          parent_uri=str(cpath.parent)
        )
        parsed_resources.add(str(cpath.gallery))
        
    exclude_unneeded_resources(existing_resources, parsed_resources)