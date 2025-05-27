from app import neo4j_service as db

# Crear usuarios
db.create_user("Alice")
db.create_user("Bob")
db.create_user("Charlie")

# Crear relaciones
db.follow_user("Bob", "Alice")
db.follow_user("Charlie", "Alice")

# Obtener seguidores
followers = db.get_followers("Alice")
print("Seguidores de Alice:", followers)
