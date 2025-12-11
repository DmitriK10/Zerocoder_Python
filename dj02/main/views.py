from django.shortcuts import render

def index(request):
    # Первый способ передачи данных
    return render(request, 'main/index.html', {
        'caption': 'CatDjango',
        'title': 'Мой первый сайт на Django'
    })

def new(request):
    # Второй способ: через переменную
    data = {
        'page_title': 'Вторая страница',
        'description': 'Это описание второй страницы'
    }
    return render(request, 'main/new.html', data)