import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))
redis_password = os.getenv("REDIS_PASSWORD")

client = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True
)

# Prueba básica SET y GET
client.set("clave_prueba", "Hola desde Redis!")
valor = client.get("clave_prueba")
print(f"El valor de 'clave_prueba' es: {valor}")
