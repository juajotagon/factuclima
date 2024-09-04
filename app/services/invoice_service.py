from app.models import Factura, Producto, db
from app.utils.pdf_generator import generate_invoice_pdf
from datetime import datetime
from pypdf import PdfWriter
from io import BytesIO
import os

def crear_factura(numero_parte, ot_number, order_number, empresa):
    # Verificación de duplicados
    factura_existente = Factura.query.filter_by(
        numero_parte=numero_parte,
        ot_number=ot_number,
        order_number=order_number
    ).first()

    if factura_existente:
        return None, f"Factura ya existe con Numero de Parte: {numero_parte}, OT: {ot_number}, Número de Pedido: {order_number}."

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

    return nueva_factura, None

def crear_productos(factura_id, nombres_productos, precios_productos):
    productos = []
    for nombre, precio in zip(nombres_productos, precios_productos):
        nuevo_producto = Producto(
            factura_id=factura_id,
            nombre_producto=nombre,
            precio_producto=float(precio)
        )
        db.session.add(nuevo_producto)
        productos.append(nuevo_producto)

    db.session.commit()
    return productos

def generar_factura_pdf(factura, productos):
    pdf_file_path = generate_invoice_pdf(factura, productos)
    return pdf_file_path


def manejar_archivos(factura_pdf, parte_pdf, factura_id):
    ruta_archivos = session.get('ruta_archivos', '/ruta/por/defecto')
    
    if session.get('guardar_factura'):
        # Guardar la factura generada en PDF
        factura_pdf_path = os.path.join(ruta_archivos, f'factura_{factura_id}.pdf')
        with open(factura_pdf_path, 'wb') as f:
            f.write(factura_pdf)

    if session.get('guardar_parte'):
        # Guardar el PDF del "parte"
        parte_pdf_path = os.path.join(ruta_archivos, f'parte_{factura_id}.pdf')
        with open(parte_pdf_path, 'wb') as f:
            f.write(parte_pdf)

    if session.get('guardar_combinado'):
        # Combinar ambos PDFs
        combinado_pdf = combinar_pdfs(factura_pdf, parte_pdf)
        combinado_pdf_path = os.path.join(ruta_archivos, f'factura_combinada_{factura_id}.pdf')
        with open(combinado_pdf_path, 'wb') as f:
            f.write(combinado_pdf)

    return True

def combinar_pdfs(factura_pdf, parte_pdf):
    # Función para combinar PDFs en memoria
    pdf_writer = PdfWriter()

    pdf_writer.add_page(factura_pdf)
    pdf_writer.add_page(parte_pdf)

    # Usamos un buffer de memoria
    buffer = BytesIO()
    pdf_writer.write(buffer)
    buffer.seek(0)

    return buffer.read()