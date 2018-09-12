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

    driver = GraphDatabase.driver("bolt://db:7687")

    def handle(self, *args, **options):

        pass
