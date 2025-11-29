from app import app, db
from app.models import User

# Очистка БД
with app.app_context():
    db.drop_all()
    print("Database tables dropped successfully!")