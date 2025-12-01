# Импортируем необходимые библиотеки
# Flask для создания веб-приложения
from flask import Flask, render_template, request
# Requests для отправки HTTP-запросов к API
import requests
# Random для случайного выбора API источника
import random

# Создаем экземпляр Flask приложения
# __name__ передается для определения текущего модуля
app = Flask(__name__)


def get_zenquotes():
    """Получение случайной цитаты из ZenQuotes API"""
    try:
        # URL эндпоинта API ZenQuotes для получения случайной цитаты
        url = "https://zenquotes.io/api/random"
        # Отправляем GET-запрос к API с таймаутом 5 секунд
        response = requests.get(url, timeout=5)

        # Проверяем успешность запроса (статус код 200)
        if response.status_code == 200:
            # Преобразуем ответ из JSON формата в словарь Python
            data = response.json()
            # Проверяем, что данные получены и не пустые
            if data and len(data) > 0:
                # Возвращаем словарь с данными цитаты
                return {
                    'quote': data[0]['q'],  # Текст цитаты
                    'author': data[0]['a'],  # Автор цитаты
                    'source': 'ZenQuotes API',  # Источник данных
                    'status': 'success'  # Статус успешного получения
                }
        # Если статус код не 200 или данные пустые, возвращаем ошибку
        return {'status': 'error', 'message': 'ZenQuotes API временно недоступен'}
    except:
        # Обрабатываем любые исключения (например, проблемы с сетью)
        return {'status': 'error', 'message': 'ZenQuotes API временно недоступен'}


def get_quoteslate():
    """Получение случайной цитаты из Quoteslate API"""
    try:
        # URL эндпоинта API Quoteslate для получения случайной цитаты
        url = "https://quoteslate.vercel.app/api/quotes/random"
        # Отправляем GET-запрос к API с таймаутом 5 секунд
        response = requests.get(url, timeout=5)

        # Проверяем успешность запроса (статус код 200)
        if response.status_code == 200:
            # Преобразуем ответ из JSON формата в словарь Python
            data = response.json()
            # Возвращаем словарь с данными цитаты
            return {
                'quote': data['quote'],  # Текст цитаты
                'author': data['author'],  # Автор цитаты
                'source': 'Quoteslate API',  # Источник данных
                'status': 'success'  # Статус успешного получения
            }
        # Если статус код не 200, возвращаем ошибку
        return {'status': 'error', 'message': 'Quoteslate API временно недоступен'}
    except:
        # Обрабатываем любые исключения (например, проблемы с сетью)
        return {'status': 'error', 'message': 'Quoteslate API временно недоступен'}


# Декоратор Flask для определения маршрута и методов HTTP
# '/' - корневой путь приложения
# methods=['GET', 'POST'] - разрешенные методы запроса
@app.route('/', methods=['GET', 'POST'])
def index():
    """Главная страница со случайной цитатой"""
    # Инициализируем переменные
    quote_data = None  # Будет хранить данные о цитате
    warning = None  # Будет хранить предупреждение о переключении API
    current_api = None  # Будет хранить информацию о текущем используемом API

    # Обрабатываем как GET, так и POST запросы
    if request.method == 'POST' or request.method == 'GET':
        # Случайно выбираем API для первого запроса
        # random.choice выбирает один из двух вариантов
        api_choice = random.choice(['zenquotes', 'quoteslate'])

        # Если случайно выбран ZenQuotes
        if api_choice == 'zenquotes':
            # Пытаемся получить цитату из ZenQuotes
            quote_data = get_zenquotes()

            # Если получение прошло успешно
            if quote_data['status'] == 'success':
                # Запоминаем, что используем ZenQuotes API
                current_api = 'ZenQuotes API'
            else:
                # Если ZenQuotes не работает, пробуем Quoteslate
                quote_data = get_quoteslate()

                # Если Quoteslate работает
                if quote_data['status'] == 'success':
                    # Запоминаем, что используем Quoteslate API
                    current_api = 'Quoteslate API'
                    # Создаем предупреждение о переключении
                    warning = f"ZenQuotes API временно недоступен. Используется альтернативный сервис: {current_api}"
                else:
                    # Если оба API не работают
                    current_api = 'Ни один сервис'

        # Если случайно выбран Quoteslate
        else:
            # Пытаемся получить цитату из Quoteslate
            quote_data = get_quoteslate()

            # Если получение прошло успешно
            if quote_data['status'] == 'success':
                # Запоминаем, что используем Quoteslate API
                current_api = 'Quoteslate API'
            else:
                # Если Quoteslate не работает, пробуем ZenQuotes
                quote_data = get_zenquotes()

                # Если ZenQuotes работает
                if quote_data['status'] == 'success':
                    # Запоминаем, что используем ZenQuotes API
                    current_api = 'ZenQuotes API'
                    # Создаем предупреждение о переключении
                    warning = f"Quoteslate API временно недоступен. Используется альтернативный сервис: {current_api}"
                else:
                    # Если оба API не работают
                    current_api = 'Ни один сервис'

    # Рендерим HTML шаблон, передавая данные
    # render_template загружает index.html из папки templates
    # и подставляет в него переданные переменные
    return render_template('index.html',
                           quote=quote_data,
                           warning=warning,
                           current_api=current_api)


# Точка входа в приложение
# Этот блок выполняется только при прямом запуске файла
if __name__ == '__main__':
    # Запускаем Flask приложение
    # debug=True включает режим отладки (автоперезагрузка при изменениях)
    app.run(debug=True)