from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    """Менеджер для кастомной модели User"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Создание обычного пользователя"""
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя с email в качестве username
    """
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    address = models.TextField(max_length=500, blank=True, verbose_name="Адрес")
    
    # Стандартные поля для Django User
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Дата регистрации")
    
    # Обязательные поля для кастомной модели User
    USERNAME_FIELD = 'email'  # Используем email вместо username
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Обязательные поля при создании суперпользователя
    
    objects = UserManager()
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['-date_joined']  # ИСПРАВЛЕНО: date_joined вместо created_at
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def get_full_name(self):
        """Полное имя пользователя"""
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        """Короткое имя пользователя"""
        return self.first_name