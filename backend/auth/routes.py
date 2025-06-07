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

    # Llamar a la función de servicio que devuelve el rol
    usuario_autenticado = auth_usuario(correo, password)

    if usuario_autenticado:
        # Autenticación exitosa.
        
        # Añadimos el rol y la empresa a los 'claims' del token JWT.
        # Esto es muy útil para proteger otras rutas basadas en el rol.
        additional_claims = {
            "rol": usuario_autenticado.get("rol", "desconocido"),
            "empresa_id": usuario_autenticado.get("empresa_id")
        }

        access_token = create_access_token(
            identity=usuario_autenticado['usuario_id'],
            additional_claims=additional_claims
        )
        
        # Devolvemos el token y los datos del usuario (incluyendo su rol)
        # al frontend.
        return jsonify(
            access_token=access_token, 
            usuario=usuario_autenticado
        ), 200
    else:
        # Credenciales incorrectas. Se devuelve 401 Unauthorized.
        return jsonify({"msg": "Correo o contraseña incorrectos"}), 401

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
