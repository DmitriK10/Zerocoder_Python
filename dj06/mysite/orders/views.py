from django.http import HttpResponse
from django.shortcuts import render
from .models import Order

def order_list(request):
    """
    View для отображения списка заказов
    """
    orders = Order.objects.all()[:10]  # Получаем первые 10 заказов для примера
    orders_text = "<h1>Список заказов</h1><ul>"
    
    for order in orders:
        orders_text += f"<li>{order.product} - ${order.price} (Статус: {order.status})</li>"
    
    orders_text += "</ul><p>Это демонстрационная страница списка заказов.</p>"
    return HttpResponse(orders_text)

def order_detail(request, order_id):
    """
    View для детальной информации о заказе
    """
    return HttpResponse(f'<h1>Детали заказа #{order_id}</h1><p>Здесь будет подробная информация о заказе.</p>')