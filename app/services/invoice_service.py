from app.models import Factura, Producto, db
from app.utils.pdf_generator import generate_invoice_pdf
from datetime import datetime

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
