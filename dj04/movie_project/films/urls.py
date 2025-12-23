from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='films_home'),
    path('add/', views.add_film, name='add_film'),
]