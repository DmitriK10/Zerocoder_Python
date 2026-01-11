from django.db import models
from django.conf import settings

class Order(models.Model):
    """
    Модель заказа для приложения orders
    Использует ForeignKey для связи с кастомной моделью User
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Пользователь"
    )
    product = models.CharField(max_length=100, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    # Статусы заказа
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('processing', 'В процессе'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name="Статус"
    )
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.product}"
    
    def get_total_price(self):
        """Метод для расчета общей стоимости"""
        return self.price