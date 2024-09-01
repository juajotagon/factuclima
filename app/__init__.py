from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializar SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///facturas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar la base de datos con la aplicación Flask
    db.init_app(app)

    # Importar modelos aquí, después de inicializar la aplicación
    with app.app_context():
        from app import models

    from .routes import main
    app.register_blueprint(main)

    return app
