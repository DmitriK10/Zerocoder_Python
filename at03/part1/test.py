# at03/part1/test.py
import pytest
from main import get_weather  # Импортируем функцию для тестирования

def test_get_weather_success(mocker):
    """
    Тестируем успешный запрос к API погоды
    
    Args:
        mocker: Фикстура pytest-mock для создания mock-объектов
    """
    # 1. Создаем mock-объект для функции requests.get
    #    Патчим (заменяем) реальную функцию на mock-объект
    mock_get = mocker.patch('main.requests.get')
    
    # 2. Настраиваем поведение mock-объекта для успешного запроса
    #    Устанавливаем статус код 200 (успех)
    mock_get.return_value.status_code = 200
    
    # 3. Настраиваем возвращаемые данные в формате JSON
    mock_get.return_value.json.return_value = {
        'weather': [{'description': 'clear sky'}],
        'main': {'temp': 282.55}  # Температура в Кельвинах
    }
    
    # 4. Подготавливаем тестовые данные
    api_key = 'test_api_key'
    city = 'London'
    
    # 5. Вызываем тестируемую функцию
    weather_data = get_weather(api_key, city)
    
    # 6. Проверяем, что функция вернула ожидаемые данные
    assert weather_data == {
        'weather': [{'description': 'clear sky'}],
        'main': {'temp': 282.55}
    }
    
    # 7. Дополнительная проверка: убеждаемся, что mock был вызван
    mock_get.assert_called_once()

def test_get_weather_failure(mocker):
    """
    Тестируем неуспешный запрос к API погоды (ошибка 404)
    
    Args:
        mocker: Фикстура pytest-mock для создания mock-объектов
    """
    # 1. Создаем mock-объект для функции requests.get
    mock_get = mocker.patch('main.requests.get')
    
    # 2. Настраиваем поведение mock-объекта для неуспешного запроса
    #    Устанавливаем статус код 404 (город не найден)
    mock_get.return_value.status_code = 404
    
    # 3. Подготавливаем тестовые данные
    api_key = 'test_api_key'
    city = 'UnknownCity'
    
    # 4. Вызываем тестируемую функцию
    weather_data = get_weather(api_key, city)
    
    # 5. Проверяем, что функция вернула None при ошибке
    assert weather_data is None
    
    # 6. Проверяем, что mock был вызван
    mock_get.assert_called_once()