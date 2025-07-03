from app.database import driver, r
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

def redis_key(entity, identifier, suffix=None):
    key = f"{entity}:{identifier}"
    if suffix:
        key += f":{suffix}"
    return key

# Usuarios
def create_user_neo4j(user_id, name, email):
    try:
        with driver.session() as session:
            # Verificar si ya existe user_id o email
            existing = session.run(
                """
                MATCH (u:User)
                WHERE u.user_id = $user_id OR u.email = $email
                RETURN u LIMIT 1
                """,
                user_id=user_id,
                email=email
            )
            if existing.single() is not None:
                raise ValueError("User with same user_id or email already exists")

            # Crear usuario si no existe
            session.run(
                "CREATE (u:User {user_id: $user_id, name: $name, email: $email})",
                user_id=user_id, name=name, email=email
            )
    except Exception as e:
        logger.error(f"[Neo4j] Error al crear usuario: {e}")
        raise

def create_user_redis(user_id, name, email):
    try:
        key = redis_key("user", user_id)
        if r.exists(key):
            raise ValueError("User with same user_id already exists in Redis")
        r.hset(key, mapping={"name": name, "email": email})
    except Exception as e:
        logger.error(f"[Redis] Error al guardar usuario: {e}")
        raise

def get_all_users():
    users = []
    try:
        with driver.session() as session:
            result = session.run(
                "MATCH (u:User) RETURN u.user_id AS user_id, u.name AS name, u.email AS email"
            )
            for record in result:
                users.append({
                    "user_id": record["user_id"],
                    "name": record["name"],
                    "email": record["email"]
                })
    except Exception as e:
        logger.error(f"[Neo4j] Error al obtener usuarios: {e}")
        raise
    return users

# Posts
def create_post_neo4j(post_id, user_id, content, timestamp):
    try:
        with driver.session() as session:
            result = session.run(
                "MATCH (u:User {user_id: $user_id}) RETURN u", user_id=user_id
            )
            if result.single() is None:
                raise ValueError(f"Usuario {user_id} no existe en Neo4j")

            session.run("""
                MATCH (u:User {user_id: $user_id})
                CREATE (p:Post {post_id: $post_id, content: $content, timestamp: $timestamp})
                CREATE (u)-[:POSTED]->(p)
            """, post_id=post_id, user_id=user_id, content=content, timestamp=timestamp)
    except Exception as e:
        logger.error(f"[Neo4j] Error al crear post: {e}")
        raise

def create_post_redis(post_id, user_id, content, timestamp):
    try:
        r.hset(redis_key("post", post_id), mapping={
            "content": content, "user_id": user_id, "timestamp": timestamp
        })
    except Exception as e:
        logger.error(f"[Redis] Error al guardar post: {e}")
        raise

def get_all_posts():
    posts = []
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (p:Post)<-[:POSTED]-(u:User)
                RETURN p.post_id AS post_id, p.content AS content, p.timestamp AS timestamp, u.user_id AS user_id, u.name AS user_name
                ORDER BY p.timestamp DESC
                LIMIT 100
            """)
            for record in result:
                post_id = record["post_id"]

                # Contar likes en Redis
                like_count = r.scard(redis_key("post", post_id, "likes"))

                # Obtener comentarios en Redis (lista)
                comments_json = r.lrange(redis_key("post", post_id, "comments"), 0, -1)
                comments = [json.loads(c) for c in comments_json]

                posts.append({
                    "post_id": post_id,
                    "content": record["content"],
                    "timestamp": record["timestamp"],
                    "user_id": record["user_id"],
                    "user_name": record["user_name"],
                    "like_count": like_count,
                    "comments": comments
                })
    except Exception as e:
        logger.error(f"[Neo4j] Error al obtener posts: {e}")
        raise
    return posts


# Likes
def like_post_neo4j(user_id, post_id):
    try:
        with driver.session() as session:
            session.run("""
                MATCH (u:User {user_id: $user_id}), (p:Post {post_id: $post_id})
                MERGE (u)-[:LIKES]->(p)
            """, user_id=user_id, post_id=post_id)
    except Exception as e:
        logger.error(f"[Neo4j] Error al dar like: {e}")
        raise

def like_post_redis(user_id, post_id):
    try:
        r.sadd(redis_key("post", post_id, "likes"), user_id)
    except Exception as e:
        logger.error(f"[Redis] Error al registrar like: {e}")
        raise

# Comentarios
def comment_post_neo4j(user_id, post_id, comment_text):
    try:
        with driver.session() as session:
            session.run("""
                MATCH (u:User {user_id: $user_id}), (p:Post {post_id: $post_id})
                CREATE (u)-[:COMMENTED {comment_text: $comment_text}]->(p)
            """, user_id=user_id, post_id=post_id, comment_text=comment_text)
    except Exception as e:
        logger.error(f"[Neo4j] Error al comentar: {e}")
        raise

def comment_post_redis(user_id, post_id, comment_text, timestamp):
    try:
        comment = {
            "user_id": user_id,
            "comment_text": comment_text,
            "timestamp": timestamp
        }
        r.rpush(redis_key("post", post_id, "comments"), json.dumps(comment))
    except Exception as e:
        logger.error(f"[Redis] Error al guardar comentario: {e}")
        raise
