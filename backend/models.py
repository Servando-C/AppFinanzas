# backend/models.py
from .app import db # Se importa la instancia abierta de la 'db' de app.py para crear las clases

#SE DEBEN PONER LOS MISMOS NOMBRES QUE EN LOS CAMPOS DE DB, VERIFICAR SI ES SENSIBLE A CARACTERES LA DB

# Modelo para la tabla EMPRESA
class Empresa(db.Model):
    __tablename__ = 'empresa' 

    empresa_id = db.Column(db.Numeric(10, 0), primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    dueño = db.Column(db.String(40), nullable=False) 
    correo = db.Column(db.String(40), nullable=False)
    telefono = db.Column(db.Numeric(10, 0), nullable=False)
    direccion = db.Column(db.String(140), nullable=False)
    rfc = db.Column(db.String(12), nullable=False)

#LAS RELACIONES SON LAS RELACIONES ENTRE TABLAS
    # Relaciones (las definiremos con más detalle después, por ahora es un placeholder)
    # proyectos = db.relationship('Proyecto', backref='empresa', lazy=True)
    # usuarios_roles = db.relationship('RolesEmpresa', backref='empresa', lazy=True)

    def __repr__(self):
        return f'<Empresa {self.empresa_id}: {self.nombre}>'

# Modelo para la tabla USUARIO
class Usuario(db.Model):
    __tablename__ = 'usuario'

    usuario_id = db.Column(db.Numeric(10, 0), primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)
    correo = db.Column(db.String(60), nullable=False, unique=True)
    rfc = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False) # Aumentado para almacenar hashes de contraseñas

    # Relaciones
    # roles_empresas = db.relationship('RolesEmpresa', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.usuario_id}: {self.nombre}>'

# Modelo para la tabla ROLES_EMPRESA
class RolesEmpresa(db.Model):
    __tablename__ = 'roles_empresa'

    # Clave primaria compuesta
    empresa_id = db.Column(db.Numeric(10, 0), db.ForeignKey('empresa.empresa_id'), primary_key=True)
    usuario_id = db.Column(db.Numeric(10, 0), db.ForeignKey('usuario.usuario_id'), primary_key=True)

    # Roles como booleanos, según tu ERD
    rol_capturista = db.Column(db.Boolean, nullable=False, default=False)
    rol_admin = db.Column(db.Boolean, nullable=False, default=False)
    rol_jefe = db.Column(db.Boolean, nullable=False, default=False) # Asumo que ROL_JEFE es un rol
    rol_financiero = db.Column(db.Boolean, nullable=False, default=False) # Asumo que ROL_FINANCIERO es un rol

    # Definir relaciones para acceder fácilmente a los objetos Empresa y Usuario
    empresa = db.relationship('Empresa', backref=db.backref('roles_asignados', lazy='dynamic'))
    usuario = db.relationship('Usuario', backref=db.backref('roles_en_empresas', lazy='dynamic'))


    def __repr__(self):
        return f'<RolesEmpresa Usuario:{self.usuario_id} Empresa:{self.empresa_id}>'

