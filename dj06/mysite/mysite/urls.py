"""
Основной URL-конфиг для проекта mysite
"""
from django.contrib import admin
from django.urls import path, include

# Импортируем views из приложений
from users import views as user_views
from orders import views as order_views

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),
    
    # Маршруты для приложения users
    path('login/', user_views.login, name='login'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    
    # Маршруты для приложения orders
    path('orders/', order_views.order_list, name='order_list'),
    path('orders/<int:order_id>/', order_views.order_detail, name='order_detail'),
    
    # Домашняя страница
    path('', user_views.login, name='home'),  # Перенаправляем на логин как домашнюю страницу
]