# at03/part1/main.py
import requests

def get_weather(api_key, city):
    """
    Функция для получения данных о погоде через OpenWeatherMap API
    
    Args:
        api_key (str): API ключ для доступа к сервису
        city (str): Название города
    
    Returns:
        dict: Данные о погоде в формате JSON или None при ошибке
    """
    # Формируем URL запроса с использованием f-строки
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    
    # Отправляем GET-запрос к API
    response = requests.get(url)
    
    # Проверяем статус код ответа
    if response.status_code == 200:
        # При успешном запросе возвращаем данные в формате JSON
        return response.json()
    else:
        # При ошибке возвращаем None
        return None