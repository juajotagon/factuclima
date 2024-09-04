# app/models.py
from . import db
from datetime import datetime

class Factura(db.Model):
    __tablename__ = 'facturas'

    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String, nullable=False)
    numero_parte = db.Column(db.String, nullable=False)
    ot_number = db.Column(db.String, nullable=True)
    order_number = db.Column(db.String, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con la tabla de productos
    productos = db.relationship('Producto', backref='factura', lazy=True)

    def __repr__(self):
        return f'<Factura {self.id}>'


class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('facturas.id'), nullable=False)
    nombre_producto = db.Column(db.String, nullable=False)
    precio_producto = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre_producto} - {self.precio_producto}€>'


class ConfiguracionUsuario(db.Model):
    __tablename__ = 'configuraciones_usuarios'

    id = db.Column(db.Integer, primary_key=True)
    guardar_factura = db.Column(db.Boolean, default=True)
    guardar_parte = db.Column(db.Boolean, default=True)
    guardar_combinado = db.Column(db.Boolean, default=True)
    ruta_archivos = db.Column(db.String(255), nullable=True)
    usuario_id = db.Column(db.Integer, nullable=True)  # Puedes enlazar esto con la tabla de usuarios si tienes varios

    def __repr__(self):
        return f'<ConfiguracionUsuario {self.id}>'