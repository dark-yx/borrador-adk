from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

if __name__ == "__main__":
    from api.main import app
    with app.app_context():
        db.create_all()
        print("Tablas creadas correctamente.")
