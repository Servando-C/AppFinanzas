from .models import *
from sqlalchemy import func
from backend import db
from decimal import Decimal #Ya que se maneja dinero
from datetime import datetime, date
from flask import jsonify
from fpdf import FPDF # Para generar PDF

# --- Constantes para Clasificación de Bienes (Tipos de Cuenta para Activos) ---
# Estos son los valores que esperarías en la columna bien.tipo_bien
TIPO_BIEN_EFECTIVO_EQUIVALENTES = "EFECTIVO_Y_EQUIVALENTES" # Aunque el efectivo principal vendrá de tesorería
TIPO_BIEN_INMUEBLES = "BIENES_INMUEBLES"
TIPO_BIEN_MUEBLES_EQUIPOS = "MUEBLES_Y_EQUIPOS"
TIPO_BIEN_INVENTARIO = "INVENTARIO"
TIPO_BIEN_CUENTAS_POR_COBRAR = "CUENTAS_POR_COBRAR" # Si decides implementarlo
TIPO_BIEN_GASTO = "GASTO" # Para identificar adquisiciones que son gastos y no activos

# Lista de tipos de bien que se consideran activos para el Balance General
TIPOS_BIEN_ACTIVOS = [
    TIPO_BIEN_EFECTIVO_EQUIVALENTES, # Aunque se maneje desde tesorería, es bueno tenerlo
    TIPO_BIEN_INMUEBLES,
    TIPO_BIEN_MUEBLES_EQUIPOS,
    TIPO_BIEN_INVENTARIO,
    #TIPO_BIEN_GASTO, QUITADO TEMPORALMENTE
    TIPO_BIEN_CUENTAS_POR_COBRAR # Incluir si se implementa en MVP
]

#EN ESTE ARCHIVO ESTARÁ LA LÓGICA DE NEGOCIO COMO FUNCIONES, LAS FUNCIONES CORE ES RECIBIR UNA NUEVA ADQUISICION Y EL CALCULO DEL BALANCE,
#EL CALCULO DEL BALANCE DEBE EJECUTARSE SIEMPRE QUE SE PIDE O SE PIDE GENERAR UN REPORTE

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
            dueno=dueño_empresa,
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
            fecha_creacion_obj = datetime.strptime(fecha_creacion_str, '%Y-%m-%d').date()
            capital_asignado_decimal = Decimal(capital_inicial_asignado_str)
        except ValueError:
            return {"error": "Formato de fecha_creacion incorrecto. Usar YYYY-MM-DD."}, 400

        try:
            capital_asignado = Decimal(capital_inicial_asignado_str)
        except:
            return {"error": "Capital inicial asignado debe ser un número."}, 400
        
        proyecto_existente = proyecto.query.filter_by(
            empresa_id=empresa_id_param, 
            nombre=nombre_proyecto
        ).first()
        if proyecto_existente:
            return {"error": f"Ya existe un proyecto con el nombre '{nombre_proyecto}' en esta empresa."}, 409 
        
        #SE DEBE ANALIZAR QUE ONDA CON LAS DOS PK POR PROYECTO, SE GENERA UNA COMPUESTA O CADA PROYECTO TIENE SU NUMERACIÓN PERO PUEDEN REPETIRSE EN LAS GLOBALES???
        nuevo_proy = proyecto(
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
        return {"error": f"Error interno al crear el proyecto: {str(e)}"}, 500

def registrar_o_actualizar_tesoreria(
    proyecto_id_param,
    empresa_id_param,
    fecha_movimiento, # objeto date
    monto_entrada_mov, # Decimal
    monto_salida_mov,  # Decimal
    descripcion_mov, # Descripción del movimiento actual
):
    """
    Actualiza el snapshot de tesorería del día 'fecha_movimiento' si existe,
    o crea uno nuevo para ese día.
    Los montos de entrada/salida del snapshot son los ACUMULADOS hasta ese día.
    El monto_disponible es el saldo al final de ese día.
    """
    try:
        proyecto_obj = proyecto.query.filter_by(
            proyecto_id=proyecto_id_param,
            empresa_id=empresa_id_param
        ).first()
        if not proyecto_obj:
            raise ValueError(f"Proyecto con id {proyecto_id_param} para empresa {empresa_id_param} no encontrado.")

        monto_entrada_mov_actual = Decimal(monto_entrada_mov) # Movimiento de esta transacción
        monto_salida_mov_actual = Decimal(monto_salida_mov)   # Movimiento de esta transacción

        if monto_entrada_mov_actual < 0 or monto_salida_mov_actual < 0:
            raise ValueError("Los montos de entrada y salida del movimiento no pueden ser negativos.")

        # Buscar el snapshot de tesorería más reciente estrictamente ANTERIOR a fecha_movimiento
        # para obtener los saldos acumulados y disponible al inicio del día del movimiento.
        ultimo_snapshot_dia_anterior = tesoreria.query.filter(
            tesoreria.proyecto_id == proyecto_obj.proyecto_id,
            tesoreria.fecha_registro < fecha_movimiento
        ).order_by(tesoreria.fecha_registro.desc(), tesoreria.tesoreria_id.desc()).first()

        monto_disponible_al_inicio_dia = Decimal('0.00')
        monto_entradas_acum_inicio_dia = Decimal('0.00')
        monto_salidas_acum_inicio_dia = Decimal('0.00')

        if ultimo_snapshot_dia_anterior:
            monto_disponible_al_inicio_dia = Decimal(ultimo_snapshot_dia_anterior.monto_disponible)
            monto_entradas_acum_inicio_dia = Decimal(ultimo_snapshot_dia_anterior.monto_entradas if ultimo_snapshot_dia_anterior.monto_entradas is not None else '0.00')
            monto_salidas_acum_inicio_dia = Decimal(ultimo_snapshot_dia_anterior.monto_salidas if ultimo_snapshot_dia_anterior.monto_salidas is not None else '0.00')
        
        # Buscar si ya existe un snapshot PARA LA MISMA fecha_movimiento
        snapshot_del_dia_existente = tesoreria.query.filter(
            tesoreria.proyecto_id == proyecto_obj.proyecto_id,
            tesoreria.fecha_registro == fecha_movimiento
        ).order_by(tesoreria.tesoreria_id.desc()).first() # En caso de que hubiera más de uno por error, tomar el último.

        if snapshot_del_dia_existente:
            # Actualizar el snapshot existente del día
            # Los montos acumulados en el snapshot se incrementan con este movimiento
            snapshot_del_dia_existente.monto_entradas = (Decimal(snapshot_del_dia_existente.monto_entradas if snapshot_del_dia_existente.monto_entradas is not None else '0.00') + 
                                                         monto_entrada_mov_actual)
            snapshot_del_dia_existente.monto_salidas = (Decimal(snapshot_del_dia_existente.monto_salidas if snapshot_del_dia_existente.monto_salidas is not None else '0.00') +
                                                        monto_salida_mov_actual)
            # El disponible se ajusta con el movimiento actual sobre el disponible que YA TENÍA ese snapshot.
            snapshot_del_dia_existente.monto_disponible = (Decimal(snapshot_del_dia_existente.monto_disponible) + 
                                                           monto_entrada_mov_actual - monto_salida_mov_actual)
            
            # Actualizar descripción y observaciones puede ser opcional o concatenar.
            # Por ahora, podemos sobreescribir con la del último movimiento o la más genérica del día.
            snapshot_del_dia_existente.descripcion = f"Movimientos consolidados al {fecha_movimiento.isoformat()}. Último: {descripcion_mov}"
            
            print(f"Actualizando tesorería para P:{proyecto_obj.proyecto_id}, F:{fecha_movimiento}")
        else:
            # Crear un nuevo snapshot de tesorería para esta fecha_movimiento
            # Los acumulados del NUEVO snapshot parten de los acumulados al INICIO DEL DÍA + este movimiento.
            nuevo_monto_entradas_acum_dia = monto_entradas_acum_inicio_dia + monto_entrada_mov_actual
            nuevo_monto_salidas_acum_dia = monto_salidas_acum_inicio_dia + monto_salida_mov_actual
            nuevo_monto_disponible_dia = monto_disponible_al_inicio_dia + monto_entrada_mov_actual - monto_salida_mov_actual

            nuevo_snapshot = tesoreria(
                descripcion=descripcion_mov, # La descripción del primer movimiento que crea el snapshot del día
                monto_disponible=nuevo_monto_disponible_dia,
                monto_entradas=nuevo_monto_entradas_acum_dia, # Acumulado total hasta este día
                monto_salidas=nuevo_monto_salidas_acum_dia,   # Acumulado total hasta este día
                fecha_registro=fecha_movimiento,
                proyecto_id=proyecto_obj.proyecto_id,
                empresa_id=proyecto_obj.empresa_id 
            )
            db.session.add(nuevo_snapshot)
            print(f"Creando nuevo snapshot de tesorería para P:{proyecto_obj.proyecto_id}, F:{fecha_movimiento}")
        
        # El commit se hará en la función que llama a esta
        return True 

    except ValueError as ve:
        print(f"Error de validación en tesorería: {str(ve)}")
        raise ve # Relanzar para que la función que llama maneje el rollback y la respuesta
    except Exception as e:
        print(f"Error en registrar_o_actualizar_tesoreria: {str(e)}")
        # import traceback # Descomentar para depuración más profunda
        # traceback.print_exc()
        raise e

def get_or_create_bien(nombre_bien, tipo_bien_param, desc_tipo):
    """Busca un bien por nombre y tipo, si no existe, lo crea."""
    # Validar que tipo_bien_param sea uno de los esperados (según tus constantes)
    if (not tipo_bien_param ): #comprueba si no esta en las constantes, pero debo analizar cuales usar
         # Podrías añadir más tipos válidos si es necesario
        raise ValueError(f"Tipo de bien '{tipo_bien_param}' esta vacío.")
    
    if(tipo_bien_param not in TIPOS_BIEN_ACTIVOS and tipo_bien_param != TIPO_BIEN_GASTO):
        raise ValueError(f"Tipo de bien '{tipo_bien_param}' no reconocido o no válido.")

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
# backend/services.py

def agregar_adquisicion(
    empresa_id_param, proyecto_id_param,
    nombre_bien_param, tipo_bien_param, desc_tipo_bien_param,
    monto_total_str, monto_inicial_str, fecha_adquisicion_str,
    forma_pago_char_param,
    meses_pago_param, numero_pagos_param,
    tiene_financiamiento=False,
    fuente_financiamiento_param=None,
    porcentaje_financiamiento_str=None,
    monto_financiado_str=None
):
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
            monto_inicial = Decimal(monto_inicial_str) if monto_inicial_str is not None else Decimal('0.00')
            fecha_adquisicion = datetime.strptime(fecha_adquisicion_str, '%Y-%m-%d').date()
            num_pagos_int = int(numero_pagos_param) if numero_pagos_param is not None else None
            meses_pago_int = int(meses_pago_param) if meses_pago_param is not None else None
        except (ValueError, TypeError) as e:
            return {"error": f"Error en formato de monto, fecha o pagos: {e}"}, 400
        
        if monto_inicial > monto_total:
            raise ValueError("El monto inicial no puede ser mayor al monto total.")
        
        bien_obj = get_or_create_bien(nombre_bien_param, tipo_bien_param, desc_tipo_bien_param)
        forma_pago_obj = get_or_create_forma_pago(forma_pago_char_param)

        # --- LÓGICA CORREGIDA PARA CALCULAR 'periodicidad' ---
        periodicidad_calculada = None
        # Solo se intenta la división si ambos valores son números y el divisor no es cero.
        if meses_pago_int is not None and num_pagos_int is not None and num_pagos_int > 0:
            periodicidad_calculada = Decimal(meses_pago_int) / Decimal(num_pagos_int)
        # --------------------------------------------------------

        nueva_adq = adquisicion(
            monto_total=monto_total,
            enganche=monto_inicial,
            fecha_adquisicion=fecha_adquisicion,
            numero_pagos=num_pagos_int,
            meses_pagos=meses_pago_int,
            periodicidad=periodicidad_calculada, # Se usa el valor calculado de forma segura
            proyecto_id=proyecto_obj.proyecto_id,
            empresa_id=proyecto_obj.empresa_id,
            bien_id=bien_obj.bien_id,
            forma_pago_id=forma_pago_obj.forma_pago_id,
        )
        db.session.add(nueva_adq)
        db.session.flush() 

        # ... (el resto de la lógica de financiamiento y tesorería no cambia) ...

        financiamiento_creado = None
        if tiene_financiamiento and monto_financiado_str and fuente_financiamiento_param:
            try:
                monto_financiado = Decimal(monto_financiado_str)
                porcentaje_fin = Decimal(porcentaje_financiamiento_str) if porcentaje_financiamiento_str else None
            except (ValueError, TypeError):
                 db.session.rollback()
                 return {"error": "Monto de financiamiento debe ser un número o el porcentaje es incorrecto."}, 400

            if not (monto_total == monto_inicial + monto_financiado):
                db.session.rollback()
                return {"error": "El monto total no coincide con la suma del enganche y el monto financiado."}, 400
            
            nuevo_fin = financiamiento(
                fuente=fuente_financiamiento_param,
                porcentaje=porcentaje_fin,
                monto_financiado=monto_financiado,
                adquisicion_id=nueva_adq.adquisicion_id
            )
            db.session.add(nuevo_fin)
            financiamiento_creado = nuevo_fin

        if forma_pago_obj.tipo == 'E' and monto_inicial > Decimal('0.00'):
            registrar_o_actualizar_tesoreria(
                proyecto_id_param=nueva_adq.proyecto_id,
                empresa_id_param=nueva_adq.empresa_id,
                fecha_movimiento=fecha_adquisicion,
                monto_entrada_mov=Decimal('0.00'),
                monto_salida_mov=monto_inicial,
                descripcion_mov=f"Pago inicial adquisición: {bien_obj.nombre}"
            )

        db.session.commit()

        # ... (la lógica para construir la respuesta no cambia) ...
        adq_data = {
            "adquisicion_id": float(nueva_adq.adquisicion_id),
            "monto_total": str(nueva_adq.monto_total),
            "bien_nombre": bien_obj.nombre,
            "proyecto_id": float(nueva_adq.proyecto_id)
        }
        if financiamiento_creado:
            adq_data["financiamiento_id"] = float(financiamiento_creado.financiamiento_id)
            adq_data["monto_financiado"] = str(financiamiento_creado.monto_financiado)

        return {"mensaje": "Adquisición agregada exitosamente.", "adquisicion": adq_data}, 201

    except ValueError as ve: 
        db.session.rollback()
        return {"error": str(ve)}, 400
    except Exception as e:
        db.session.rollback()
        print(f"Error en agregar_adquisicion: {str(e)}")
        return {"error": f"Error interno al agregar la adquisición: {str(e)}"}, 500

def calcular_balance_general(empresa_id, proyecto_id, fecha_str):

    try: #Se hace todo dentro de un try-catch a reserva de los posibles errores que se pueden generar con la base de datos
        #validación para ver si la empresa y el proyecto existen
        emp_id = Decimal(empresa_id)
        proy_id =  Decimal(proyecto_id)
        proyecto_val_query = db.select(proyecto).where(proyecto.empresa_id == emp_id).where(proyecto.proyecto_id == proy_id) #Crea la consulta SQL
        proyecto_existente = db.session.execute(proyecto_val_query).scalar_one_or_none() #Ejecuta la consulta SQL en la sesi´on que abrí y trae un registro

        if not proyecto_existente:
            return {"error": f"No existe el proyecto {proyecto_id}"}, 404
        
        #Variables que se usarán parra el cálculo del balance
        activos_desglosados = {}
        pasivos_desglosados = {}
        total_activos_calculado = Decimal('0.00')
        total_pasivos_calculado = Decimal('0.00')
        fecha_balance = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        snapshot_tesoreria = tesoreria.query.filter(
            tesoreria.empresa_id == empresa_id,
            tesoreria.proyecto_id == proyecto_id,
            tesoreria.fecha_registro <= fecha_balance
        ).order_by(
            tesoreria.fecha_registro.desc(),
            tesoreria.tesoreria_id.desc()
        ).first()
        
        # --- VERSIÓN CORREGIDA ---
        # En lugar de devolver un error, asumimos que el efectivo es 0 si no hay registro.
        efectivo = Decimal('0.00')
        if snapshot_tesoreria:
            efectivo = Decimal(snapshot_tesoreria.monto_disponible)
        
        # El resto de la lógica para sumar activos continúa desde aquí...
        total_activos_calculado += efectivo
        activos_desglosados[TIPO_BIEN_EFECTIVO_EQUIVALENTES] = efectivo


        #Aquí se harán consultas por tipo de bien para poder tener el desglose en el diccionario y PDF
        #Es una consulta compleja
        #********************REVISAR SI USARR MONTO TOTAL O QUE NO ESTOY SEGURO AL CONTAR EL EFECTIVO DE TESORERIA ****************
        activosDB = db.session.query(bien.tipo_bien, func.sum(adquisicion.monto_total).label('total_por_tipo') #SELECT Y SUMA DE SQL CUANDO SE AGRUPE
                                      ).join( #JOIN DE ADQUISICION Y BIENES
                                          bien, adquisicion.bien_id == bien.bien_id
                                      ).filter( #TRAE SOLO LOS RREGISTROS DEL PROYYECTO, EMPRRESA ANTES DE LA FECHA DEL BALANCE
                                          adquisicion.empresa_id == emp_id,
                                          adquisicion.proyecto_id == proyecto_id,
                                          adquisicion.fecha_adquisicion <= fecha_balance,
                                          bien.tipo_bien.in_(TIPOS_BIEN_ACTIVOS) #VER SI ESTA LINEA ESTA CORRECTA, QUITARRE GASTOS DE LA ESTRUCTURA, DEPENDE COMO SALGA EL BALANCE
                                      ).group_by( #AGRUPA Y EJECUTA LA SUMA POR TIPO DE BIEN
                                          bien.tipo_bien
                                      ).all() #EJECUTA LA CONSULTA
        
        for tipo, total in activosDB:
            monto_total_tipo = Decimal(total) if total is not None else Decimal('0.00') #Se valida que el total no sea , si lo es aún así lo formatea para cuadrar la suma
            activos_desglosados[tipo] = activos_desglosados.get(tipo, Decimal('0.00')) + monto_total_tipo #asignación robusta, por si hubiera algún errro con group byy en la consulta y repitierra tipo
            total_activos_calculado += monto_total_tipo

        #Consulta compleja y desglose para los pasivos
        pasivosDB = db.session.query(financiamiento.fuente, func.sum(financiamiento.monto_financiado).label('total por tipo')#SIMILAR A ACTIVOS, TRAIGO LA FUENTE COMO TIPO PARA EL DESGLOSE Y SUMMARE AL AGRUPAR
                                     ).join(#JOIN DE ADQUISICIÓN Y FINANCIAMMIENTO
                                        adquisicion, financiamiento.adquisicion_id == adquisicion.adquisicion_id #INNER JOIN
                                     ).filter( #TRAE SOLO LOS RREGISTROS DEL PROYYECTO, EMPRRESA ANTES DE LA FECHA DEL BALANCE
                                        adquisicion.empresa_id == emp_id,
                                        adquisicion.proyecto_id == proyecto_id,
                                        adquisicion.fecha_adquisicion <= fecha_balance
                                     ).group_by( #AGRUPA Y EJECUTA SEGÚN LA FUENTE DE FINANCIAMIENTO
                                        financiamiento.fuente
                                     ).all()#EJECUTA LA CONSULTA
        
        for tipo, total in pasivosDB:
            monto_total_tipo = Decimal(total) if total is not None else Decimal('0.00') #Se valida que el total no sea , si lo es aún así lo formatea para cuadrar la suma
            pasivos_desglosados[tipo] = pasivos_desglosados.get(tipo, Decimal('0.00')) + monto_total_tipo #asignación robusta, por si hubiera algún errro con group byy en la consulta y repitierra tipo
            total_pasivos_calculado += monto_total_tipo

        capital_contable_calculado = total_activos_calculado - total_pasivos_calculado

        balance = balanceFinanciero.query.filter(balanceFinanciero.empresa_id == emp_id,
                                                    balanceFinanciero.proyecto_id == proy_id,
                                                    balanceFinanciero.fecha_generado == fecha_balance
                                                    ).first() #CONSULTA PARA VER SI EL BALANCE YA SE CALCULO
        
        nombre_balance = f"Balance General al {fecha_balance.isoformat()}"
        
        if balance:
            balance.nombre = nombre_balance
            balance.total_activos = total_activos_calculado
            balance.total_pasivos = total_pasivos_calculado
            balance.capital_contable = capital_contable_calculado
            balance.observaciones = "El balance fue actualizao"
        else:
            nuevo_balance = balanceFinanciero(
                nombre = nombre_balance,
                fecha_generado = fecha_balance,
                total_activos = total_activos_calculado,
                total_pasivos = total_pasivos_calculado,
                capital_contable = capital_contable_calculado,
                proyecto_id = proy_id,
                empresa_id = emp_id
            )
            db.session.add(nuevo_balance)
        
        db.session.commit()

        # Convertir los diccionarios de desglose a una lista de objetos, que es más fácil de usar en el frontend
        activos_lista_para_json = [{"categoria": key, "monto": str(value)} for key, value in activos_desglosados.items()]
        pasivos_lista_para_json = [{"categoria": key, "monto": str(value)} for key, value in pasivos_desglosados.items()]

        # Diccionario final de respuesta
        respuesta_balance = {
            "mensaje": "Balance General calculado exitosamente.",
            "empresa_id": str(empresa_id),
            "proyecto_id": str(proyecto_id),
            "fecha_balance": fecha_balance.isoformat(),
            "totales": {
                "total_activos": str(total_activos_calculado),
                "total_pasivos": str(total_pasivos_calculado),
                "capital_contable": str(capital_contable_calculado)
            },
            "desglose": {
                "activos": activos_lista_para_json,
                "pasivos": pasivos_lista_para_json
            }
        }

        return respuesta_balance, 200
    except ValueError as ve: #errores de validación en los datos del JSON
        db.session.rollback()
        return {"error": str(ve)}, 400
    except Exception as e: #error en la base de datos u otros
        db.session.rollback()
        return {"error": f"Error inesperado durante el cálculo del balance {str(e)}"}, 500

def send_tesoreria_fechas(empresa_id, proyecto_id):
    try:
        fechas_registros = tesoreria.query.filter(
            tesoreria.empresa_id == empresa_id,
            tesoreria.proyecto_id == proyecto_id
        ).with_entities(tesoreria.fecha_registro).all()

        fechas_formateadas = [fecha.fecha_registro.strftime('%Y-%m-%d') for fecha in fechas_registros] #Se debe procesar para poder meterse en el JSON

        return jsonify({"success": True, "fechas": fechas_formateadas}), 200

    except Exception as e:
        # En caso de cualquier error (ej. problema de base de datos, tipos de datos incorrectos)
        return jsonify({"success": False, "message": f"Error al obtener fechas de tesorería: {str(e)}"}), 500

# En tu archivo de servicios (ej. services.py)
from .models import empresa
from flask import jsonify
from decimal import Decimal

def send_empresas():
    try:
        todas_las_empresas = empresa.query.order_by(empresa.nombre).all() #TRAE TODAS LAS EMPRESAS DE LA TABLA

        empresas_lista = []

        for emp in todas_las_empresas:
            empresa_data = {
                "empresa_id": float(emp.empresa_id),
                "nombre": emp.nombre
            }
            empresas_lista.append(empresa_data)

        return {
            "mensaje": "Empresas obtenidas exitosamente",
            "empresas": empresas_lista
        }, 200

    except Exception as e:
        print(f"Error en send_empresas: {str(e)}")
        return {"error": f"Error interno al obtener las empresas: {str(e)}"}, 500

def obtener_proyectos_por_empresa(empresa_id_param):
    try:
        empresa_id = Decimal(empresa_id_param)
        
        empresa_obj = empresa.query.get(empresa_id)
        if not empresa_obj:
            return {"error": f"La empresa con id {empresa_id} no fue encontrada."}, 404

        proyectos_de_la_empresa = proyecto.query.filter_by(empresa_id=empresa_id).order_by(proyecto.nombre).all() #TRAE TODOS LOS PROYECTOS DE UNA EMPRESA

        #Preparar la lista de resultados para la respuesta JSON.
        proyectos_lista = []
        for proy in proyectos_de_la_empresa:
            proyecto_data = {
                "proyecto_id": float(proy.proyecto_id),
                "nombre": proy.nombre,
            }
            proyectos_lista.append(proyecto_data)
        
        return {
            "mensaje": f"Proyectos de la empresa '{empresa_obj.nombre}' obtenidos exitosamente.",
            "proyectos": proyectos_lista
        }, 200

    except ValueError:
        return {"error": "El ID de la empresa debe ser un número válido."}, 400
    except Exception as e:
        print(f"Error en obtener_proyectos_por_empresa: {str(e)}")
        return {"error": f"Error interno al obtener los proyectos: {str(e)}"}, 500

def generar_balance_pdf(empresa_id_param, proyecto_id_param, fecha_hasta_str):
    """
    Orquesta la creación de un reporte de Balance General en formato PDF,
    con soporte para caracteres Unicode (UTF-8) y pasos de depuración.
    """
    # 1. Obtener los datos del balance
    datos_balance, status_code = calcular_balance_general(
        empresa_id_param, proyecto_id_param, fecha_hasta_str
    )

    if status_code != 200:
        return datos_balance, status_code

    # --- PASO DE DEPURACIÓN 1: Imprimir los datos recibidos ---
    print("--- Datos recibidos para generar PDF ---")
    print(datos_balance)
    print("--------------------------------------")

    try:
        # 2. Construir el PDF
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()

        # Añadir y establecer la fuente Unicode
        try:
            pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
            pdf.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', uni=True)
            pdf.set_font('DejaVu', '', 12)
        except RuntimeError as e:
            print(f"ADVERTENCIA: No se encontró la fuente DejaVu. Error: {e}")
            pdf.set_font('Arial', '', 12)

        # --- PASO DE DEPURACIÓN 2: Establecer color de texto explícitamente ---
        pdf.set_text_color(0, 0, 0) # Establecer texto a color negro (RGB)

        # --- CABECERA DEL DOCUMENTO ---
        pdf.set_font('DejaVu', 'B', 16)
        pdf.cell(0, 10, 'Balance General', ln=True, align='C')
        
        proyecto_obj = proyecto.query.get(proyecto_id_param)
        empresa_obj = empresa.query.get(empresa_id_param)
        
        pdf.set_font('DejaVu', '', 12)
        pdf.cell(0, 8, f"Empresa: {empresa_obj.nombre if empresa_obj else 'N/A'}", ln=True, align='C')
        pdf.cell(0, 8, f"Proyecto: {proyecto_obj.nombre if proyecto_obj else 'N/A'}", ln=True, align='C')
        pdf.cell(0, 8, f"Al {datos_balance.get('fecha_balance', 'N/A')}", ln=True, align='C')
        pdf.ln(10)

        # --- SECCIONES DEL PDF ---
        # Asegúrate de que las claves 'desglose', 'activos', 'totales', etc., existan en 'datos_balance'
        desglose_data = datos_balance.get('desglose', {})
        totales_data = datos_balance.get('totales', {})

        # Sección de Activos
        pdf.set_font('DejaVu', 'B', 14)
        pdf.cell(0, 10, 'Activos', ln=True)
        pdf.set_font('DejaVu', '', 11)
        # Usamos .get() con una lista vacía como default para evitar errores si la clave no existe
        for item in desglose_data.get('activos', []):
            pdf.cell(130, 7, f"  {item.get('categoria', 'N/A')}")
            pdf.cell(50, 7, f"$ {item.get('monto', '0.00')}", ln=True, align='R')
        pdf.set_font('DejaVu', 'B', 12)
        pdf.cell(130, 8, 'Total Activos', border='T')
        pdf.cell(50, 8, f"$ {totales_data.get('total_activos', '0.00')}", border='T', ln=True, align='R')
        pdf.ln(8)
        
        # Sección de Pasivos
        pdf.set_font('DejaVu', 'B', 14)
        pdf.cell(0, 10, 'Pasivos', ln=True)
        pdf.set_font('DejaVu', '', 11)
        for item in desglose_data.get('pasivos', []):
            pdf.cell(130, 7, f"  {item.get('categoria', 'N/A')}")
            pdf.cell(50, 7, f"$ {item.get('monto', '0.00')}", ln=True, align='R')
        pdf.set_font('DejaVu', 'B', 12)
        pdf.cell(130, 8, 'Total Pasivos', border='T')
        pdf.cell(50, 8, f"$ {totales_data.get('total_pasivos', '0.00')}", border='T', ln=True, align='R')
        pdf.ln(8)
        
        # Sección de Patrimonio
        pdf.set_font('DejaVu', 'B', 14)
        pdf.cell(0, 10, 'Patrimonio', ln=True)
        pdf.set_font('DejaVu', 'B', 12)
        pdf.cell(130, 8, 'Capital Contable', border='T')
        pdf.cell(50, 8, f"$ {totales_data.get('capital_contable', '0.00')}", border='T', ln=True, align='R')

        # Generar los bytes del PDF
        output_bytearray = pdf.output(dest='S')
        pdf_bytes = bytes(output_bytearray)
        
        # --- PASO DE DEPURACIÓN 3: Verificar el tamaño del PDF generado ---
        print(f"--- PDF generado, tamaño en bytes: {len(pdf_bytes)} ---")
        if len(pdf_bytes) < 400: # Un PDF real, incluso simple, suele ser más grande
            print("ADVERTENCIA: El tamaño del PDF generado es muy pequeño, podría estar vacío.")

        nombre_archivo = f"Balance_General_{empresa_obj.nombre.replace(' ', '') if empresa_obj else 'Reporte'}{fecha_hasta_str}.pdf"

        return {"pdf_bytes": pdf_bytes, "nombre_archivo": nombre_archivo}, 200

    except Exception as e:
        print(f"ERROR al generar PDF en 'generar_balance_pdf': {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": "Error interno al generar el archivo PDF."}, 500

