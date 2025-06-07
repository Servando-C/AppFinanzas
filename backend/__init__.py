# backend/__init__.py
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import secrets

# 1. Inicializar las extensiones globalmente, pero SIN una app.
#    Ahora, cualquier archivo podrá hacer 'from backend import db'.
db = SQLAlchemy()
jwt = JWTManager()
#cors = CORS()

def create_app():
    """
    Crea y configura una instancia de la aplicación Flask.
    Este es el patrón Application Factory.
    """
    app = Flask(__name__)
    load_dotenv() # Cargar variables de entorno desde .env

    # 2. Configurar la aplicación desde variables de entorno
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_hex(16))
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")

    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. Vincular las extensiones con la aplicación creada
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {
        "origins": "*",  # Permite peticiones desde cualquier origen. Para producción final, podrías poner aquí tu dominio.
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], # Permite todos los métodos comunes
        "allow_headers": ["Content-Type", "Authorization"] # Permite los headers necesarios para JSON y tokens JWT
    }})

    with app.app_context():
        # 4. Importar y registrar los Blueprints aquí dentro
        #    para evitar importaciones circulares.
        from .auth.routes import auth_bp
        from .reports.routes import reportes_bp

        # ¡No olvides añadir el prefijo /api aquí!
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(reportes_bp, url_prefix='/api/reportes')

        # Ruta de prueba para verificar que la app funciona
        @app.route('/api/health')
        def health_check():
            return jsonify({"status": "healthy"}), 200

    return app
