# at03/part2/test.py
import pytest
from main import get_github_user  # Импортируем функцию для тестирования

def test_get_github_user_success(mocker):
    """
    Тестируем успешный запрос к GitHub API
    
    Args:
        mocker: Фикстура pytest-mock для создания mock-объектов
    """
    # 1. Создаем mock-объект для функции requests.get
    mock_get = mocker.patch('main.requests.get')
    
    # 2. Настраиваем поведение mock-объекта
    mock_get.return_value.status_code = 200
    
    # 3. Настраиваем возвращаемые данные
    mock_get.return_value.json.return_value = {
        'login': 'nizavr',
        'id': 345178,
        'name': 'Nina'
    }
    
    # 4. Вызываем тестируемую функцию
    #    Важно: передаем любое имя пользователя, так как мы мокируем ответ
    user_data = get_github_user('cat')
    
    # 5. Проверяем результат
    assert user_data == {
        'login': 'nizavr',
        'id': 345178,
        'name': 'Nina'
    }
    
    # 6. Проверяем, что mock был вызван с правильными аргументами
    mock_get.assert_called_once_with('https://api.github.com/users/cat')

def test_get_github_user_failure(mocker):
    """
    Тестируем неуспешный запрос к GitHub API (ошибка сервера)
    
    Args:
        mocker: Фикстура pytest-mock для создания mock-объектов
    """
    # 1. Создаем mock-объект
    mock_get = mocker.patch('main.requests.get')
    
    # 2. Настраиваем статус код 500 (внутренняя ошибка сервера)
    mock_get.return_value.status_code = 500
    
    # 3. Вызываем функцию
    user_data = get_github_user('cat')
    
    # 4. Проверяем, что функция вернула None при ошибке
    assert user_data is None
    
    # 5. Проверяем вызов mock
    mock_get.assert_called_once_with('https://api.github.com/users/cat')