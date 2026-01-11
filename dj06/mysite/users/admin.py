from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админ-панель для кастомной модели User"""
    
    # Поля для отображения в списке
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_staff', 'is_active')  # ИСПРАВЛЕНО: date_joined
    list_filter = ('is_staff', 'is_active', 'date_joined')  # ИСПРАВЛЕНО: date_joined
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)  # ИСПРАВЛЕНО: date_joined
    
    # Поля для формы редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Персональная информация'), {'fields': ('first_name', 'last_name', 'address')}),
        (_('Права доступа'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Поля для формы создания пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    # Дополнительные настройки
    filter_horizontal = ('groups', 'user_permissions',)