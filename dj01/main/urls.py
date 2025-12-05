from django.urls import path
from . import views  # или from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
]