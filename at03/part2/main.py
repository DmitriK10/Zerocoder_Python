# at03/part2/main.py
import requests

def get_github_user(username):
    """
    Функция для получения данных о пользователе GitHub
    
    Args:
        username (str): Имя пользователя GitHub
    
    Returns:
        dict: Данные пользователя в формате JSON или None при ошибке
    """
    # Формируем URL запроса к GitHub API
    url = f'https://api.github.com/users/{username}'
    
    # Отправляем GET-запрос
    response = requests.get(url)
    
    # Проверяем статус код ответа
    if response.status_code == 200:
        # При успешном запросе возвращаем данные в формате JSON
        return response.json()
    else:
        # При ошибке возвращаем None
        return None