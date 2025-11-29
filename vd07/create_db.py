from app import app, db
from app.models import User

# Создание БД
with app.app_context():
    db.create_all()
    print("Database created successfully!")

