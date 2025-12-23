from django.shortcuts import render, redirect
from .models import Film
from .forms import FilmForm

def home(request):
    """Главная страница - список всех фильмов"""
    films = Film.objects.all().order_by('-created_at')
    return render(request, 'films/films_list.html', {'films': films})

def add_film(request):
    """Страница для добавления нового фильма"""
    error = ''
    
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('films_home')
        else:
            error = "Пожалуйста, исправьте ошибки в форме."
    else:
        form = FilmForm()
    
    return render(request, 'films/add_film.html', {'form': form, 'error': error})