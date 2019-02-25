from neo4j import GraphDatabase

class GraphMethods():
  """
  Module containing various methods used to control
  neo4j graph database and written in cipher language
  """

  def connect_to_neo4j():
    """Gets the connection to the neo4j graph database

    Returns:
        object: neo4j connection driver
    """
    connection = GraphDatabase.driver("bolt://db:7687", auth=("neo4j", "password"))
    return connection

  @staticmethod
  def delete_nodes_and_descendants(tx, uri):
    print(" --- deleting node and children ---- ", uri)
    tx.run(
      f"""
        MATCH (node {{ uri: "{uri}" }})
        MATCH (node)-[:CONTAINS*0..]->(child)
        DETACH DELETE node, child
      """
    )

  @staticmethod
  def get_child_uris(tx, uri):
    return tx.run(
      f"""
        MATCH (folder:Folder {{ uri: "{uri}" }})-[:CONTAINS]->(child)
        RETURN child.uri
      """
    )

  @staticmethod
  def get_subfolders(tx, uri):
    return tx.run(
      f"""
        MATCH (folder:Folder {{ uri: "{uri}" }})-[:CONTAINS]->(subfolder:Folder)
        RETURN subfolder
      """
    )

  @staticmethod
  def get_folder_images(tx, uri):
    return tx.run(
      f"""
        MATCH (folder:Folder {{ uri: "{uri}" }})-[:CONTAINS]->(image:Image)
        RETURN image
      """
    )

  @staticmethod
  def get_single_image(tx, uri):
    return tx.run(
      f"""
        MATCH (image:Image {{ uri: "{uri}" }})
        RETURN image
      """
    )

  @staticmethod
  def add_image(tx, uri, resource_name, size, title, description, last_modified, parent_uri, thumbnail_uri, full_image_uri):
    print(" ---- adding image ----- ", uri, resource_name, size, title, description, last_modified, parent_uri, thumbnail_uri, full_image_uri)
    tx.run(
      f"""
        MERGE (folder:Folder {{ uri: "{parent_uri}" }})
        MERGE (folder)-[:CONTAINS]->(image:Image {{  uri: "{uri}" }})
        SET image.description = "{description}",
            image.size = "{size}",
            image.title = "{title}",
            image.resource_name = "{resource_name}",
            image.last_modified = "{last_modified}",
            image.parent_uri = "{parent_uri}",
            image.thumbnail_uri = "{thumbnail_uri}",
            image.full_image_uri = "{full_image_uri}"
      """
    )

  @staticmethod
  def add_folder(tx, uri, resource_name, parent_uri):
    print(" ---- adding folder ----- ", uri, resource_name, parent_uri)
    tx.run(
      f"""
        MERGE (folder:Folder {{ uri: "{parent_uri}" }})
        MERGE (childfolder:Folder {{ uri: "{uri}" }})
        MERGE (folder)-[:CONTAINS]->(childfolder)
        SET childfolder.resource_name = "{resource_name}",
            childfolder.parent_uri = "{parent_uri}"
      """
    )
