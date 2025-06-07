from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..authservice import auth_usuario, crear_usuario_capturista

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
        additional_claims = {"rol": usuario_autenticado.get("rol", "desconocido")} #Se obtiene el rol del usuario
        access_token = create_access_token(
            identity=usuario_autenticado['usuario_id'],
            additional_claims=additional_claims
        )
        return jsonify(
            access_token=access_token, 
            usuario=usuario_autenticado
        ), 20
    else:
        # Si el servicio devolvió None, las credenciales son incorrectas.
        return jsonify({"msg": "Correo o contraseña incorrectos"}),401

@auth_bp.route('/signup', methods=['POST'])
def create_user_endpoint():
    data = request.get_json()
    
    required_fields = ['empresa_id', 'nombre', 'correo', 'rfc', 'password']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"msg": "No puede haber campos vacíos."}), 400
    
    empresa_id = data.get("empresa_id")
    nombre = data.get("nombre")
    correo = data.get("correo")
    rfc = data.get("rfc")
    password = data.get("password")

    resultado, status_code = crear_usuario_capturista(empresa_id, nombre, correo, rfc, password)

    return jsonify(resultado), status_code
