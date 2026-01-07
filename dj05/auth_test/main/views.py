from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView

# ЗАДАНИЕ 2 СРЕДНИЙ УРОВЕНЬ: Используем стандартную форму UserCreationForm
from django.contrib.auth.forms import UserCreationForm

class HomeView(TemplateView):

    template_name = 'index.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    ЗАДАНИЕ 2 СРЕДНИЙ УРОВЕНЬ: 
    Страница профиля доступна только авторизованным пользователям.
    Используем LoginRequiredMixin для ограничения доступа.
    """
    template_name = 'profile.html'
    login_url = reverse_lazy('login')   # Перенаправление неавторизованных на вход

class RegisterView(CreateView):
    """
    ЗАДАНИЕ 2 СРЕДНИЙ УРОВЕНЬ: 
    Страница регистрации с формой UserCreationForm.
    После успешной регистрации - редирект на страницу входа.
    """
    form_class = UserCreationForm        # Используем стандартную форму Django
    template_name = 'register.html'
    success_url = reverse_lazy('login')  # Редирект на страницу входа после регистрации

class LoginView(AuthLoginView):

    template_name = 'login.html'

class LogoutView(AuthLogoutView):

    next_page = reverse_lazy('index')