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

from django.core.management.base import BaseCommand

from neo4j import GraphDatabase
from neo4j.util import watch
import logging
from sys import stdout

from pathlib import PurePath

# watch("neo4j.bolt", logging.DEBUG, stdout)

class Command(BaseCommand):

  def handle(self, *args, **options):

    parse_path( GalleryPath(options['path']) )

  def add_arguments(self, parser):

    parser.add_argument('path', type=str)

def mimetype_is_image(path):
  '''
  Accepts a path string value
  '''
  mime_type = magic.from_file(str(path), mime=True)
  mime_category = mime_type.split('/')
  if mime_category[0] == 'image':
    return True
  return False

def get_last_modified_datetime(path):
  '''
  Accepts a PurePath value
  '''
  epoch_time = os.path.getmtime(path)
  date_time = datetime.utcfromtimestamp(epoch_time)
  return timezone.make_aware(date_time, timezone=pytz.UTC)

def parse_path(path):
  '''
  Accepts a GalleryPath value
  '''
  print("PARSE_PATH ****", str(path.parent), path.name)

  driver = GraphDatabase.driver("bolt://db:7687", auth=("neo4j", "password"))

  with driver.session() as session:

    if path.is_file() and mimetype_is_image(path.app):

      md = MetaData(path.app)
      session.write_transaction(add_image,
        uri=str(path.gallery),
        name=path.name,
        size=md.getImageSize(),
        title=md.getTitle(),
        description=md.getDescription(),
        last_modified=get_last_modified_datetime(path.app),
        parent_uri=str(path.parent)
      )

    elif path.is_dir():

      session.write_transaction(add_folder,
        uri=str(path.gallery),
        name=path.name,
        parent_uri=str(path.parent)
      )

      parse_dir(path)


def parse_dir(path):

  driver = GraphDatabase.driver("bolt://db:7687", auth=("neo4j", "password"))

  with driver.session() as session:

    # collect current list of child uris
    results = session.read_transaction(get_resources,
      uri=str(path.gallery)
    )

    resources, resources2 = set(), set()
    for resource in results:
      resources.add(resource["child.uri"])
    resources.discard('.')

    # scan the directory specified in the path for all photos
    # and folders, send this info to browser via websockets
    for child in os.scandir(path.app):

      cpath = GalleryPath(
        PurePath(child.path).relative_to(settings.GALLERY_BASE_DIR)
      )

      if not cpath.name.startswith('.') and cpath.is_dir():

        session.write_transaction(add_folder,
          uri=str(cpath.gallery),
          name=cpath.name,
          parent_uri=str(cpath.parent)
        )
        resources2.add(str(cpath.gallery))

      if not cpath.name.startswith('.') and cpath.is_file() and mimetype_is_image(cpath.app):

        md = MetaData(cpath.app)
        generate_thumbnails_if_missing(cpath)

        session.write_transaction(add_image,
          uri=str(cpath.gallery),
          name=cpath.name,
          size=md.getImageSize(),
          title=md.getTitle(),
          description=md.getDescription(),
          last_modified=get_last_modified_datetime(cpath.app),
          parent_uri=str(cpath.parent)
        )
        resources2.add(str(cpath.gallery))
        
    items_to_delete = resources - resources2
    # print("resources", resources)
    # print("resources2", resources2)
    print(items_to_delete)
    for uri in items_to_delete:
      session.write_transaction(delete_nodes_and_descendants,
        uri=uri
      )

def delete_nodes_and_descendants(tx, uri):
  print(" --- deleting node and children ---- ", uri)
  tx.run(
    f"""
      MATCH (node {{ uri: "{uri}" }})
      MATCH (node)-[:CONTAINS*0..]->(child)
      DETACH DELETE node, child
    """
  )

def get_resources(tx, uri):
  return tx.run(
    f"""
      MATCH (folder:Folder {{ uri: "{uri}" }})-[:CONTAINS]->(child)
      RETURN child.uri
    """
  )

def add_image(tx, uri, name, size, title, description, last_modified, parent_uri):
  print(" ---- adding image ----- ", uri, name, size, title, description, last_modified, parent_uri)
  tx.run(
    f"""
      MERGE (folder:Folder {{ uri: "{parent_uri}" }})
      MERGE (folder)-[:CONTAINS]->(image:Image {{  uri: "{uri}" }})
      SET image.description = "{description}",
          image.size = "{size}",
          image.title = "{title}",
          image.last_modified = "{last_modified}",
          image.parent_uri = "{parent_uri}"
    """
  )

def add_folder(tx, uri, name, parent_uri):
  print(" ---- adding folder ----- ", uri, name, parent_uri)
  tx.run(
    f"""
      MERGE (folder:Folder {{ uri: "{parent_uri}" }})
      MERGE (childfolder:Folder {{ uri: "{uri}" }})
      MERGE (folder)-[:CONTAINS]->(childfolder)
    """
  )

# RUN THIS BABY IN add_folder IF NEEDED IF CAUSING DUPLICATES
# AFTER FIRST CREATING SUBFOLDER THEN PARENT
# tx.run(
#   f"""
#     MATCH (folder:Folder {{ uri: "{uri}" }}) 
#     WITH collect(folder) AS folders
#     CALL apoc.refactor.mergeNodes(folders) YIELD node
#     RETURN *
#   """
# )
