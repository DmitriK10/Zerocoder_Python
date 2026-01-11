#!/usr/bin/env python
"""
Скрипт для создания тестовых данных
"""
import os
import django
import sys

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from users.models import User
from orders.models import Order

def create_test_data():
    """Создание тестовых данных"""
    
    print("Создание тестовых пользователей...")
    
    # Создаем тестовых пользователей
    users_data = [
        {'email': 'user1@example.com', 'first_name': 'Иван', 'last_name': 'Иванов'},
        {'email': 'user2@example.com', 'first_name': 'Мария', 'last_name': 'Петрова'},
        {'email': 'user3@example.com', 'first_name': 'Алексей', 'last_name': 'Сидоров'},
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'password': 'testpassword123'  # В реальном проекте нужно хэшировать
            }
        )
        if created:
            created_users.append(user)
            print(f"Создан пользователь: {user.email}")
    
    print("\nСоздание тестовых заказов...")
    
    # Создаем тестовые заказы
    orders_data = [
        {'product': 'Ноутбук', 'price': 1200.00, 'status': 'delivered'},
        {'product': 'Смартфон', 'price': 800.00, 'status': 'shipped'},
        {'product': 'Наушники', 'price': 150.00, 'status': 'processing'},
        {'product': 'Монитор', 'price': 400.00, 'status': 'pending'},
        {'product': 'Клавиатура', 'price': 80.00, 'status': 'cancelled'},
    ]
    
    for i, order_data in enumerate(orders_data):
        if created_users:
            user = created_users[i % len(created_users)]
            order, created = Order.objects.get_or_create(
                user=user,
                product=order_data['product'],
                defaults={
                    'price': order_data['price'],
                    'status': order_data['status']
                }
            )
            if created:
                print(f"Создан заказ: {order.product} для {user.email}")
    
    print("\nТестовые данные успешно созданы!")
    print(f"Всего пользователей: {User.objects.count()}")
    print(f"Всего заказов: {Order.objects.count()}")

if __name__ == '__main__':
    create_test_data()