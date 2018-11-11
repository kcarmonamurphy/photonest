class GraphMethods():
  """
  Module containing various methods used to control
  neo4j graph database and written in cipher language
  """

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
  def get_folders(tx, uri):
    return tx.run(
      f"""
        MATCH (folder:Folder {{ uri: "{uri}" }})-[:CONTAINS]->(child:Folder)
        RETURN child
      """
    )

  @staticmethod
  def get_images(tx, uri):
    return tx.run(
      f"""
        MATCH (folder:Folder {{ uri: "{uri}" }})-[:CONTAINS]->(child:Image)
        RETURN child
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

  @staticmethod
  def add_folder(tx, uri, name, parent_uri):
    print(" ---- adding folder ----- ", uri, name, parent_uri)
    tx.run(
      f"""
        MERGE (folder:Folder {{ uri: "{parent_uri}" }})
        MERGE (childfolder:Folder {{ uri: "{uri}" }})
        MERGE (folder)-[:CONTAINS]->(childfolder)
      """
    )