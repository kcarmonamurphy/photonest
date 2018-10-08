from django.core.management.base import BaseCommand

from neo4j import GraphDatabase

class Command(BaseCommand):

    def handle(self, *args, **options):

        driver = GraphDatabase.driver("bolt://db:7687", auth=("neo4j", "password"))

        with driver.session() as session:
            session.write_transaction(delete_nodes)

def delete_nodes(tx):
    tx.run("MATCH (n)"
        "DETACH DELETE n")