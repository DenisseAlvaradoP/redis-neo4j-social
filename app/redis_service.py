import redis
import os

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "redis-XXXX.c1.europe-west1-1.gce.cloud.redislabs.com"),
    port=int(os.getenv("REDIS_PORT", 12345)),
    password=os.getenv("REDIS_PASSWORD", "tu_contraseña"),
    decode_responses=True
)

def add_post(username, content):
    post_id = redis_client.incr("next_post_id")
    redis_client.hmset(f"post:{post_id}", {"username": username, "content": content})
    redis_client.lpush("posts", post_id)
    return post_id

def get_all_posts():
    post_ids = redis_client.lrange("posts", 0, -1)
    posts = []
    for pid in post_ids:
        post = redis_client.hgetall(f"post:{pid}")
        post["id"] = pid
        posts.append(post)
    return posts
