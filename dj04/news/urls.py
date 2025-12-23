from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='news_home'),
    path('create/', views.create_news, name='add_news'),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
]