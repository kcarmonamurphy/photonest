from os import scandir

from app.metadata import MetaData
from app.path import GalleryPath

from django.conf import settings

from app.thumbnails import generate_thumbnails_if_missing

import logging
logging.basicConfig(level=logging.INFO)

from pathlib import PurePath

from app.graphmethods import GraphMethods
from app.fileutils import FileUtils

def heavy_get(path):
  """
  Heavyweight GET for any GalleryPath object which parses metadata
  of either single image element or all subfolder contents

  Parameters:
    path: GalleryPath object
  """

  logging.info(f" get {path.parent}/{path.gallery})")

  # get the driver to neo4j database
  driver = GraphMethods.connect_to_neo4j()

  with driver.session() as neo4j_session:

    # check if path points to an image file
    if path.is_file() and FileUtils().mimetype_is_image(path.app):
      write_single_image_to_neo4j(path, neo4j_session)

    # check if path points to a directory
    elif path.is_dir():
      # write the path level folder to neo4j
      write_single_folder_to_neo4j(path, neo4j_session)

      # collect all the existing resources in folder as a set
      existing_resources = collect_existing_resources(path, neo4j_session)

      # loop over subfolders and images within folder and write
      # information to neo4j; also return parsed resources as a set
      parsed_resources = write_folder_contents_to_neo4j(path, neo4j_session)

      # perform set difference and delete irrelevant nodes
      exclude_unneeded_resources(existing_resources, parsed_resources)

    return "done"

def write_single_image_to_neo4j(path, neo4j_session):
  """
  Write a single image to neo4j

  Parameters:
    path: GalleryPath
    neo4j_session: neo4j connection
  """

  # get the metadata for the image
  md = MetaData(path.app)

  params = build_image_params(path, md)

  neo4j_session.write_transaction(
    GraphMethods().add_image,
    **params
  )

def build_image_params(path, md):
  """
  Provide neo4j method parameters for creating an image entry

  Parameters:
    path: GalleryPath
    md: instance of MetaData class

  Returns:
    dict: neo4j params
  """

  return {
    'uri': str(path.gallery),
    'name': path.name,
    'size': md.getImageSize(),
    'title': md.getTitle(),
    'description': md.getDescription(),
    'last_modified': FileUtils().get_last_modified_datetime(path.app),
    'parent_uri': str(path.parent)
  }

def write_single_folder_to_neo4j(path, neo4j_session):
  """
  Write a single folder to neo4j

  Parameters:
    path: GalleryPath
    neo4j_session: neo4j connection
  """

  params = build_folder_params(path)

  neo4j_session.write_transaction(
    GraphMethods().add_folder,
    **params
  )

def build_folder_params(path):
  """
  Provide neo4j method parameters for creating a folder entry

  Parameters:
    path: GalleryPath

  Returns:
    dict: neo4j params
  """

  return {
    'uri': str(path.gallery),
    'name': path.name,
    'parent_uri': str(path.parent)
  }

def collect_existing_resources(path, neo4j_session):
  """
  Collect a set of resources already existing in the
  neo4j database. This will be used to compare against parsed
  set to determine which nodes can be deleted

  Parameters:
    path: GalleryPath
    neo4j_session: neo4j connection

  Returns:
    set: child resource gallery uris
  """

  resources = set()

  params = {
    'uri': str(path.gallery)
  }

  for resource in neo4j_session.read_transaction(
    GraphMethods().get_child_uris,
    **params
  ):
    resources.add(resource["child.uri"])

  resources.discard('.')

  return resources

def exclude_unneeded_resources(existing_resources, parsed_resources):
  """
  Iterate through the contents of the folder and add them to the
  neo4j database. Also, return a set of all resources added so that
  resources not parsed may be excluded from neo4j

  Parameters:
    existing_resources: set of gallery uris
    parsed_resources: set of gallery uris
  """
  items_to_delete = existing_resources - parsed_resources

  print(items_to_delete)

  for uri in items_to_delete:
    params = {
      'uri': uri
    }

    neo4j_session.write_transaction(
      GraphMethods().delete_nodes_and_descendants,
      **params
    )

def write_folder_contents_to_neo4j(path, neo4j_session):
  """
  Iterate through the contents of the folder and add them to the
  neo4j database. Also, return a set of all resources added so that
  resources not parsed may be excluded from neo4j

  Parameters:
    path: GalleryPath
    neo4j_session: neo4j connection

  Returns:
    set: child resource gallery uris
  """

  # empty set which will be populated with uris of
  # resources in folder
  contents_set = set()

  # scan the directory specified in the path for all photos
  # and folders, send this info to browser via websockets
  for child in scandir(path.app):

    child_path = GalleryPath(
      PurePath(child.path).relative_to(settings.GALLERY_BASE_DIR)
    )

    if not child_path.name.startswith('.') and child_path.is_dir():
      # write the subfolder to neo4j
      write_single_folder_to_neo4j(child_path, neo4j_session)
      # add uri to set
      contents_set.add(str(child_path.gallery))

    if not child_path.name.startswith('.') and child_path.is_file() and FileUtils().mimetype_is_image(child_path.app):
      # write the image to neo4j
      write_single_image_to_neo4j(child_path, neo4j_session)
      # if image thumbnails are missing, create them
      generate_thumbnails_if_missing(child_path)
      # add uri to set
      contents_set.add(str(child_path.gallery))

  return contents_set
