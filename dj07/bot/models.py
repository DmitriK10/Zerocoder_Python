from django.db import models

class TelegramUser(models.Model):
    """
    Модель для хранения пользователей Telegram.
    Сохраняет user_id, username и дату регистрации.
    """
    user_id = models.BigIntegerField(
        unique=True,
        verbose_name="Telegram User ID",
        help_text="Уникальный идентификатор пользователя в Telegram"
    )
    
    username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Telegram Username",
        help_text="Имя пользователя в Telegram (без @)"
    )
    
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="First Name",
        help_text="Имя пользователя"
    )
    
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Last Name",
        help_text="Фамилия пользователя"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Registration Date",
        help_text="Дата и время регистрации пользователя"
    )
    
    last_activity = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Activity",
        help_text="Дата и время последней активности"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
        help_text="Активен ли пользователь"
    )

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"
        ordering = ['-created_at']

    def __str__(self):
        if self.username:
            return f"@{self.username} ({self.user_id})"
        elif self.first_name:
            return f"{self.first_name} {self.last_name or ''}".strip()
        else:
            return f"User {self.user_id}"
    
    def to_dict(self):
        """Преобразование объекта в словарь"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'is_active': self.is_active
        }