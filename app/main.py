from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid

from app import models

app = FastAPI()

# Middleware CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Puedes usar ["*"] en desarrollo si deseas permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],         # Permite todos los métodos HTTP
    allow_headers=["*"],         # Permite todos los headers
)

# Token simple para ejemplo (en producción, usa JWT u otro método seguro)
API_TOKEN = "secret-token-123"

# Dependencia para verificar token en headers
def verify_token(x_token: str = Header(...)):
    if x_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

# Ruta raíz
@app.get("/")
async def root():
    return {"message": "API funcionando. Ve a /docs para la documentación."}

# Schemas para validar entrada
class UserCreate(BaseModel):
    user_id: str
    name: str
    email: str

class PostCreate(BaseModel):
    user_id: str
    content: str

class LikeCreate(BaseModel):
    user_id: str
    post_id: str

class CommentCreate(BaseModel):
    user_id: str
    post_id: str
    comment_text: str

# Crear usuario (sin token)
@app.post("/users/")
async def create_user(user: UserCreate):
    try:
        models.create_user_neo4j(user.user_id, user.name, user.email)
        models.create_user_redis(user.user_id, user.name, user.email)
        return {"message": "User created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

# Crear post (requiere token)
@app.post("/posts/", dependencies=[Depends(verify_token)])
async def create_post(post: PostCreate):
    try:
        post_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        models.create_post_neo4j(post_id, post.user_id, post.content, timestamp)
        models.create_post_redis(post_id, post.user_id, post.content, timestamp)
        return {"message": "Post created", "post_id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating post: {str(e)}")

# Dar like (requiere token)
@app.post("/likes/", dependencies=[Depends(verify_token)])
async def like_post(like: LikeCreate):
    try:
        models.like_post_neo4j(like.user_id, like.post_id)
        models.like_post_redis(like.user_id, like.post_id)
        return {"message": "Post liked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error liking post: {str(e)}")

# Comentar (requiere token)
@app.post("/comments/", dependencies=[Depends(verify_token)])
async def comment_post(comment: CommentCreate):
    try:
        timestamp = datetime.utcnow().isoformat()
        models.comment_post_neo4j(comment.user_id, comment.post_id, comment.comment_text)
        models.comment_post_redis(comment.user_id, comment.post_id, comment.comment_text, timestamp)
        return {"message": "Comment added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding comment: {str(e)}")

# Listar usuarios
@app.get("/users/")
async def list_users():
    try:
        users = models.get_all_users()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting users: {str(e)}")

# Listar posts
@app.get("/posts/")
async def list_posts():
    try:
        posts = models.get_all_posts()
        return {"posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting posts: {str(e)}")
