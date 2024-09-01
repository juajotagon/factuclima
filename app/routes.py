from flask import Blueprint, render_template, request, redirect, url_for, send_file
from app.models import Factura, Producto, db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/invoice', methods=['GET', 'POST'])
def invoice():
    if request.method == 'POST':
        # Capturar los datos generales de la factura
        numero_parte = request.form.get('numero_parte')
        ot_number = request.form.get('ot_number')
        order_number = request.form.get('order_number')
        empresa = request.form.get('empresa')

        # Capturar los productos dinámicos
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
        db.session.commit()  # Guardar la factura para obtener el ID

        # Crear los productos asociados a la factura
        for nombre, precio in zip(nombres_productos, precios_productos):
            nuevo_producto = Producto(
                factura_id=nueva_factura.id,
                nombre_producto=nombre,
                precio_producto=float(precio)
            )
            db.session.add(nuevo_producto)

        db.session.commit()  # Guardar todos los productos en la base de datos

        # Redirigir o mostrar un mensaje de éxito
        return redirect(url_for('main.index'))

    return render_template('invoice.html')
