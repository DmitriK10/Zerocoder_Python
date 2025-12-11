from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='zerocoder_home'),
    path('moscow/', views.moscow, name='moscow'),
    path('peter/', views.peter, name='peter'),
    path('sochi/', views.sochi, name='sochi'),
]