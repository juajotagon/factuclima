from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

mail = Mail()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    mail.init_app(app)
    db.init_app(app)

    # Registrar blueprints y otras configuraciones
    from .routes import main
    app.register_blueprint(main)

    return app