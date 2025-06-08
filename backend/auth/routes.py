from ..models import usuario, rolesEmpresa
from sqlalchemy import func
from sqlalchemy import text
from werkzeug.security import check_password_hash
from backend import db
from decimal import Decimal
from werkzeug.security import generate_password_hash
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..authservice import auth_usuario, crear_usuario_capturista


# Definición del Blueprint (si no lo tienes ya)
auth_bp = Blueprint('auth_bp', __name__)

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


def auth_usuario(correo_param, password_plano_param):
    """
    Verifica las credenciales de un usuario y obtiene su rol único.

    Args:
        correo_param (str): El correo del usuario.
        password_plano_param (str): La contraseña en texto plano.

    Returns:
        Un diccionario con los datos del usuario y su rol si la autenticación
        es exitosa; de lo contrario, devuelve None.
    """
    try:
        # 1. Consulta SQL cruda con JOIN para obtener datos de usuario y rol a la vez.
        #    - Se usa LEFT JOIN para ser más robusto: devolverá al usuario incluso si por error no tuviera un rol asignado.
        #    - Se usan los nombres de tabla completos como solicitaste.
        query = text("""
            SELECT 
                usuario.usuario_id, 
                usuario.nombre, 
                usuario.correo, 
                usuario.rfc,
                roles_empresa.empresa_id,
                roles_empresa.rol_capturista, 
                roles_empresa.rol_admin, 
                roles_empresa.rol_mvp, 
                roles_empresa.rol_financiero
            FROM 
                usuario
            LEFT JOIN 
                roles_empresa ON usuario.usuario_id = roles_empresa.usuario_id
            WHERE 
                usuario.correo = :correo AND usuario.password = crypt(:password, usuario.password)
        """)
        
        # 2. Ejecutamos la consulta. Usamos .first() porque esperamos un solo rol por usuario.
        resultado_db = db.session.execute(
            query,
            {'correo': correo_param, 'password': password_plano_param}
        ).mappings().first()

        if resultado_db:
            # 3. Si encontramos un resultado, procesamos los datos.
            usuario_data = dict(resultado_db)
            
            # Determinar el nombre del rol a partir de las columnas booleanas
            rol_asignado = "desconocido" # Valor por defecto si no tiene rol o ninguno es True
            if usuario_data.get('rol_capturista'):
                rol_asignado = "capturista"
            elif usuario_data.get('rol_admin'):
                rol_asignado = "admin"
            elif usuario_data.get('rol_mvp'):
                rol_asignado = "mvp"
            elif usuario_data.get('rol_financiero'):
                rol_asignado = "financiero"
            
            # Preparamos el diccionario final para devolver
            usuario_final = {
                "usuario_id": float(usuario_data['usuario_id']),
                "nombre": usuario_data['nombre'],
                "correo": usuario_data['correo'],
                "rfc": usuario_data['rfc'],
                "empresa_id": float(usuario_data['empresa_id']) if usuario_data['empresa_id'] else None,
                "rol": rol_asignado
            }
            return usuario_final
        else:
            # Si no hay resultado, las credenciales son incorrectas.
            return None

    except Exception as e:
        print(f"Error en auth_usuario: {str(e)}")
        return None
