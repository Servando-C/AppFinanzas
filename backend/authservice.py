from .models import usuario, rolesEmpresa
from sqlalchemy import func
from sqlalchemy import text
from werkzeug.security import check_password_hash
from .database import db
from decimal import Decimal
from werkzeug.security import generate_password_hash

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
    
def crear_usuario_capturista(empresa_id, nombre, correo, rfc, password):
    try:
        if not all([empresa_id, nombre, correo, rfc, password]):
            return {"error": "Todos los campos son requeridos para poder crear un usario"}, 400
        
        emp_id = Decimal(empresa_id)

        correo_val = usuario.query.filter_by(correo = correo).first()
        rfc_val = usuario.query.filter_by(rfc = rfc).first()

        if correo_val or rfc_val:
            return {"error": "Ya hay un usuario registrado con este correo o RFC"}, 412

        nuevo_usuario = usuario(
            #EL ID DE USUARIO ES AUTOGENERADO POR LA BASE DE DATOS
            nombre = nombre,
            correo = correo,
            rfc = rfc,
            password = password #LE ENTENDÍA A TELCEL QUE EL ENCRIPTA POR ESO REVISAR SI MANDAR EN CLARO O HASHEED
        )
        
        db.session.add(nuevo_usuario)
        db.session.flush()

        #Lo útlimo que se hace es asignar el rol, primero se debe obtener el id que se le dio al usuario en la db para ponerlo en su rol

        nuevo_rol = rolesEmpresa(
            empresa_id = emp_id,
            usuario_id = nuevo_usuario.usuario_id, #ESTOS IDS LOS ASIGNO YO, NO TELCEL
            rol_capturista = True,
            rol_admin = False,
            rol_mvp = False,
            rol_financiero = False
        )

        db.session.add(nuevo_rol)
        db.session.commit()

        return {
            "mensaje": "Usuario capturista creado y rol asignado exitosamente.",
            "usuario": {
                "usuario_id": float(nuevo_usuario.usuario_id),
                "nombre": nuevo_usuario.nombre,
                "correo": nuevo_usuario.correo,
                "rol_asignado": "capturista"
            }
        }, 201
    
    except ValueError as ve:
        db.session.rollback()
        return {"error": f"Error en los datos de entrada: {str(ve)}"}, 400
    except Exception as e:
        db.session.rollback()
        return {"error": f"Error inesperado al crear el usuario: {str(e)}"}, 500