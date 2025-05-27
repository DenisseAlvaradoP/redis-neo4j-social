from flask import Blueprint, request, jsonify
from app.redis_service import add_post, get_all_posts
from app.neo4j_service import create_user, follow_user, get_followers

main_routes = Blueprint("main", __name__)

@main_routes.route("/")
def home():
    return "API de red social con Redis y Neo4j"

@main_routes.route("/post", methods=["POST"])
def create_post():
    data = request.get_json()
    post_id = add_post(data["username"], data["content"])
    return jsonify({"message": "Post creado", "post_id": post_id})

@main_routes.route("/posts", methods=["GET"])
def posts():
    return jsonify(get_all_posts())

@main_routes.route("/user", methods=["POST"])
def user():
    data = request.get_json()
    create_user(data["username"])
    return jsonify({"message": "Usuario creado"})

@main_routes.route("/follow", methods=["POST"])
def follow():
    data = request.get_json()
    follow_user(data["follower"], data["followee"])
    return jsonify({"message": f"{data['follower']} ahora sigue a {data['followee']}"})

@main_routes.route("/followers/<username>", methods=["GET"])
def followers(username):
    return jsonify(get_followers(username))
