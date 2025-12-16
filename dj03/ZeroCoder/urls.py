from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),              # Старое приложение main
    path('attractions/', include('dj02.urls')),  # Новое приложение dj02
    path('news/', include('news.urls')),         # Новости dj03
]