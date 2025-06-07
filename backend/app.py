# backend/app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
from .database import db
from .reports.routes import reportes_bp
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .auth.routes import auth_bp

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "tu_clave_secreta_aqui"
jwt = JWTManager(app) #para gestionar el login y contraseñas

CORS(app)

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return "¡El archivo principal del backend esta funcionando"

@app.route('/test_db')
def test_db_connection():
    try:
        with db.engine.connect() as connection:
            connection.execute(db.text('SELECT 1'))
        return "¡Conexión a la base de datos exitosa!"
    except Exception as e:
        return f"Error al conectar a la base de datos: {str(e)}"

app.register_blueprint(auth_bp) #Llama a los endpoints involucrados en la autenticación
app.register_blueprint(reportes_bp) #Llama a los endpoints involucrados en la generación de reportes

if __name__ == '__main__':
    with app.app_context(): # Necesario para operaciones de BD fuera de una request
        pass
    app.run(debug=True)
