from pathlib import PurePath

from neo4j import GraphDatabase

import logging
logging.basicConfig(level=logging.INFO)

from app.fileutils import FileUtils
from app.path import GalleryPath
from app.graphmethods import GraphMethods

def light_get(path):
  """
  Lightweight GET for any GalleryPath which provides the cached contents
  of that path from the neo4j graph database

  Parameters:
    path: GalleryPath object

  Returns:
    object: neo4j connection driver
  """

  logging.info(f" peek {path.parent_relative}/{path.relative_path})")

  # get the driver to neo4j database
  driver = GraphMethods.connect_to_neo4j()

  # open up a session to the neo4j database
  with driver.session() as neo4j_session:

    # if image, return image from neo4j as a dict
    if path.is_file() and FileUtils().mimetype_is_image(path.app):
      return get_single_image_from_neo4j(path, neo4j_session)

    # if folder, return folder contents (subfolders and images) as a list
    elif path.is_dir():
      return get_folder_contents_from_neo4j(path, neo4j_session)


def get_single_image_from_neo4j(path, neo4j_session):
  """
  Return image details, given path

  Parameters:
    path: GalleryPath

  Returns:
    dict: image details
  """

  params = {
    'uri': path.relative_path
  }

  # even though we're getting a single image, we must still use a for loop
  # simply return the first value which is the image
  for resource in neo4j_session.read_transaction(
    GraphMethods().get_single_image,
    **params
  ):
    neo4j_image = resource['image']
    image_response = build_image_response(neo4j_image)
    return image_response

def get_folder_contents_from_neo4j(path, neo4j_session):
  """
  Build the response list of subfolders and images, given a path

  Parameters:
    path: GalleryPath
    neo4j_session: neo4j connection

  Returns:
    list: individual subfolder and image dicts
  """

  # create empty response array
  response = []

  # set the parameters to be passed to neo4j methods
  params = {
    'uri': path.relative_path
  }

  # get all of the subfolders of 'path' and add them to the
  # response list
  for resource in neo4j_session.read_transaction(
    GraphMethods().get_subfolders,
    **params
  ):
    neo4j_subfolder = resource['subfolder']
    subfolder_response = build_subfolder_response(neo4j_subfolder)
    response.append(subfolder_response)

  # get all of the images of the folder at 'path' and add them
  # to the response list
  for resource in neo4j_session.read_transaction(
    GraphMethods().get_folder_images,
    **params
  ):
    neo4j_image = resource['image']
    image_response = build_image_response(neo4j_image)
    response.append(image_response)

  return response

def build_subfolder_response(subfolder):
  """
  Extract the parameters from subfolder dict

  Parameters:
    subfolder: Node type object from neo4j 

  Returns:
    dict: values to be serialized into JSON
  """

  return {
    'parent_uri': subfolder['parent_uri'],
    'uri': subfolder['uri'],
    'resource_name': subfolder['resource_name'],
    'type': 'folder'
  }

def build_image_response(image):
  """
  Extract the parameters from the image dict

  Parameters:
    image: Node type object from neo4j 

  Returns:
    dict: values to be serialized into JSON
  """

  return {
    'parent_uri': image['parent_uri'],
    'description': image['description'],
    'resource_name': image['resource_name'],
    'size': image['size'],
    'title': image['title'],
    'last_modified': image['last_modified'],
    'uri': image['uri'],
    'thumbnail_uri': image['thumbnail_uri'],
    'full_image_uri': image['full_image_uri'],
    'type': 'image'
  }
