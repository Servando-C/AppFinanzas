from .models import *
from sqlalchemy import func
from .app import db
from decimal import Decimal #Ya que se maneja dinero

# --- Constantes para Clasificación de Bienes (Tipos de Cuenta para Activos) ---
# Estos son los valores que esperarías en la columna bien.tipo_bien
TIPO_BIEN_EFECTIVO_EQUIVALENTES = "EFECTIVO_Y_EQUIVALENTES" # Aunque el efectivo principal vendrá de tesorería
TIPO_BIEN_INMUEBLES = "BIENES_INMUEBLES"
TIPO_BIEN_MUEBLES_EQUIPOS = "MUEBLES_Y_EQUIPOS"
TIPO_BIEN_INVENTARIO = "INVENTARIO"
TIPO_BIEN_CUENTAS_POR_COBRAR = "CUENTAS_POR_COBRAR" # Si decides implementarlo
TIPO_BIEN_GASTO = "GASTO" # Para identificar adquisiciones que son gastos y no activos

# Podrías tener un mapeo más estructurado si necesitas agruparlos por Activo Circulante/Fijo
CLASIFICACION_ACTIVOS = {
    TIPO_BIEN_EFECTIVO_EQUIVALENTES: "ACTIVO_CIRCULANTE",
    TIPO_BIEN_INVENTARIO: "ACTIVO_CIRCULANTE",
    TIPO_BIEN_CUENTAS_POR_COBRAR: "ACTIVO_CIRCULANTE",
    TIPO_BIEN_INMUEBLES: "ACTIVO_FIJO",
    TIPO_BIEN_MUEBLES_EQUIPOS: "ACTIVO_FIJO",
}

#EN ESTE ARCHIVO ESTARÁ LA LÓGICA DE NEGOCIO COMO FUNCIONES, LAS FUNCIONES CORE ES RECIBIR UNA NUEVA ADQUISICION Y EL CALCULO DEL BALANCE,
#EL CALCULO DEL BALANCE DEBE EJECUTARSE SIEMPRE QUE SE PIDE O SE PIDE GENERAR UN REPORTE

# backend/services.py
# ... (importaciones y constantes) ...

def nueva_empresa(nombre_empresa, dueño_empresa, correo_empresa, telefono_empresa, direccion_empresa, rfc_empresa):
    """Crea una nueva empresa y la guarda en la base de datos."""
    try:
        # Validaciones básicas (puedes expandirlas)
        if not all([nombre_empresa, dueño_empresa, correo_empresa, rfc_empresa]):
            return {"error": "Nombre, dueño, correo y RFC son requeridos para la empresa."}, 400

        # Verificar si ya existe una empresa con el mismo RFC (asumiendo RFC es único para empresa)
        existente = empresa.query.filter_by(rfc=rfc_empresa).first()
        if existente:
            return {"error": f"Ya existe una empresa con el RFC {rfc_empresa}"}, 409 # Conflict

        nueva_emp = empresa(
            nombre=nombre_empresa,
            dueño=dueño_empresa,
            correo=correo_empresa,
            telefono=telefono_empresa, # Asegúrate que el tipo de dato coincida (Numeric)
            direccion=direccion_empresa,
            rfc=rfc_empresa
        )

        #VER SI EL ID SE GENERA SOLO EN LA BASE DE DATOS O SI SE DEBE HACER ALGO

        db.session.add(nueva_emp)
        db.session.commit()
        return {
            "mensaje": "Empresa creada exitosamente",
            "empresa": {
                "empresa_id": float(nueva_emp.empresa_id), # Convertir Decimal a float para JSON
                "nombre": nueva_emp.nombre,
                "rfc": nueva_emp.rfc
            }
        }, 201 # Created
    except Exception as e:
        db.session.rollback()
        print(f"Error en nueva_empresa: {str(e)}")
        return {"error": f"Error interno al crear la empresa: {str(e)}"}, 500

def nuevo_proyecto(empresa_id_param, nombre_proyecto, fecha_creacion_str, capital_inicial_asignado_str):
    """Crea un nuevo proyecto para una empresa y lo guarda en la base de datos."""
    try:
        #La primera validación comprueba si existe la empresa a la que se quiere agregar el proyecto
        empresa_obj = empresa.query.get(empresa_id_param)
        if not empresa_obj:
            return {"error": f"Empresa con id {empresa_id_param} no encontrada."}, 404

        if not nombre_proyecto or not fecha_creacion_str:
            return {"error": "Nombre del proyecto y fecha de creación son requeridos."}, 400

        try:
            fecha_creacion_obj = datetime.datetime.strptime(fecha_creacion_str, '%Y-%m-%d').date()
            capital_asignado_decimal = Decimal(capital_inicial_asignado_str)
        except ValueError:
            return {"error": "Formato de fecha_creacion incorrecto. Usar YYYY-MM-DD."}, 400

        try:
            capital_asignado = Decimal(capital_inicial_asignado_str)
        except:
            return {"error": "Capital inicial asignado debe ser un número."}, 400
        
        #SE DEBE ANALIZAR QUE ONDA CON LAS DOS PK POR PROYECTO, SE GENERA UNA COMPUESTA O CADA PROYECTO TIENE SU NUMERACIÓN PERO PUEDEN REPETIRSE EN LAS GLOBALES???
        nuevo_proy = proyecto(
            # proyecto_id=nuevo_proyecto_id_local, # Si lo generamos
            empresa_id=empresa_obj.empresa_id,
            nombre=nombre_proyecto,
            fecha_creacion=fecha_creacion_obj,
            capital_disponible=capital_asignado
        )
        db.session.add(nuevo_proy)
        db.session.flush()

        if capital_asignado_decimal > Decimal('0.00'):
            registrar_o_actualizar_tesoreria(
                proyecto_id_param=nuevo_proy.proyecto_id,
                empresa_id_param=empresa_obj.empresa_id,
                fecha_movimiento=fecha_creacion_obj,
                monto_entrada_mov=capital_asignado_decimal,
                monto_salida_mov=Decimal('0.00'),
                descripcion_mov=f"Capital inicial para proyecto: {nombre_proyecto}",
                observaciones_mov="Registro automático por creación de proyecto"
            )

        db.session.commit()

        return {
            "mensaje": "Proyecto creado y capital inicial registrado en tesorería.",
            "proyecto": {
                "proyecto_id": float(nuevo_proy.proyecto_id),
                "empresa_id": float(nuevo_proy.empresa_id),
                "nombre": nuevo_proy.nombre,
                "capital_inicial_registrado_tesoreria": str(capital_asignado_decimal) if capital_asignado_decimal > Decimal('0.00') else "0.00"
            }
        }, 201
    except Exception as e:
        db.session.rollback()
        print(f"Error en nuevo_proyecto: {str(e)}")
        return {"error": f"Error interno al crear el proyecto: {str(e)}"}, 500.

def registrar_o_actualizar_tesoreria(
    proyecto_id_param,
    empresa_id_param,
    fecha_movimiento, # objeto date
    monto_entrada_mov, # Decimal
    monto_salida_mov,  # Decimal
    descripcion_mov,
    observaciones_mov=None
):
    """
    Registra un movimiento de tesorería creando un nuevo snapshot o actualizando
    uno existente para la misma fecha.
    Maneja los acumulados de entradas, salidas y el monto disponible.
    """
    try:
        # Validar que el proyecto exista
        proyecto_obj = proyecto.query.filter_by(
            proyecto_id=proyecto_id_param,
            empresa_id=empresa_id_param
        ).first()
        if not proyecto_obj:
            raise ValueError(f"Proyecto con id {proyecto_id_param} para empresa {empresa_id_param} no encontrado.")

        monto_entrada_mov = Decimal(monto_entrada_mov)
        monto_salida_mov = Decimal(monto_salida_mov)

        # Buscar el snapshot de tesorería más reciente o antes de la fecha_movimiento
        ultimo_snapshot_tesoreria = tesoreria.query.filter(
            tesoreria.proyecto_id == proyecto_obj.proyecto_id,
            tesoreria.empresa_id == proyecto_obj.empresa_id,
            tesoreria.fecha_registro <= fecha_movimiento
        ).order_by(tesoreria.fecha_registro.desc(), tesoreria.tesoreria_id.desc()).first() # Ordenar por ID si hay varios en misma fecha

        monto_disponible_previo = Decimal('0.00')
        monto_entradas_acum_previo = Decimal('0.00')
        monto_salidas_acum_previo = Decimal('0.00')

        if ultimo_snapshot_tesoreria:
            monto_disponible_previo = Decimal(ultimo_snapshot_tesoreria.monto_disponible)
            monto_entradas_acum_previo = Decimal(ultimo_snapshot_tesoreria.monto_entradas)
            monto_salidas_acum_previo = Decimal(ultimo_snapshot_tesoreria.monto_salidas)

        # Determinar si se actualiza un snapshot del mismo día o se crea uno nuevo
        snapshot_del_dia_a_actualizar = None
        if ultimo_snapshot_tesoreria and ultimo_snapshot_tesoreria.fecha_registro == fecha_movimiento:
            snapshot_del_dia_a_actualizar = ultimo_snapshot_tesoreria
        
        if snapshot_del_dia_a_actualizar:
            # Actualizar el snapshot existente para esta fecha
            snapshot_del_dia_a_actualizar.monto_entradas = monto_entradas_acum_previo + monto_entrada_mov
            snapshot_del_dia_a_actualizar.monto_salidas = monto_salidas_acum_previo + monto_salida_mov
            snapshot_del_dia_a_actualizar.monto_disponible = monto_disponible_previo + monto_entrada_mov - monto_salida_mov
            snapshot_del_dia_a_actualizar.descripcion = descripcion_mov 
            snapshot_del_dia_a_actualizar.observaciones = observaciones_mov
            print(f"Actualizando tesorería para P:{proyecto_obj.proyecto_id}, F:{fecha_movimiento}")
        else:
            # Crear un nuevo snapshot de tesorería
            # Si el ultimo_snapshot_tesoreria es de una fecha anterior, usamos sus acumulados como base.
            # Si no hay ultimo_snapshot_tesoreria, los previos son 0.
            nuevo_monto_entradas_acum = monto_entradas_acum_previo + monto_entrada_mov
            nuevo_monto_salidas_acum = monto_salidas_acum_previo + monto_salida_mov
            nuevo_monto_disponible = monto_disponible_previo + monto_entrada_mov - monto_salida_mov
            
            # Si el ultimo_snapshot_tesoreria es de una fecha estrictamente anterior,
            # el monto_disponible_previo ya es el correcto para iniciar el cálculo del nuevo día.
            # Si no hay ultimo_snapshot, monto_disponible_previo es 0.

            nuevo_snapshot = tesoreria(
                descripcion=descripcion_mov,
                monto_disponible=nuevo_monto_disponible,
                monto_entradas=nuevo_monto_entradas_acum,
                monto_salidas=nuevo_monto_salidas_acum,
                fecha_registro=fecha_movimiento,
                observaciones=observaciones_mov,
                proyecto_id=proyecto_obj.proyecto_id,
                empresa_id=proyecto_obj.empresa_id
            )
            db.session.add(nuevo_snapshot)
            print(f"Creando nuevo snapshot de tesorería para P:{proyecto_obj.proyecto_id}, F:{fecha_movimiento}")
        
        # El commit se hará en la función que llama a esta, ej. nuevo_proyecto o agregar_adquisicion
        return True # O el objeto tesorería creado/actualizado

    except ValueError as ve:
        print(f"Error de validación en tesorería: {str(ve)}")
        raise ve # Relanzar para que la función que llama maneje el rollback y la respuesta
    except Exception as e:
        print(f"Error en registrar_o_actualizar_tesoreria: {str(e)}")
        # import traceback
        # traceback.print_exc()
        raise e # Relanzar para que la función que llama maneje el rollback y la respuesta

def get_or_create_bien(nombre_bien, tipo_bien_param, desc_tipo):
    """Busca un bien por nombre y tipo, si no existe, lo crea."""
    # Validar que tipo_bien_param sea uno de los esperados (según tus constantes)
    if not (tipo_bien_param in CLASIFICACION_ACTIVOS or tipo_bien_param == TIPO_BIEN_GASTO): #comprueba si no esta en las constantes, pero debo analizar cuales usar
         # Podrías añadir más tipos válidos si es necesario
        raise ValueError(f"Tipo de bien '{tipo_bien_param}' no reconocido.")

    bien_obj = bien.query.filter_by(nombre=nombre_bien, tipo_bien=tipo_bien_param).first()
    if not bien_obj:
        bien_obj = bien(
            nombre=nombre_bien,
            tipo_bien=tipo_bien_param,
            desc_tipo=desc_tipo
        )
        # Asumimos que bien_id es autoincremental
        db.session.add(bien_obj)
    return bien_obj

def get_or_create_forma_pago(tipo_char):
    """Busca una forma de pago por su tipo CHAR(1), si no existe, la crea."""
    if not tipo_char or len(tipo_char) != 1:
        raise ValueError("No se reconoce el tipo de forma de pago")

    fp_obj = formaDePago.query.filter_by(tipo=tipo_char).first()
    if not fp_obj:
        fp_obj = formaDePago(tipo=tipo_char)
        # Asumimos que forma_pago_id es autoincremental
        db.session.add(fp_obj)
    return fp_obj

def get_default_status_adquisicion():
    """Obtiene el statusAdquisicion por defecto para nuevas adquisiciones."""
    # Debe decidirse cuales son las claves  o descripciones para el estado por defecto, como para eñ restp
    status_clave_defecto = "ACT"
    status_obj = statusAdquisicion.query.filter_by(clave=status_clave_defecto).first()
    if not status_obj:
        #¿QUÉ DEBERÍA PASAR SI NO EXISTE?
        #ME FALTA AGREGAR ACTIVO PERO NO TENGO IDEA DE QUE SIGNIFICA ESO EN STATUS
        raise ValueError(f"Estado de adquisición por defecto con clave '{status_clave_defecto}' no encontrado.")
    return status_obj

#PEDIR QUE EN LA BASE CAMBIEN AÑOS PAGOS DE ADQUISICION POR MESES(PERIODO)
#PARECE QUE LA SUMA DEL FINANCIAMIENTO DE TODAS LAS ADQUISICIONES ES EL TOTAL PASIVO, CADA FINANCIAMIENTO, UN PASIVO
#USARE TIPO_BIEN COMO EL TIPO DE CUENTA PARA PRESENTAR LOS ACTIVOS Y LA FUENTE DE FINANCIAMIENTO PARA PRESENTAR LAS DEUDAS
def agregar_adquisicion(
    empresa_id_param, proyecto_id_param,
    nombre_bien_param, tipo_bien_param, desc_tipo_bien_param,
    monto_total_str, monto_inicial_str, fecha_adquisicion_str,
    forma_pago_char_param,
    meses_pago_param, numero_pagos_param, # meses_pago es el antiguo anios_pagos
    tiene_financiamiento=False, #Los siguientes parametros se ponene por default en none, por si no hay financiamiento
    fuente_financiamiento_param=None,
    porcentaje_financiamiento_str=None,
    monto_financiado_str=None
):
    """Agrega una nueva adquisición, su posible financiamiento y actualiza dependencias."""
    try:
        # Validar existencia de empresa y proyecto
        proyecto_obj = proyecto.query.filter_by(
            proyecto_id=proyecto_id_param, 
            empresa_id=empresa_id_param
        ).first()
        if not proyecto_obj:
            return {"error": f"Proyecto con id {proyecto_id_param} para empresa {empresa_id_param} no encontrado."}, 404

        # Convertir y validar datos numéricos y de fecha
        try:
            monto_total = Decimal(monto_total_str)
            monto_inicial = Decimal(monto_inicial_str)
            fecha_adquisicion = datetime.datetime.strptime(fecha_adquisicion_str, '%Y-%m-%d').date()
        except (ValueError, TypeError) as e:
            return {"error": f"Error en formato de monto, fecha o pagos: {e}"}, 400
        
        if monto_inicial > monto_total:
            raise ValueError("El monto inicial no puede ser mayor al monto total.")
        
        # 1. Obtener/Crear Bien
        bien_obj = get_or_create_bien(nombre_bien_param, tipo_bien_param, desc_tipo_bien_param)

        # 2. Obtener/Crear Forma de Pago
        forma_pago_obj = get_or_create_forma_pago(forma_pago_char_param)

        # 3. Obtener Status Adquisición por defecto
        status_adq_obj = get_default_status_adquisicion()

        # 4. Crear Adquisición
        # Se asume de momento, como para el resto de inserciones que el id es autoincremental
        nueva_adq = adquisicion(
            monto_total=monto_total,
            monto_inicial=monto_inicial,
            fecha_adquisicion=fecha_adquisicion,
            numero_pagos=numero_pagos_param, # Tu modelo lo tiene como Numeric(2,0)
            anios_pagos=meses_pago_param, # Usando anios_pagos para meses_pago de momento
            proyecto_id=proyecto_obj.proyecto_id,
            empresa_id=proyecto_obj.empresa_id,
            bien_id=bien_obj.bien_id,
            forma_pago_id=forma_pago_obj.forma_pago_id,
            status_adquisicion_id=status_adq_obj.status_adquisicion_id
        )
        db.session.add(nueva_adq)
        # se hace flush para obtener el nueva_adq.adquisicion_id si es autoincrementa y existe financiamiento
        db.session.flush() 

        # 5. Crear Financiamiento si aplica
        financiamiento_creado = None
        if tiene_financiamiento and monto_financiado_str and fuente_financiamiento_param:
            try:
                monto_financiado = Decimal(monto_financiado_str)
                porcentaje_fin = Decimal(porcentaje_financiamiento_str)
            except (ValueError, TypeError):
                 db.session.rollback()
                 return {"error": "Monto de financiamiento debe ser un número o el porcentaje es incorrecto."}, 400

            if monto_total == monto_inicial + monto_financiado: #Se valida que todos los montos cuadren para añadir el financiamiento
                # una vez más, se asume el id autoincremental
                nuevo_fin = financiamiento(
                    fuente=fuente_financiamiento_param,
                    porcentaje=porcentaje_fin,
                    monto_financiado=monto_financiado,
                    adquisicion_id=nueva_adq.adquisicion_id # Usar el ID de la adquisición recién creada
                )
                db.session.add(nuevo_fin)
                financiamiento_creado = nuevo_fin

           #ASUMO QUE E SERÁ EFECTIVO EN "FORMA_PAGO" PERO LES DEBO PREGUNTAR 
            if forma_pago_obj.tipo == 'E' and monto_inicial > Decimal('0.00'):
                registrar_o_actualizar_tesoreria(
                    proyecto_id_param=nueva_adq.proyecto_id,
                    empresa_id_param=nueva_adq.empresa_id,
                    fecha_movimiento=fecha_adquisicion,
                    monto_entrada_mov=Decimal('0.00'),
                    monto_salida_mov=monto_inicial, # El pago inicial sale de tesorería
                    descripcion_mov=f"Pago inicial adquisición: {bien_obj.nombre}",
                    observaciones_mov=f"Adquisición ID: {nueva_adq.adquisicion_id}"
                )

        #SE HACE COMMIT AQUÍ PARA TODOS LOS INSERTS DE LAS FUNCIONES USADAS, Y LOS QUE SE REALIZAN EN ESTA MISMA
        db.session.commit()

        adq_data = {
            "adquisicion_id": float(nueva_adq.adquisicion_id),
            "monto_total": str(nueva_adq.monto_total),
            "bien_nombre": bien_obj.nombre,
            "proyecto_id": float(nueva_adq.proyecto_id)
        }
        if financiamiento_creado:
            adq_data["financiamiento_id"] = float(financiamiento_creado.financiamiento_id)
            adq_data["monto_financiado"] = str(financiamiento_creado.monto_financiado)

        return {"mensaje": "Adquisición agregada y movimiento de tesorería (si aplica) registrado.", "adquisicion": adq_data}, 201

    except ValueError as ve: # Errores de validación 
        db.session.rollback()
        return {"error": str(ve)}, 400
    except Exception as e:
        db.session.rollback()
        print(f"Error en agregar_adquisicion: {str(e)}")
        # Considera loggear el traceback completo aquí para depuración: import traceback; traceback.print_exc()
        return {"error": f"Error interno al agregar la adquisición: {str(e)}"}, 500

def calcular_balance_general(empresa_id, proyecto_id):
    return

def get_balance_actual():
    return

def generar_reporte_PDF():
    return



