from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import News_post
from .forms import News_postForm


def home(request):
    """Отображение всех новостей"""
    news = News_post.objects.all().order_by('-pub_date')  # сортируем по дате (новые сверху)
    return render(request, 'news/news.html', {'news': news})


def create_news(request):
    """Создание новой новости"""
    error = ''  # Переменная для хранения ошибки

    if request.method == 'POST':
        # Если форма отправлена
        form = News_postForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_home')
        else:
            error = "Пожалуйста, исправьте ошибки в форме."
    else:
        # Если просто зашли на страницу
        form = News_postForm()

    return render(request, 'news/add_new_post.html', {'form': form, 'error': error})


def news_detail(request, news_id):
    """Детальное отображение новости"""
    news_item = get_object_or_404(News_post, id=news_id)
    return render(request, 'news/news_detail.html', {'news': news_item})