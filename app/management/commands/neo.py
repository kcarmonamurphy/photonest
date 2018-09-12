import os
import magic
import json
from datetime import datetime
import pytz
from django.utils import timezone

from app.metadata import MetaData
from app.path import Path

from app.thumbnails import generate_thumbnails_if_missing

from django.core.management.base import BaseCommand

from neo4j import GraphDatabase

class Command(BaseCommand):

    def handle(self, *args, **options):

        parse_path(Path('albums'))

def mimetype_is_image(path):
    '''
    Accepts a vlue of os.DirEntry
    '''
    mime_type = magic.from_file(path, mime=True)
    mime_category = mime_type.split('/')
    if mime_category[0] == 'image':
        return True
    return False

def get_last_modified_datetime(path):
    epoch_time = os.path.getmtime(path)
    date_time = datetime.utcfromtimestamp(epoch_time)
    return timezone.make_aware(date_time, timezone=pytz.UTC)

def parse_path(path):

    print("PARSE_PATH ****", path.gallery.dir, path.gallery.base)

    driver = GraphDatabase.driver("bolt://db:7687")

    with driver.session() as session:

        if path.isfile() and mimetype_is_image(path.app.file):

            md = MetaData(path.app.file)
            session.write_transaction(add_image,
                uri=path.gallery.file,
                name=path.gallery.base,
                size=md.getImageSize(),
                title=md.getTitle(),
                description=md.getDescription(),
                last_modified=get_last_modified_datetime(path.app.file),
                parent_uri=path.gallery.dir
            )

        elif path.isdir():

            # scan the directory specified in the path for all photos
            # and folders, send this info to browser via websockets
            for child in os.scandir(path.app.dir):

                child_path = Path(child.path, "app")

                if not child.name.startswith('.') and child.is_dir():

                    session.write_transaction(add_folder,
                        uri=child_path.gallery.dir,
                        name=child.name,
                        parent_uri=path.gallery.dir
                    )

                if not child.name.startswith('.') and child.is_file() and mimetype_is_image(child.path):

                    md = MetaData(child_path.app.file)
                    generate_thumbnails_if_missing(child)

                    session.write_transaction(add_image,
                        uri=child_path.gallery.file,
                        name=child.name,
                        size=md.getImageSize(),
                        title=md.getTitle(),
                        description=md.getDescription(),
                        last_modified=get_last_modified_datetime(child_path.app.file),
                        parent_uri=child_path.gallery.dir
                    )

def add_image(tx, uri, name, size, title, description, last_modified, parent_uri):
    print(uri, name, size, title, description, last_modified, parent_uri)
    tx.run("MERGE (folder:Folder {uri: $parent_uri})"
        "MERGE (folder)-[:CONTAINS]->(image:Image {uri: $uri})",
        uri=uri, parent_uri=parent_uri)

def add_folder(tx, uri, name, parent_uri):
    print(uri, name, parent_uri)
    tx.run("MERGE (folder:Folder {uri: $parent_uri})"
        "MERGE (folder)-[:CONTAINS]->(childfolder:Folder {uri: $uri})",
        uri=uri, parent_uri=parent_uri)
