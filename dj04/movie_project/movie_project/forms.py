from django import forms
from .models import Film

class FilmForm(forms.ModelForm):
    """Форма для добавления фильма"""
    
    class Meta:
        model = Film
        fields = ['title', 'description', 'review']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название фильма'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание фильма',
                'rows': 4
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите ваш отзыв о фильме',
                'rows': 6
            }),
        }
        
        labels = {
            'title': 'Название фильма',
            'description': 'Описание фильма',
            'review': 'Ваш отзыв',
        }