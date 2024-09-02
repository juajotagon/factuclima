from flask import Blueprint, render_template, request, redirect, url_for, send_file
from app.models import Factura, Producto, db
from datetime import datetime
from fpdf import FPDF
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/invoice', methods=['GET', 'POST'])
def invoice():
    if request.method == 'POST':
        # Captura de datos como antes
        numero_parte = request.form.get('numero_parte')
        ot_number = request.form.get('ot_number')
        order_number = request.form.get('order_number')
        empresa = request.form.get('empresa')

        nombres_productos = request.form.getlist('nombre_producto[]')
        precios_productos = request.form.getlist('precio_producto[]')

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

        # Verificar que el archivo exista antes de enviarlo
        if os.path.exists(pdf_file_path):
            return send_file(pdf_file_path, as_attachment=True)
        else:
            return "Error: El archivo no se generó correctamente", 500

        # Enviar el archivo PDF al cliente
        return send_file(pdf_file_path, as_attachment=True)

    return render_template('invoice.html')


def generate_invoice_pdf(factura, productos):
    pdf = FPDF()
    pdf.add_page()

    # Configurar la fuente Arial
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Factura", ln=True, align='C')

    pdf.cell(200, 10, txt=f"Empresa: {factura.empresa}", ln=True)
    pdf.cell(200, 10, txt=f"Número del Parte: {factura.numero_parte}", ln=True)
    if factura.ot_number:
        pdf.cell(200, 10, txt=f"OT: {factura.ot_number}", ln=True)
    if factura.order_number:
        pdf.cell(200, 10, txt=f"Número de Pedido: {factura.order_number}", ln=True)
    pdf.cell(200, 10, txt=f"Fecha: {factura.fecha.strftime('%Y-%m-%d')}", ln=True)

    pdf.ln(10)  # Espacio entre los detalles de la factura y los productos

    pdf.cell(200, 10, txt="Productos:", ln=True)

    for producto in productos:
        pdf.cell(200, 10, txt=f"{producto.nombre_producto} - {producto.precio_producto} Euros", ln=True)

    # Guardar PDF temporalmente
    pdf_file_name = f"factura_{factura.id}.pdf"
    pdf_file_path = os.path.join(os.path.abspath("instance"), pdf_file_name)
    pdf.output(pdf_file_path)
    pdf.close()

    return pdf_file_path