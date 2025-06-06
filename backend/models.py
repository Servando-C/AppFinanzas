# backend/models.py
from .database import db # Se importa la instancia abierta de la 'db' de app.py para crear las clases usando el modelo de la DB

#SE DEBEN PONER LOS MISMOS NOMBRES QUE EN LOS CAMPOS DE DB, VERIFICAR SI ES SENSIBLE A MAYUSCULAS O MINUSCULAS  LA DB
class empresa(db.Model):
    __tablename__ = 'empresa' 

    #Atributos de la tabla
    empresa_id = db.Column(db.Numeric(10, 0), primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    dueno = db.Column(db.String(50), nullable=False) 
    correo = db.Column(db.String(80), nullable=False)
    telefono = db.Column(db.Numeric(10, 0), nullable=False)
    direccion = db.Column(db.String(140), nullable=False)
    rfc = db.Column(db.String(12), nullable=False)

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<empresa id={self.empresa_id}: nombre="{self.nombre}">'

class usuario(db.Model):
    __tablename__ = 'usuario'

    #Atributos de la tabla
    usuario_id = db.Column(db.Numeric(10, 0), primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    correo = db.Column(db.String(80), nullable=False, unique=True)
    rfc = db.Column(db.String(13), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False) # Aumentado para almacenar hashes de contraseñas

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<usuario id={self.usuario_id}: nombre="{self.nombre}">'

class rolesEmpresa(db.Model):
    __tablename__ = 'roles_empresa'

    # Clave primaria compuesta (En este caso son también IDs en otras tablas, por eso FK)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('empresa.empresa_id'), primary_key=True) #SE DEBE USAR LOS NOMBRES DE LA TABLA PARA FK
    usuario_id = db.Column(db.Numeric(10, 0), db.ForeignKey('usuario.usuario_id'), primary_key=True)

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
    __tablename__='balance_financiero'

    #Clave primaria
    balance_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    nombre = db.Column(db.String(40), nullable=False)
    fecha_generado = db.Column(db.Date, nullable=False)
    total_activos = db.Column(db.Numeric(17, 2), nullable=False)
    total_pasivos = db.Column(db.Numeric(17, 2), nullable=False)
    capital_contable = db.Column(db.Numeric(17, 2), nullable=False)
    observaciones = db.Column(db.Text, nullable = True)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    proyecto_id = db.Column(db.Numeric(10, 0), db.ForeignKey('proyecto.proyecto_id'), nullable=False)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('empresa.empresa_id'), nullable=False)

    #Relaciones con otros objetos
    proyecto = db.relationship('proyecto', foreign_keys=[proyecto_id])
    empresa = db.relationship('empresa', foreign_keys=[empresa_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<balanceFinanciero balance_id={self.balance_id}: nombre="{self.nombre}">' #Se añaden comillas a nombre por legibilidad

class proyecto(db.Model):
    __tablename__='proyecto'

    #Clave primaria compuesta
    proyecto_id = db.Column(db.Numeric(10, 0), primary_key=True)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('empresa.empresa_id'), primary_key=True)

    #Atributos de la tabla
    nombre = db.Column(db.String(40), nullable=False)
    fecha_creacion = db.Column(db.Date, nullable=False)
    capital_disponible = db.Column(db.Numeric(16,2), nullable=False)

    #Relaciones con otros objetos
    empresa = db.relationship('empresa', backref=db.backref('empresa_proyecto')) #VERIFICAR SI SE DEBE USAR DYNAMIC U OTRO PARAM  EN LAZY

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Proyecto proyectoID={self.proyecto_id}: empresaID={self.empresa_id}: nombre="{self.nombre}">' #Se añaden comillas a nombre por legibilidad
class statusAdquisicion(db.Model):
    __tablename__='status_adquisicion'

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
    __tablename__='historico_status_adquisicion'

    #Clave primaria
    historico_status_adquisicion_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    fecha_status = db.Column(db.Date, nullable=False)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    adquisicion_id = db.Column(db.Numeric(10, 0), db.ForeignKey('adquisicion.adquisicion_id'), nullable=False)
    status_adquisicion_id = db.Column(db.Numeric(10, 0), db.ForeignKey('status_adquisicion.status_adquisicion_id'), nullable=False)

    #Relaciones con otros objetos
    adquisicion = db.relationship('adquisicion', foreign_keys=[adquisicion_id])
    status = db.relationship('statusAdquisicion', foreign_keys=[status_adquisicion_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Historico ID={self.historico_status_adquisicion_id}: fecha={self.fecha_status}>'
    
class financiamiento(db.Model):
    __tablename__='financiamiento'

    #Clave primaria
    financiamiento_id = db.Column(db.Numeric(10, 0), primary_key=True   )

    #Atributos de la tabla
    fuente = db.Column(db.String(40), nullable=False)
    porcentaje = db.Column(db.Numeric(5, 2), nullable=True)
    monto_financiado = db.Column(db.Numeric(14, 2), nullable=True)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    adquisicion_id = db.Column(db.Numeric(10, 0), db.ForeignKey('adquisicion.adquisicion_id'), nullable=False)

    #Relaciones con otros objetos
    adquisicion = db.relationship('adquisicion', foreign_keys=[adquisicion_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Financiamiento ID={self.financiamiento_id}: adquisicion={self.adquisicion_id}: monto={self.monto_financiado}>'

class formaDePago(db.Model):
    __tablename__='forma_pago'

    #Clave primaria
    forma_pago_id = db.Column(db.Numeric(10, 0), primary_key= True)

    #Atributos de la tabla
    tipo = db.Column(db.CHAR(1), nullable=False)

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Forma de pago ID={self.forma_pago_id}: tipo={self.tipo}>'

class bien(db.Model):
    __tablename__='bien'

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
    __tablename__='estado_resultado'

    #Clave primaria
    estado_resultado_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    anio = db.Column(db.Numeric(4, 0), nullable=False)
    periodo = db.Column(db.String(40), nullable=False)
    fecha_registro = db.Column(db.Date, nullable=False)
    ingreso_total = db.Column(db.Numeric(17, 2), nullable=False)
    gasto_total = db.Column(db.Numeric(17, 2), nullable=False)
    utilidad_neta = db.Column(db.Numeric(17, 2), nullable=False)
    observaciones = db.Column(db.Text, nullable=True)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    proyecto_id = db.Column(db.Numeric(10, 0), db.ForeignKey('proyecto.proyecto_id'), nullable=False)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('empresa.empresa_id'), nullable=False)

    #Relaciones con otros objetos
    proyecto  = db.relationship('proyecto', foreign_keys=[proyecto_id])
    empresa  = db.relationship('empresa', foreign_keys=[empresa_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Resultado  ID={self.estado_resultado_id}: empresa={self.empresa_id}: proyecto={self.proyecto_id}>'

class adquisicion(db.Model):
    __tablename__='adquisicion'

    #Clave primaria
    adquisicion_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    monto_total = db.Column(db.Numeric(17, 2), nullable=False)
    enganche = db.Column(db.Numeric(17, 2), nullable=True)
    fecha_adquisicion = db.Column(db.Date, nullable=False)
    numero_pagos = db.Column(db.Numeric(2, 0), nullable=True)
    periodicidad  = db.Column(db.Numeric(2, 0), nullable=True) 
    meses_pagos = db.Column(db.Numeric(2, 0), nullable=True) #Se manejará en meses con el cambio a la db

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    proyecto_id = db.Column(db.Numeric(10, 0), db.ForeignKey('proyecto.proyecto_id'), nullable=False)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('empresa.empresa_id'), nullable=False)
    bien_id = db.Column(db.Numeric(10, 0), db.ForeignKey('bien.bien_id'), nullable=False)
    forma_pago_id = db.Column(db.Numeric(10, 0), db.ForeignKey('forma_pago.forma_pago_id'), nullable=True)

    #Relaciones con otros objetos
    proyecto  = db.relationship('proyecto', foreign_keys=[proyecto_id])
    empresa  = db.relationship('empresa', foreign_keys=[empresa_id])
    bien = db.relationship('bien', foreign_keys=[bien_id])
    pago = db.relationship('formaDePago', foreign_keys=[forma_pago_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Adquisicion ID={self.adquisicion_id}: bien={self.bien_id}: empresa={self.empresa_id}: monto={self.monto_total}>'
    
class reporte(db.Model):
    __tablename__='reporte'

    #Clave primaria
    reporte_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    archivo = db.Column(db.LargeBinary, nullable=False) #SE CAMBIARÁ EN LA BASE DE DATOS PARA HACER MATCH CON ESTE MAPEO
    ruta_archivo = db.Column(db.String(255), nullable=False)
    tipo_reporte =  db.Column(db.String(40), nullable=False)
    fecha_subida = db.Column(db.Date, nullable=False)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    proyecto_id = db.Column(db.Numeric(10, 0), db.ForeignKey('proyecto.proyecto_id'), nullable=False)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('empresa.empresa_id'), nullable=False)

    #Relaciones con otros objetos
    proyecto  = db.relationship('proyecto', foreign_keys=[proyecto_id])
    empresa  = db.relationship('empresa', foreign_keys=[empresa_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<ReportePDF ID={self.reporte_id}: empresa={self.empresa_id}>'

class tesoreria(db.Model):
    __tablename__='tesoreria'

    #Clave primaria
    tesoreria_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    descripcion = db.Column(db.String(140), nullable=False) #COMPROBAR CON BASES SI EL TAMAÑO DE LA DESCRIPCIÓN ES CORRECTO
    monto_disponible = db.Column(db.Numeric(17, 2), nullable=False)
    monto_entradas = db.Column(db.Numeric(17, 2), nullable=True)
    monto_salidas = db.Column(db.Numeric(17, 2), nullable=True)
    fecha_registro = db.Column(db.Date, nullable=False)
    
    #Atributos de la tabla que son foreignKeys desde otras tablas 
    proyecto_id = db.Column(db.Numeric(10, 0), db.ForeignKey('proyecto.proyecto_id'), nullable=False)
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('empresa.empresa_id'), nullable=False)

    #Relaciones con otros objetos
    proyecto  = db.relationship('proyecto', foreign_keys=[proyecto_id])
    empresa  = db.relationship('empresa', foreign_keys=[empresa_id])


    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Tesoreria  ID={self.tesoreria_id} empresa={self.empresa_id}: disponible={self.monto_disponible}>'

class cuentaResultado (db.Model):
    __tablename__='cuenta_resultado'

    #Clave primaria
    cuenta_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    nombre = db.Column(db.String(40), nullable = False)
    tipo = db.Column(db.String(40), nullable = False)

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Resultado de Cuenta  ID={self.cuenta_id} nombre="{self.nombre}">' #Se añaden comillas a nombre por legibilidad

class detalleResultado(db.Model):
    __tablename__='detalle_resultado'

    #Clave primaria
    detalle_resultado_id = db.Column(db.Numeric(10, 0), primary_key=True)

    #Atributos de la tabla
    monto = db.Column(db.Numeric(14, 2), nullable=False)

    #Atributos de la tabla que son foreignKeys desde otras tablas 
    tesoreria_id = db.Column(db.Numeric(10, 0), db.ForeignKey('tesoreria.tesoreria_id'), nullable=False)
    cuenta_id = db.Column(db.Numeric(10, 0), db.ForeignKey('cuenta_resultado.cuenta_id'), nullable=False)

    #Relaciones con otros objetos
    tesoreria  = db.relationship('tesoreria', foreign_keys=[tesoreria_id])
    cuenta  = db.relationship('cuentaResultado', foreign_keys=[cuenta_id])

    #Función para recrear el objeto en texto, se usará su ID principal y el atributo más característico de la clase
    def __repr__(self):
        return f'<Detalle del resultado ID={self.detalle_resultado_id}: tesoreria={self.tesoreria_id}: monto={self.monto}>'