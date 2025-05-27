from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "neo4j+s://XXXX.databases.neo4j.io"),
    auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "tu_contraseña"))
)

def create_user(username):
    with driver.session() as session:
        session.run("MERGE (u:User {name: $username})", username=username)

def follow_user(follower, followee):
    with driver.session() as session:
        session.run("""
            MATCH (a:User {name: $follower}), (b:User {name: $followee})
            MERGE (a)-[:FOLLOWS]->(b)
        """, follower=follower, followee=followee)

def get_followers(username):
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User)<-[:FOLLOWS]-(f:User)
            WHERE u.name = $username
            RETURN f.name AS follower
        """, username=username)
        return [record["follower"] for record in result]
