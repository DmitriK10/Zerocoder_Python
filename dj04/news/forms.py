from django import forms
from .models import News_post


class News_postForm(forms.ModelForm):
    """Форма для создания/редактирования новости"""

    class Meta:
        model = News_post
        fields = ['title', 'short_description', 'text', 'pub_date']

        # Настраиваем виджеты для стилизации
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок новости'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Краткое описание (максимум 200 символов)'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Полный текст новости',
                'rows': 5
            }),
            'pub_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'  # HTML5 input для даты и времени
            }),
        }

        # Необязательно: можно добавить подсказки
        help_texts = {
            'pub_date': 'Укажите дату и время публикации',
        }