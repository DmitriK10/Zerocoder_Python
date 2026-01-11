from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'status', 'user', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('product', 'user__email')
    ordering = ('-created_at',)