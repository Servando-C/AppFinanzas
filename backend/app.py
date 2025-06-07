# backend/app.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import secrets

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Inicializar las extensiones SIN una aplicación.
# Se vincularán a la aplicación dentro de la función factory.
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

# --- LA FUNCIÓN "APPLICATION FACTORY" ---
def create_app():
    """Crea y configura una instancia de la aplicación Flask."""

    app = Flask(__name__)

    # --- Configuración de la Aplicación ---
    # Carga la SECRET_KEY y las credenciales de la base de datos desde .env
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_hex(16))
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_hex(16)) # JWT también usa esta clave

    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Vincular las Extensiones con la Aplicación ---
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # --- Registrar los Blueprints ---
    with app.app_context():
        # Importamos los blueprints aquí dentro para evitar importaciones circulares
        from auth.routes import auth_bp
        from reports.routes import reportes_bp

        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(reportes_bp, url_prefix='/api/reportes')

        # Ruta de prueba para verificar que la app funciona
        @app.route('/health')
        def health_check():
            return "Health check OK"

    return app

# --- Punto de Entrada para Gunicorn y Desarrollo Local ---
# Creamos la instancia de la app llamando a la factory
app = create_app()

if __name__ == '__main__':
    # Esto permite que sigas usando 'python backend/app.py' para desarrollo local
    app.run(debug=True)
