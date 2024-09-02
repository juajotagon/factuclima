import os
from fpdf import FPDF
from flask import current_app

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

    # Guardar PDF en la estructura Empresa/Año/Mes
    pdf_file_name = f"factura_{factura.id}.pdf"
    pdf_storage_path = current_app.config['PDF_STORAGE_PATH']
    empresa_dir = os.path.join(pdf_storage_path, factura.empresa)
    year_dir = os.path.join(empresa_dir, str(factura.fecha.year))
    month_dir = os.path.join(year_dir, str(factura.fecha.month))

    # Crear el directorio si no existe
    os.makedirs(month_dir, exist_ok=True)

    pdf_file_path = os.path.join(month_dir, pdf_file_name)
    pdf.output(pdf_file_path)
    pdf.close()

    return pdf_file_path
