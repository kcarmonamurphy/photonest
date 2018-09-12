import os
import magic
import json

from app.metadata import MetaData
from app.path import Path

from app.thumbnails import generate_thumbnails_if_missing

from app.models import Folder, Image

from django.core.management.base import BaseCommand

from django.db.models.base import ObjectDoesNotExist

from neo4j import GraphDatabase

class Command(BaseCommand):

    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

    def handle(self, *args, **options):

        create_node()

    def create_node():

        pass
