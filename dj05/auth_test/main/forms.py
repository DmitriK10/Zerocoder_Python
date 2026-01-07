# ЗАДАНИЕ 2 СРЕДНИЙ УРОВЕНЬ: используется стандартная форма UserCreationForm

# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User

# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username', 'email', 'phone_number', 'password1', 'password2')
#     
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({
#             'placeholder': 'Введите имя пользователя'
#         })
#         self.fields['email'].widget.attrs.update({
#             'placeholder': 'Введите email'
#         })
#         self.fields['phone_number'].widget.attrs.update({
#             'placeholder': '+7XXXXXXXXXX'
#         })
#         self.fields['password1'].widget.attrs.update({
#             'placeholder': 'Введите пароль'
#         })
#         self.fields['password2'].widget.attrs.update({
#             'placeholder': 'Повторите пароль'
#         })