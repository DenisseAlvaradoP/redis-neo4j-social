from neo4j import GraphDatabase
from redis import Redis
from dotenv import load_dotenv
import os


# Cargar variables desde .env
load_dotenv()

# Neo4j config desde .env
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Redis config para Redis Cloud (SSL habilitado, sin validación estricta de certificado)
r = Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    password=os.getenv('REDIS_PASSWORD'),
)
