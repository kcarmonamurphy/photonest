# photonest

Photonest is a backend service which provides a REST interface for getting picture listings and data from a file system.

It uses the neo4j graph database to cache request information.

### Running

Photonest requires Docker. In your projects directory:

1) `git clone git@github.com:kevcom/photonest.git`
2) `cd photonest`
3) `docker-compose up -d`