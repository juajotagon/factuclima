from flask import Blueprint, render_template, request, redirect, url_for, send_file
from app.models import Factura, Producto, db
from app.utils.pdf_generator import generate_invoice_pdf
from datetime import datetime
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/invoice', methods=['GET', 'POST'])
def invoice():
    # Obtener todas las facturas para mostrarlas en el desplegable
    facturas = Factura.query.all()
    factura = None  # Inicializamos la variable factura como None

    if request.method == 'POST':
        # Captura de datos
        numero_parte = request.form.get('numero_parte')
        ot_number = request.form.get('ot_number')
        order_number = request.form.get('order_number')
        empresa = request.form.get('empresa')
        nombres_productos = request.form.getlist('nombre_producto[]')
        precios_productos = request.form.getlist('precio_producto[]')

        # Validaciones
        if not numero_parte or not empresa:
            return "Número de parte y Empresa son campos obligatorios.", 400
        if any(not nombre for nombre in nombres_productos):
            return "Todos los productos deben tener un nombre.", 400
        if any(not precio or float(precio) <= 0 for precio in precios_productos):
            return "Todos los productos deben tener un precio válido mayor que 0.", 400

        # Verificación de duplicados
        factura_existente = Factura.query.filter_by(
            numero_parte=numero_parte,
            ot_number=ot_number,
            order_number=order_number
        ).first()

        if factura_existente:
            return f"Factura ya existe con Numero de Parte: {numero_parte}, OT: {ot_number}, Número de Pedido: {order_number}.", 400
        
        # Crear la nueva factura
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

        if os.path.exists(pdf_file_path):
            return send_file(pdf_file_path, as_attachment=True)
        else:
            return f"Error: El archivo {pdf_file_path} no se generó correctamente", 500
    
    # Verificar si hay una factura seleccionada mediante el parámetro 'factura_id' en la URL
    factura_id = request.args.get('factura_id')
    if factura_id:
        factura = Factura.query.get(factura_id)

    # Renderizar la plantilla con las facturas y la factura seleccionada
    return render_template('invoice.html', facturas=facturas, factura=factura)


@main.route('/facturas', methods=['GET'])
def facturas():
    # Obtener los parámetros de filtrado desde la solicitud
    numero_parte = request.args.get('numero_parte')
    ot_number = request.args.get('ot_number')
    order_number = request.args.get('order_number')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Construir la consulta de filtrado
    query = Factura.query

    if numero_parte:
        query = query.filter(Factura.numero_parte.like(f'%{numero_parte}%'))
    if ot_number:
        query = query.filter(Factura.ot_number.like(f'%{ot_number}%'))
    if order_number:
        query = query.filter(Factura.order_number.like(f'%{order_number}%'))
    if start_date:
        query = query.filter(Factura.fecha >= start_date)
    if end_date:
        query = query.filter(Factura.fecha <= end_date)

    # Ejecutar la consulta para obtener las facturas filtradas
    facturas = query.all()

    # Recopilar todos los productos asociados a las facturas filtradas
    productos_filtrados = []
    total_acumulado = 0
    for factura in facturas:
        for producto in factura.productos:
            productos_filtrados.append({
                'factura_id': factura.id,
                'numero_parte': factura.numero_parte,
                'ot_number': factura.ot_number,
                'order_number': factura.order_number,
                'fecha': factura.fecha.strftime('%Y-%m-%d'),
                'nombre_producto': producto.nombre_producto,
                'precio_producto': producto.precio_producto
            })
            total_acumulado += producto.precio_producto

    # Renderizar la página con los productos filtrados y el total acumulado
    return render_template('facturas.html', productos=productos_filtrados, total_acumulado=total_acumulado)

@main.route('/send_invoice_mock/<int:factura_id>', methods=['POST'])
def send_invoice_mock(factura_id):
    factura = Factura.query.get_or_404(factura_id)

    factura.correo_enviado = True
    factura.fecha_envio = datetime.now()

    db.session.commit()

    return f"Mockup: Correo enviado correctamente para la factura {factura.id}"
