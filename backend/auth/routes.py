from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..authservice import auth_usuario

# Definición del Blueprint (si no lo tienes ya)
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login_endpoint():
    data = request.get_json()
    if not data or not data.get('correo') or not data.get('password'):
        return jsonify({"msg": "Faltan correo o contraseña."}), 400

    correo = data.get("correo")
    password = data.get("password")

    # Llamar a la función de servicio para hacer la autenticación
    usuario_autenticado = auth_usuario(correo, password)

    if usuario_autenticado:
        # Si el servicio devolvió los datos del usuario, la autenticación fue exitosa.
        # Creamos el token de acceso. La 'identity' puede ser cualquier identificador único.
        # Usar el usuario_id es una buena práctica.
        access_token = create_access_token(identity=usuario_autenticado['usuario_id'])
        return jsonify(access_token=access_token), 200
    else:
        # Si el servicio devolvió None, las credenciales son incorrectas.
        return jsonify({"msg": "Correo o contraseña incorrectos"}),