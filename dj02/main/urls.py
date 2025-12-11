from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),      # Добавляем name='home'
    path('new/', views.new, name='page2'),   # Добавляем name='page2'
]