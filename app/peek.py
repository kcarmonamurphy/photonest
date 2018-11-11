from app.path import GalleryPath

import json

from django.conf import settings

from neo4j import GraphDatabase

from pathlib import PurePath

from app.fileutils import FileUtils

from app.graphmethods import GraphMethods

def peek_get(path):
  '''
  Accepts a GalleryPath value
  '''
  print("PARSE_PATH ****", str(path.parent), path.name)

  driver = GraphDatabase.driver("bolt://db:7687", auth=("neo4j", "password"))

  with driver.session() as neo4j_session:

    response = []

    if path.is_file() and FileUtils().mimetype_is_image(path.app):

      for resource in neo4j_session.read_transaction(GraphMethods().get_single_image,
        uri=str(path.gallery)
      ):
        image = resource['image']
        response.append({
          "parent_uri": image["parent_uri"],
          "description": image["description"],
          'size': image['size'],
          'title': image['title'],
          'last_modified': image['last_modified'],
          'uri': image['uri'],
          'type': 'image'
        })

      return response

    elif path.is_dir():

      response = []
      for resource in neo4j_session.read_transaction(GraphMethods().get_folders,
        uri=str(path.gallery)
      ):
        folder = resource['child']
        response.append({
          "parent_uri": folder["parent_uri"],
          'uri': folder['uri'],
          'type': 'folder'
        })

      for resource in neo4j_session.read_transaction(GraphMethods().get_images,
        uri=str(path.gallery)
      ):
        image = resource['child']
        response.append({
          "parent_uri": image["parent_uri"],
          "description": image["description"],
          'size': image['size'],
          'title': image['title'],
          'last_modified': image['last_modified'],
          'uri': image['uri'],
          'type': 'image'
        })

      return response
