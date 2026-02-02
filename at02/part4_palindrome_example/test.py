import pytest
from main import is_palindrome


def test_is_palindrome_true():
    """Тест для слова-палиндрома"""
    assert is_palindrome("madam") == True


def test_is_palindrome_false():
    """Тест для слова, не являющегося палиндромом"""
    assert is_palindrome("hello") == False


@pytest.mark.parametrize("s, expected", [
    ("racecar", True),   # racecar - палиндром
    ("python", False),   # python - не палиндром
    ("level", True),     # level - палиндром
    ("", True),          # Пустая строка считается палиндромом
    ("a", True),         # Строка из одного символа - палиндром
    ("ab", False),       # "ab" не равно "ba"
])
def test_is_palindrome_parametrized(s, expected):
    """
    Параметризованный тест для функции is_palindrome
    
    Args:
        s (str): Тестируемая строка
        expected (bool): Ожидаемый результат
    """
    assert is_palindrome(s) == expected


# Комментарий:
# Пустая строка считается палиндромом, потому что:
# 1. Она читается одинаково слева направо и справа налево
# 2. Это соглашение упрощает многие алгоритмы