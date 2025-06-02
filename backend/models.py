# backend/models.py
from .app import db # Se importa la instancia abierta de la 'db' de app.py para crear las clases usando el modelo de la DB

#SE DEBEN PONER LOS MISMOS NOMBRES QUE EN LOS CAMPOS DE DB, VERIFICAR SI ES SENSIBLE A MAYUSCULAS O MINUSCULAS  LA DB
class empresa(db.Model):
    __tablename__ = 'EMPRESA' 

    #Atributos de la tabla
    empresa_id = db.Column(db.Numeric(10, 0), primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    dueño = db.Column(db.String(40), nullable=False) 
    correo = db.Column(db.String(40), nullable=False)
    telefono = db.Column(db.Numeric(10, 0), nullable=False)
    direccion = db.Column(db.String(140), nullable=False)
    rfc = db.Column(db.String(12), nullable=False)

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<empresa id={self.empresa_id}: nombre="{self.nombre}">'

class usuario(db.Model):
    __tablename__ = 'USUARIO'

    #Atributos de la tabla
    usuario_id = db.Column(db.Numeric(10, 0), primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    correo = db.Column(db.String(80), nullable=False, unique=True)
    rfc = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False) # Aumentado para almacenar hashes de contraseñas

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<usuario id={self.usuario_id}: nombre="{self.nombre}">'

class rolesEmpresa(db.Model):
    __tablename__ = 'ROLES_EMPRESA'

    # Clave primaria compuesta (En este caso son también IDs en otras tablas, por eso FK)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('EMPRESA.empresa_id'), primary_key=True) #SE DEBE USAR LOS NOMBRES DE LA TABLA PARA FK
    usuario_id = db.Column(db.Numeric(10, 0), db.ForeignKey('USUARIO.usuario_id'), primary_key=True)

    # Atributos de la tabla
    rol_capturista = db.Column(db.Boolean, nullable=False, default=False)
    rol_admin = db.Column(db.Boolean, nullable=False, default=False)
    rol_jefe = db.Column(db.Boolean, nullable=False, default=False) 
    rol_financiero = db.Column(db.Boolean, nullable=False, default=False) 

    # Relaciones con otros objetos
    empresa = db.relationship('empresa', backref=db.backref('roles_asignados', lazy='dynamic')) #VERIFICAR SI SE DEBE USAR DYNAMIC
    usuario = db.relationship('usuario', backref=db.backref('roles_en_empresas', lazy='dynamic'))

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<rolesEmpresa usuarioID={self.usuario_id}: empresaID={self.empresa_id}>'

class balanceFinanciero(db.Model):
    __tablename__='BALANCE_FINANCIERO'

    #Clave primaria
    balance_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    nombre = db.Column(db.String(40), nullable=False)
    fecha_generado = db.Column(db.Date, nullable=False)
    total_activos = db.Column(db.Numeric(14, 2), nullable=False)
    total_pasivos = db.Column(db.Numeric(14, 2), nullable=False)
    capital_contable = db.Column(db.Numeric(14, 2), nullable=False)
    observaciones = db.Column(db.Text, nullable = True)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    proyecto_id = db.Column(db.Numeric(10, 0), db.ForeignKey('PROYECTO.proyecto_id'), nullable=False)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('EMPRESA.empresa_id'), nullable=False)

    #Relaciones con otros objetos
    proyecto = db.relationship('proyecto', foreign_keys=[proyecto_id])
    empresa = db.relationship('empresa', foreign_keys=[empresa_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<balanceFinanciero balance_id={self.balance_id}: nombre="{self.nombre}">' #Se añaden comillas a nombre por legibilidad

class proyecto(db.Model):
    __tablename__='PROYECTO'

    #Clave primaria compuesta
    proyecto_id = db.Column(db.Numeric(10, 0), primary_key=True)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('EMPRESA.empresa_id'), primary_key=True)

    #Atributos de la tabla
    nombre = db.Column(db.String(40), nullable=False)
    fecha_creacion = db.Column(db.Date, nullable=False)
    capital_disponible = db.Column(db.Numeric(12,2), nullable=False)

    #Relaciones con otros objetos
    empresa = db.relationship('empresa', backref=db.backref('empresa_proyecto')) #VERIFICAR SI SE DEBE USAR DYNAMIC U OTRO PARAM  EN LAZY

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Proyecto proyectoID={self.proyecto_id}: empresaID={self.empresa_id}: nombre="{self.nombre}">' #Se añaden comillas a nombre por legibilidad
    

class statusAdquisicion(db.Model):
    __tablename__='STATUS_ADQUISICION'

    #Clave primaria
    status_adquisicion_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    clave = db.Column(db.String(40), nullable=False)
    descripcion = db.Column(db.String(80), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=False)

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Status de la adquisicion ID={self.status_adquisicion_id} descripcion="{self.descripcion}">' #Se añaden comillas a nombre por legibilidad

class historicoAdquisicion(db.Model):
    __tablename__='HISTORICO_STATUS_ADQUISICION'

    #Clave primaria
    historico_status_adquisicion_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    fecha_status = db.Column(db.Date, nullable=False)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    adquisicion_id = db.Column(db.Numeric(10, 0), db.ForeignKey('ADQUISICION.adquisicion_id'), nullable=False)
    status_adquisicion_id = db.Column(db.Numeric(10, 0), db.ForeignKey('STATUS_ADQUISICION.status_adquisicion_id'), nullable=False)

    #Relaciones con otros objetos
    adquisicion = db.relationship('adquisicion', foreign_keys=[adquisicion_id])
    status = db.relationship('statusAdquisicion', foreign_keys=[status_adquisicion_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Historico ID={self.historico_status_adquisicion_id}: fecha={self.fecha_status}>'
    
class financiamiento(db.Model):
    __tablename__='FINANCIAMIENTO'

    #Clave primaria
    financiamiento_id = db.Column(db.Numeric(10, 0), primary_key=True   )

    #Atributos de la tabla
    fuente = db.Column(db.String(40), nullable=False)
    porcentaje = db.Column(db.Numeric(5, 2), nullable=False)
    monto_financiado = db.Column(db.Numeric(14, 2), nullable=False)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    adquisicion_id = db.Column(db.Numeric(10, 0), db.ForeignKey('ADQUISICION.adquisicion_id'), nullable=False)

    #Relaciones con otros objetos
    adquisicion = db.relationship('adquisicion', foreign_keys=[adquisicion_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Financiamiento ID={self.financiamiento_id}: adquisicion={self.adquisicion_id}: monto={self.monto_financiado}>'

class formaDePago(db.Model):
    __tablename__='FORMA_PAGO'

    #Clave primaria
    forma_pago_id = db.Column(db.Numeric(10, 0), primary_key= True)

    #Atributos de la tabla
    tipo = db.Column(db.CHAR(1), nullable=False)

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Forma de pago ID={self.forma_pago_id}: tipo={self.tipo}>'

class bien(db.Model):
    __tablename__='BIEN'

    #Clave primaria
    bien_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    nombre = db.Column(db.String(40), nullable=False)
    tipo_bien = db.Column(db.String(40), nullable=False)
    desc_tipo = db.Column(db.String(40), nullable = False)

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Bien nombre="{self.nombre}": tipo={self.tipo_bien}>' #Se añaden comillas a nombre por legibilidad

class estadoDeResultado(db.Model):
    __tablename__='ESTADO_RESULTADO'

    #Clave primaria
    estado_resultado_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    anio = db.Column(db.Numeric(4, 0), nullable=False)
    periodo = db.Column(db.String(40), nullable=False)
    fecha_registro = db.Column(db.Date, nullable=False)
    ingreso_total = db.Column(db.Numeric(14, 2), nullable=False)
    gasto_total = db.Column(db.Numeric(14, 2), nullable=False)
    utilidad_neta = db.Column(db.Numeric(14, 2), nullable=False)
    observaciones = db.Column(db.Text, nullable=False)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    proyecto_id = db.Column(db.Numeric(10, 0), db.ForeignKey('PROYECTO.proyecto_id'), nullable=False)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('EMPRESA.empresa_id'), nullable=False)

    #Relaciones con otros objetos
    proyecto  = db.relationship('proyecto', foreign_keys=[proyecto_id])
    empresa  = db.relationship('empresa', foreign_keys=[empresa_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Resultado  ID={self.estado_resultado_id}: empresa={self.empresa_id}: proyecto={self.proyecto_id}>'

class adquisicion(db.Model):
    __tablename__='ADQUISICION'

    #Clave primaria
    adquisicion_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    monto_total = db.Column(db.Numeric(17, 2), nullable=False)
    monto_inicial = db.Column(db.Numeric(17, 2), nullable=False)
    fecha_adquisicion = db.Column(db.Date, nullable=False)
    numero_pagos = db.Column(db.Numeric(2, 0), nullable=True)
    anios_pagos = db.Column(db.Numeric(2, 0), nullable=True)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    proyecto_id = db.Column(db.Numeric(10, 0), db.ForeignKey('PROYECTO.proyecto_id'), nullable=False)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('EMPRESA.empresa_id'), nullable=False)
    bien_id = db.Column(db.Numeric(10, 0), db.ForeignKey('BIEN.bien_id'), nullable=False)
    forma_pago_id = db.Column(db.Numeric(10, 0), db.ForeignKey('FORMA_PAGO.forma_pago_id'), nullable=False)
    status_adquisicion_id = db.Column(db.Numeric(10, 0), db.ForeignKey('STATUS_ADQUISICION.status_adquisicion_id'), nullable=False)

    #Relaciones con otros objetos
    proyecto  = db.relationship('proyecto', foreign_keys=[proyecto_id])
    empresa  = db.relationship('empresa', foreign_keys=[empresa_id])
    bien = db.relationship('bien', foreign_keys=[bien_id])
    pago = db.relationship('formaDePago', foreign_keys=[forma_pago_id])
    status = db.relationship('statusAdquisicion', foreign_keys=[status_adquisicion_id])


    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Adquisicion ID={self.adquisicion_id}: bien={self.bien_id}: empresa={self.empresa_id}: monto={self.monto_total}>'
    
class reporte(db.Model):
    __tablename__='REPORTE'

    #Clave primaria
    reporte_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    archivo = db.Column(db.LargeBinary, nullable=False) #VERIFICAR QUE HAGAN MATCH LOS TIPOS DE DATOS BACK-BASE Y EL PROPOSITO DE ESTA COLUMNA
    tipo_reporte =  db.Column(db.String(40), nullable=False)
    fecha_subida = db.Column(db.Date, nullable=False)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    proyecto_id = db.Column(db.Numeric(10, 0), db.ForeignKey('PROYECTO.proyecto_id'), nullable=False)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('EMPRESA.empresa_id'), nullable=False)

    #Relaciones con otros objetos
    proyecto  = db.relationship('proyecto', foreign_keys=[proyecto_id])
    empresa  = db.relationship('empresa', foreign_keys=[empresa_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<ReportePDF ID={self.reporte_id}: empresa={self.empresa_id}>'

class tesoreria(db.Model):
    __tablename__='TESORERIA'

    #Clave primaria
    tesoreria_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    descripcion = db.Column(db.String(140), nullable=False) #COMPROBAR CON BASES SI EL TAMAÑO DE LA DESCRIPCIÓN ES CORRECTO
    monto_disponible = db.Column(db.Numeric(14, 2), nullable=False)
    monto_entradas = db.Column(db.Numeric(14, 2), nullable=False)
    monto_salidas = db.Column(db.Numeric(14, 2), nullable=False)
    fecha_registro = db.Column(db.Date, nullable=False)
    observaciones = db.Column(db.Text, nullable=False) #VER SI ESTE CAMPO ES REALMENTE NECESARIO, TENIENDO DESCRIPCION
    
    #Atributos de la tabla que son foreignKeys desde otras tablas 
    proyecto_id = db.Column(db.Numeric(10, 0), db.ForeignKey('PROYECTO.proyecto_id'), nullable=False)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('EMPRESA.empresa_id'), nullable=False)

    #Relaciones con otros objetos
    proyecto  = db.relationship('proyecto', foreign_keys=[proyecto_id])
    empresa  = db.relationship('empresa', foreign_keys=[empresa_id])


    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Tesoreria  ID={self.tesoreria_id} empresa={self.empresa_id}: disponible={self.monto_disponible}>'

class cuentaResultado (db.Model):
    __tablename__='CUENTA_RESULTADO'

    #Clave primaria
    cuenta_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    nombre = db.Column(db.String(40), nullable = False)
    tipo = db.Column(db.String(40), nullable = False)

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Resultado de Cuenta  ID={self.cuenta_id} nombre="{self.nombre}">' #Se añaden comillas a nombre por legibilidad

class detalleResultado(db.Model):
    __tablename__='DETALLE_RESULTADO'

    #Clave primaria
    detalle_resultado_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    monto = db.Column(db.Numeric(14, 2), nullable=False)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    tesoreria_id = db.Column(db.Numeric(10, 0), db.ForeignKey('TESORERIA.tesoreria_id'), nullable=False)
    cuenta_id = db.Column(db.Numeric(10, 0), db.ForeignKey('CUENTA_RESULTADO.cuenta_id'), nullable=False)

    #Relaciones con otros objetos
    tesoreria  = db.relationship('tesoreria', foreign_keys=[tesoreria_id])
    cuenta  = db.relationship('cuentaResultado', foreign_keys=[cuenta_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Detalle del resultado ID={self.detalle_resultado_id}: tesoreria={self.tesoreria_id}: monto={self.monto}>'