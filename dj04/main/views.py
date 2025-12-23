from django.shortcuts import render

def home(request):
    """Главная страница"""
    return render(request, 'main/home.html')

def page2(request):
    """Второстепенная страница"""
    return render(request, 'main/page2.html')