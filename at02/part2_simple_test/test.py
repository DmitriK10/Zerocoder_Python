import pytest
from main import check


def test_check():
    """Тест для четного числа"""
    assert check(6) == True  # 6 - четное число, ожидаем True


def test_check2():
    """Тест для нечетного числа"""
    assert check(3) == False  # 3 - нечетное число, ожидаем False


# Запуск тестов:
# В терминале перейти в папку step2_simple_test и выполнить:
# pytest test.py -v