from .models import usuario, rolesEmpresa
from sqlalchemy import func
from sqlalchemy import text
from werkzeug.security import check_password_hash
from backend import db
from decimal import Decimal
from werkzeug.security import generate_password_hash

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
    
def crear_usuario_capturista(empresa_id, nombre, correo, rfc, password):
    try:
        if not all([empresa_id, nombre, correo, rfc, password]):
            return {"error": "Todos los campos son requeridos para poder crear un usario"}, 400
        
        emp_id = Decimal(empresa_id)

        correo_val = usuario.query.filter_by(correo = correo).first()
        rfc_val = usuario.query.filter_by(rfc = rfc).first()

        if correo_val or rfc_val:
            return {"error": "Ya hay un usuario registrado con este correo o RFC"}, 412

        sql_insert_usuario = text("""
            INSERT INTO usuario (nombre, correo, rfc, password) 
            VALUES (:nombre, :correo, :rfc, crypt(:password, gen_salt('bf')))
            RETURNING usuario_id;
        """) #SE REALIZA EL INSERT CON RAW SQL PARA CONSERVAR COMO LO QUIEREN EN LA BASE Y COMO LO RECIBE LA FUNCIÓN DE AUTH

        resultado_insert = db.session.execute(
            sql_insert_usuario,
            {'nombre': nombre, 'correo': correo, 'rfc': rfc, 'password': password}
        ).scalar_one_or_none() # .scalar_one_or_none() obtiene el primer valor de la primera fila

        if not resultado_insert:
            # Si por alguna razón el insert falla y no devuelve un ID se lanza un error
            raise Exception("No se pudo crear el usuario en la base de datos.")

        user_id_generado = resultado_insert

        #Lo útlimo que se hace es asignar el rol, primero se debe obtener el id que se le dio al usuario en la db para ponerlo en su rol

        nuevo_rol = rolesEmpresa(
            empresa_id = emp_id,
            usuario_id = user_id_generado, #ESTOS IDS LOS ASIGNO YO, NO TELCEL. LOS ASIGNO CON LOS AUTOMÁTICOS DE USUARIO Y SE FORMA LA PK COMPUESTA
            rol_capturista = 1,
            rol_admin = 0,
            rol_mvp = 0,
            rol_financiero = 0
        )

        db.session.add(nuevo_rol)
        db.session.commit()

        return {
            "mensaje": "Usuario capturista creado y rol asignado exitosamente.",
            "usuario": {
                "usuario_id": float(user_id_generado),
                "nombre": nombre,
                "correo": correo,
                "rol_asignado": "capturista"
            }
        }, 201
    
    except ValueError as ve:
        db.session.rollback()
        return {"error": f"Error en los datos de entrada: {str(ve)}"}, 400
    except Exception as e:
        db.session.rollback()
        return {"error": f"Error inesperado al crear el usuario: {str(e)}"}, 500
