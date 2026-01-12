from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash_contrasena = db.Column(db.String(255), nullable=False)
    palabra_clave = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    foto_perfil = db.Column(db.String(255), default='default.jpg')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones - SIN cascade delete para mantener historial
    productos = db.relationship('Producto', backref='vendedor', lazy=True)
    ordenes = db.relationship('Orden', backref='comprador', lazy=True)
    direcciones = db.relationship('Direccion', backref='usuario', lazy=True, cascade='all, delete-orphan')
    metodos_pago = db.relationship('MetodoPago', backref='usuario', lazy=True, cascade='all, delete-orphan')
    resenas = db.relationship('Resena', backref='usuario', lazy=True)
    
    def establecer_contrasena(self, contrasena):
        """Establece la contraseña del usuario con hash"""
        self.hash_contrasena = generate_password_hash(contrasena)
    
    def verificar_contrasena(self, contrasena):
        """Verifica si la contraseña es correcta"""
        return check_password_hash(self.hash_contrasena, contrasena)
    
    def obtener_contrasena_plana(self):
        """Solo para Super Admin - NO se puede recuperar la contraseña original"""
        return "*** (hasheada, no recuperable)"
    
    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'


class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    imagen = db.Column(db.String(255), default='producto_default.jpg')
    esta_aprobado = db.Column(db.Boolean, default=False)
    id_vendedor = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)  # Nullable para mantener historial
    nombre_vendedor = db.Column(db.String(80))  # Guardar nombre del vendedor
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    items_orden = db.relationship('ItemOrden', backref='producto', lazy=True)
    resenas = db.relationship('Resena', backref='producto', lazy=True, cascade='all, delete-orphan')
    
    def calificacion_promedio(self):
        """Calcula el promedio de calificaciones del producto"""
        if not self.resenas:
            return 0
        return sum(r.calificacion for r in self.resenas) / len(self.resenas)
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'


class Orden(db.Model):
    __tablename__ = 'ordenes'
    
    id = db.Column(db.Integer, primary_key=True)
    id_comprador = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)  # Nullable para mantener historial
    nombre_comprador = db.Column(db.String(80))  # Guardar nombre del comprador
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), default='Pendiente')
    id_direccion_envio = db.Column(db.Integer, db.ForeignKey('direcciones.id'))
    id_metodo_pago = db.Column(db.Integer, db.ForeignKey('metodos_pago.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    items = db.relationship('ItemOrden', backref='orden', lazy=True, cascade='all, delete-orphan')
    direccion_envio = db.relationship('Direccion', foreign_keys=[id_direccion_envio])
    metodo_pago = db.relationship('MetodoPago', foreign_keys=[id_metodo_pago])
    
    def __repr__(self):
        return f'<Orden {self.id}>'


class ItemOrden(db.Model):
    __tablename__ = 'items_orden'
    
    id = db.Column(db.Integer, primary_key=True)
    id_orden = db.Column(db.Integer, db.ForeignKey('ordenes.id'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=True)  # Nullable para mantener historial
    nombre_producto = db.Column(db.String(200))  # Guardar nombre del producto
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<ItemOrden {self.id}>'


class Direccion(db.Model):
    __tablename__ = 'direcciones'
    
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    calle = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(20), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    es_predeterminada = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Direccion {self.calle}, {self.ciudad}>'


class MetodoPago(db.Model):
    __tablename__ = 'metodos_pago'
    
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_tarjeta = db.Column(db.String(20), default='credito')  # 'credito' o 'debito'
    ultimos4_tarjeta = db.Column(db.String(4), nullable=False)
    titular_tarjeta = db.Column(db.String(100), nullable=False)
    mes_vencimiento = db.Column(db.Integer, nullable=False)
    anio_vencimiento = db.Column(db.Integer, nullable=False)
    es_predeterminado = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<MetodoPago ****{self.ultimos4_tarjeta}>'


class Resena(db.Model):
    __tablename__ = 'resenas'
    
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)  # Nullable para mantener reseñas
    nombre_usuario = db.Column(db.String(80))  # Guardar nombre del usuario
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Resena {self.id} - {self.calificacion} estrellas>'