from flask import Blueprint, render_template, request, redirect, url_for, send_file
from app.models import Factura, Producto, db
from app.utils.pdf_generator import generate_invoice_pdf  # Importa la función desde utils/pdf_generator
from datetime import datetime
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/invoice', methods=['GET', 'POST'])
def invoice():
    if request.method == 'POST':
        # Captura de datos
        numero_parte = request.form.get('numero_parte')
        ot_number = request.form.get('ot_number')
        order_number = request.form.get('order_number')
        empresa = request.form.get('empresa')

        # Verificación de duplicados
        factura_existente = Factura.query.filter_by(
            numero_parte=numero_parte,
            ot_number=ot_number,
            order_number=order_number
        ).first()

        if factura_existente:
            # Si ya existe la factura, redirigir al usuario o mostrar un mensaje
            return f"Factura ya existe con Numero de Parte: {numero_parte}, OT: {ot_number}, Número de Pedido: {order_number}.", 400
        
        # Si no hay duplicados, crear la nueva factura
        nueva_factura = Factura(
            empresa=empresa,
            numero_parte=numero_parte,
            ot_number=ot_number,
            order_number=order_number,
            fecha=datetime.now()
        )
        db.session.add(nueva_factura)
        db.session.commit()

        # Crear los productos asociados a la factura
        nombres_productos = request.form.getlist('nombre_producto[]')
        precios_productos = request.form.getlist('precio_producto[]')

        for nombre, precio in zip(nombres_productos, precios_productos):
            nuevo_producto = Producto(
                factura_id=nueva_factura.id,
                nombre_producto=nombre,
                precio_producto=float(precio)
            )
            db.session.add(nuevo_producto)

        db.session.commit()

        # Generar el PDF de la factura
        productos = Producto.query.filter_by(factura_id=nueva_factura.id).all()
        pdf_file_path = generate_invoice_pdf(nueva_factura, productos)

        # Verificar que el archivo exista antes de enviarlo
        if os.path.exists(pdf_file_path):
            return send_file(pdf_file_path, as_attachment=True)
        else:
            return f"Error: El archivo {pdf_file_path} no se generó correctamente", 500

    return render_template('invoice.html')

@main.route('/facturas', methods=['GET'])
def facturas():
    # Aquí podrías implementar la lógica para mostrar todas las facturas generadas
    return "Página de facturas generadas (por implementar)"
