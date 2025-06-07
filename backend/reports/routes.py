# backend/reports/routes.py
from flask import Blueprint, request, jsonify, Response
from ..services import nueva_empresa, nuevo_proyecto, agregar_adquisicion, send_tesoreria_fechas, calcular_balance_general, send_empresas, obtener_proyectos_por_empresa, generar_balance_pdf
from flask import Response

reportes_bp = Blueprint('reportes_bp', __name__, url_prefix='/api/reportes') 

@reportes_bp.route('/crear/empresa', methods=['POST'])
def crear_nueva_empresa_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos JSON."}), 400

    nombre = data.get('nombre')
    dueno = data.get('dueno') 
    correo = data.get('correo')
    telefono_str = data.get('telefono')
    direccion = data.get('direccion')
    rfc = data.get('rfc')

    if not all([nombre, dueno, correo, telefono_str, direccion, rfc]):
        return jsonify({"error": "Faltan campos requeridos para crear la empresa."}), 400
    
    resultado, status_code = nueva_empresa(
        nombre_empresa=nombre,
        dueño_empresa=dueno, 
        correo_empresa=correo,
        telefono_empresa=telefono_str,
        direccion_empresa=direccion,
        rfc_empresa=rfc
    )
    return jsonify(resultado), status_code

@reportes_bp.route('/crear/proyecto', methods=['POST'])
def crear_nuevo_proyecto_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos JSON."}), 400

    empresa_id = data.get('empresa_id')
    nombre = data.get('nombre')
    fecha_creacion = data.get('fecha_creacion') # Esperar formato YYYY-MM-DD
    capital_inicial = data.get('capital_inicial')

    if not all([empresa_id, nombre, fecha_creacion, capital_inicial]):
        return jsonify({"error": "Faltan campos requeridos para crear el proyecto."}), 400
    
    try:
        empresa_id_int = int(empresa_id)
    except ValueError:
        return jsonify({"error": "empresa_id debe ser un número."}), 400
        
    resultado, status_code = nuevo_proyecto(
        empresa_id_param=empresa_id_int,
        nombre_proyecto=nombre,
        fecha_creacion_str=fecha_creacion,
        capital_inicial_asignado_str=str(capital_inicial)
    )
    return jsonify(resultado), status_code

@reportes_bp.route('/nueva/adquisicion', methods=['POST'])
def agregar_nueva_adquisicion_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos JSON."}), 400

    # Extraer todos los parámetros necesarios de 'data'
    # Coincidir con los parámetros de tu función agregar_adquisicion en services.py
    empresa_id = data.get('empresa_id')
    proyecto_id = data.get('proyecto_id') # El ID local del proyecto
    nombre_bien = data.get('nombre_bien')
    tipo_bien = data.get('tipo_bien')
    desc_tipo_bien = data.get('desc_tipo_bien')
    monto_total = data.get('monto_total')
    monto_inicial = data.get('monto_inicial')
    fecha_adquisicion = data.get('fecha_adquisicion')
    forma_pago_char = data.get('forma_pago_char')
    meses_pago = data.get('meses_pago')
    numero_pagos = data.get('numero_pagos')
    
    tiene_financiamiento = data.get('tiene_financiamiento', False)
    fuente_financiamiento = data.get('fuente_financiamiento')
    porcentaje_financiamiento = data.get('porcentaje_financiamiento')
    monto_financiado = data.get('monto_financiado')

    # Validaciones básicas
    required_fields_adq = [
        empresa_id, proyecto_id, nombre_bien, tipo_bien, desc_tipo_bien,
        monto_total, monto_inicial, fecha_adquisicion, forma_pago_char
    ]
    if not all(required_fields_adq): # numero_pagos y meses_pago pueden ser 0 o None
        return jsonify({"error": "Faltan campos requeridos para agregar la adquisición."}), 400
    
    if tiene_financiamiento and not all([fuente_financiamiento, monto_financiado]): # porcentaje es opcional
        return jsonify({"error": "Si tiene financiamiento, la fuente y el monto financiado son requeridos."}), 400

    try:
        empresa_id_int = int(empresa_id)
        proyecto_id_int = int(proyecto_id) # El ID local
    except ValueError:
        return jsonify({"error": "empresa_id y proyecto_id deben ser números."}), 400

    resultado, status_code = agregar_adquisicion(
        empresa_id_param=empresa_id_int,
        proyecto_id_param=proyecto_id_int, # Pasar el ID local del proyecto
        nombre_bien_param=nombre_bien,
        tipo_bien_param=tipo_bien,
        desc_tipo_bien_param=desc_tipo_bien,
        monto_total_str=str(monto_total),
        monto_inicial_str=str(monto_inicial),
        fecha_adquisicion_str=fecha_adquisicion,
        forma_pago_char_param=forma_pago_char,
        meses_pago_param=int(meses_pago) if meses_pago is not None else None,
        numero_pagos_param=int(numero_pagos) if numero_pagos is not None else None,
        tiene_financiamiento=tiene_financiamiento,
        fuente_financiamiento_param=fuente_financiamiento,
        porcentaje_financiamiento_str=str(porcentaje_financiamiento) if porcentaje_financiamiento is not None else None,
        monto_financiado_str=str(monto_financiado) if monto_financiado is not None else None
    )
    return jsonify(resultado), status_code

@reportes_bp.route('/tesoreria/fechas/<int:empresa_id>/<int:proyecto_id>', methods=['GET'])
def get_tesoreria_fechas_route(empresa_id, proyecto_id):
    return send_tesoreria_fechas(empresa_id, proyecto_id)

@reportes_bp.route('/balance_general', methods=['GET'])
def get_balance_general_endpoint():
    """
    Endpoint para solicitar el cálculo de un Balance General.
    Recibe los parámetros a través de la URL (query string).
    """

    #Ejemplo de URL: /reports/balance_general?empresa_id=1&proyecto_id=101&fecha_hasta=2025-12-31
    empresa_id_str = request.args.get('empresa_id')
    proyecto_id_str = request.args.get('proyecto_id')
    fecha_hasta_str = request.args.get('fecha_hasta')

    try:
        empresa_id = int(empresa_id_str)
        proyecto_id = int(proyecto_id_str)
    except ValueError:
        return jsonify({"error": "Los parámetros 'empresa_id' y 'proyecto_id' deben ser números enteros."}), 400

    # Validar que todos los parámetros necesarios fueron enviados.
    if not all([empresa_id_str, proyecto_id_str, fecha_hasta_str]):
        return jsonify({
            "error": "Parámetros insuficientes. Se requieren 'empresa_id', 'proyecto_id' y 'fecha_hasta'."
        }), 400
    
    resultado, status_code = calcular_balance_general(
        empresa_id=empresa_id,
        proyecto_id=proyecto_id,
        fecha_str=fecha_hasta_str
    )

    #El resultado ya es un diccionario listo, y el status_code
    return jsonify(resultado), status_code

@reportes_bp.route('/empresas', methods=['GET'])
def get_todas_las_empresas_endpoint():
    resultado, status_code = send_empresas()
    
    return jsonify(resultado), status_code

@reportes_bp.route('/empresas/<int:empresa_id>/proyectos', methods=['GET'])
def get_proyectos_de_empresa_endpoint(empresa_id):
    resultado, status_code = obtener_proyectos_por_empresa(empresa_id)
    
    return jsonify(resultado), status_code

@reportes_bp.route('/balance-general/pdf', methods=['GET'])
def descargar_balance_pdf_endpoint():
    # ... (código de obtención y validación de parámetros como lo tienes) ...
    empresa_id_str = request.args.get('empresa_id')
    proyecto_id_str = request.args.get('proyecto_id')
    fecha_hasta_str = request.args.get('fecha_hasta')

    # Validación básica (puedes hacerla más robusta)
    if not all([empresa_id_str, proyecto_id_str, fecha_hasta_str]):
        return jsonify({"error": "Parámetros insuficientes."}), 400

    resultado, status_code = generar_balance_pdf(
        empresa_id_param=empresa_id_str,
        proyecto_id_param=proyecto_id_str,
        fecha_hasta_str=fecha_hasta_str
    )

    if status_code != 200:
        return jsonify(resultado), status_code

    pdf_bytes = resultado.get("pdf_bytes")
    nombre_archivo = resultado.get("nombre_archivo")

    # El resto de tu código para crear la respuesta es perfecto.
    # Flask Response puede manejar el objeto bytearray directamente.
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment;filename=\"{nombre_archivo}\""}
    )