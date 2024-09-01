from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/invoice', methods=['GET', 'POST'])
def invoice():
    if request.method == 'POST':
        # Procesar datos del formulario
        pass
    return render_template('invoice.html')
