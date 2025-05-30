# backend/app.py
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Habilitar CORS para todas las rutas

@app.route('/')
def home():
    return "Prueba del backend"

if __name__ == '__main__':
    app.run(debug=True)
