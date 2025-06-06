from .models import usuario, rolesEmpresa
from sqlalchemy import func
from sqlalchemy import text
from werkzeug.security import check_password_hash
from .database import db

def auth_usuario(correo_param, password_plano_param):
    """
    Verifica las credenciales de un usuario contra la base de datos usando crypt().

    Args:
        correo_param (str): El correo del usuario.
        password_plano_param (str): La contraseña en texto plano que el usuario envió.

    Returns:
        Un diccionario con los datos del usuario si la autenticación es exitosa,
        de lo contrario, devuelve None.
    """
    try:
        # 1. Construir una consulta SQL parametrizada y segura.
        #    Usamos :correo y :password como placeholders (parámetros con nombre).
        #    La función crypt(password_enviado, password_almacenado) de PostgreSQL
        #    compara la contraseña enviada con la ya hasheada en la base de datos.
        query = text("""
            SELECT usuario_id, nombre, correo, rfc
            FROM usuario
            WHERE correo = :correo AND password = crypt(:password, password)
        """)

        # 2. Ejecutar la consulta pasando los parámetros de forma segura.
        #    SQLAlchemy se encargará de escapar los valores para prevenir inyección SQL.
        #    .mappings().first() devuelve la primera fila como un diccionario o None si no hay resultados.
        resultado_usuario = db.session.execute(
            query, 
            {'correo': correo_param, 'password': password_plano_param}
        ).mappings().first()

        if resultado_usuario:
            # Si la consulta devuelve una fila, significa que el correo y la contraseña son correctos.
            # Devolvemos los datos del usuario.
            return dict(resultado_usuario)
        else:
            # Si no hay resultado, las credenciales son incorrectas.
            return None

    except Exception as e:
        print(f"Error en autenticar_usuario: {str(e)}")
        # En caso de un error de base de datos, devolvemos None.
        return None