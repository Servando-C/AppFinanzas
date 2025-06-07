from .models import usuario, rolesEmpresa
from sqlalchemy import func
from sqlalchemy import text
from werkzeug.security import check_password_hash
from .database import db
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
        # 1. Consulta con JOIN para obtener datos de usuario y rol a la vez.
        #    - Unimos 'usuario' y 'roles_empresa' por 'usuario_id'.
        #    - Filtramos por correo y validamos la contraseña con crypt().
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
            INNER JOIN 
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
            rol_asignado = "desconocido" # Valor por defecto
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
                "empresa_id": float(usuario_data['empresa_id']),
                "rol": rol_asignado # Añadimos el rol
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