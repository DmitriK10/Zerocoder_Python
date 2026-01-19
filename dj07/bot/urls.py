from django.urls import path
from . import views

urlpatterns = [
    # Регистрация пользователя
    path('register/', views.register_user, name='register_user'),
    
    # Получение информации о пользователе
    path('user/<int:user_id>/', views.get_user_info, name='get_user_info'),
    
    # Получение списка всех пользователей
    path('users/', views.get_all_users, name='get_all_users'),
    
    # Удаление пользователя
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]