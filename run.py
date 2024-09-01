from app import create_app, db

app = create_app()

# Crear la base de datos
with app.app_context():
    db.create_all()  # Crea todas las tablas

if __name__ == "__main__":
    app.run(debug=True)
