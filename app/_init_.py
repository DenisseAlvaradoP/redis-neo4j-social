from flask import Flask
from app.routes import main_routes
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()  # Carga las variables del archivo .env

    app = Flask(__name__)

    # Ahora las variables de entorno están disponibles vía os.getenv()

    app.register_blueprint(main_routes)

    return app
