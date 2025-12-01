from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)


def get_zenquotes():
    """Получение случайной цитаты из ZenQuotes API"""
    try:
        url = "https://zenquotes.io/api/random"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return {
                    'quote': data[0]['q'],
                    'author': data[0]['a'],
                    'source': 'ZenQuotes API',
                    'status': 'success'
                }
        return {'status': 'error', 'message': 'ZenQuotes API временно недоступен'}
    except:
        return {'status': 'error', 'message': 'ZenQuotes API временно недоступен'}


def get_quoteslate():
    """Получение случайной цитаты из Quoteslate API"""
    try:
        url = "https://quoteslate.vercel.app/api/quotes/random"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return {
                'quote': data['quote'],
                'author': data['author'],
                'source': 'Quoteslate API',
                'status': 'success'
            }
        return {'status': 'error', 'message': 'Quoteslate API временно недоступен'}
    except:
        return {'status': 'error', 'message': 'Quoteslate API временно недоступен'}


@app.route('/', methods=['GET', 'POST'])
def index():
    """Главная страница со случайной цитатой"""
    quote_data = None
    warning = None
    current_api = None  # Добавляем переменную для хранения информации об используемом API

    if request.method == 'POST' or request.method == 'GET':
        # Случайно выбираем API для запроса
        api_choice = random.choice(['zenquotes', 'quoteslate'])

        if api_choice == 'zenquotes':
            quote_data = get_zenquotes()
            if quote_data['status'] == 'success':
                current_api = 'ZenQuotes API'
            else:
                # Если ZenQuotes не работает, пробуем Quoteslate
                quote_data = get_quoteslate()
                if quote_data['status'] == 'success':
                    current_api = 'Quoteslate API'
                    warning = f"ZenQuotes API временно недоступен. Используется альтернативный сервис: {current_api}"
                else:
                    current_api = 'Ни один сервис'
        else:
            quote_data = get_quoteslate()
            if quote_data['status'] == 'success':
                current_api = 'Quoteslate API'
            else:
                # Если Quoteslate не работает, пробуем ZenQuotes
                quote_data = get_zenquotes()
                if quote_data['status'] == 'success':
                    current_api = 'ZenQuotes API'
                    warning = f"Quoteslate API временно недоступен. Используется альтернативный сервис: {current_api}"
                else:
                    current_api = 'Ни один сервис'

    return render_template('index.html', quote=quote_data, warning=warning, current_api=current_api)


if __name__ == '__main__':
    app.run(debug=True)