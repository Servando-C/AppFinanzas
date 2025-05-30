# backend/app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos desde variables de entorno
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Cadena de conexión para PostgreSQL
# Formato: postgresql://usuario:contraseña@host:puerto/basededatos
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desactiva el seguimiento de modificaciones de SQLAlchemy, que no es necesario y consume recursos

# Inicializar la extensión SQLAlchemy
db = SQLAlchemy(app)

# (Opcional por ahora) Modelo de prueba para verificar la conexión
# class TestConnection(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))

#     def __repr__(self):
#         return f'<Test {self.id}>'

@app.route('/')
def home():
    return "el backend esta funcionando"

@app.route('/test_db')
def test_db_connection():
    try:
        # Intenta ejecutar una consulta simple.
        # Por ejemplo, si tienes una tabla 'usuario' (o cualquier otra tabla de tu ERD),
        # podrías intentar contar sus filas. Aquí usamos una consulta cruda genérica.
        # db.session.execute('SELECT 1') # Para SQLAlchemy < 2.0
        with db.engine.connect() as connection: # Para SQLAlchemy 2.0+
            connection.execute(db.text('SELECT 1'))
        return "¡Conexión a la base de datos exitosa!"
    except Exception as e:
        return f"Error al conectar a la base de datos: {str(e)}"

if __name__ == '__main__':
    # (Opcional) Crear tablas si no existen (solo para el modelo de prueba si lo descomentas)
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
