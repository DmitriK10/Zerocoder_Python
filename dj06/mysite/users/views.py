from django.http import HttpResponse
from django.shortcuts import render

def login(request):
    """
    View для страницы входа (логина)
    """
    return HttpResponse('<h1>Страница входа</h1><p>Это страница для авторизации пользователей.</p>')

def register(request):
    """
    View для страницы регистрации
    """
    return HttpResponse('<h1>Страница регистрации</h1><p>Здесь пользователи могут создать новый аккаунт.</p>')

def profile(request):
    """
    View для страницы профиля пользователя
    """
    return HttpResponse('<h1>Профиль пользователя</h1><p>Информация о пользователе и настройки аккаунта.</p>')