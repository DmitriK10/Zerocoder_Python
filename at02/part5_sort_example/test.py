import pytest
from main import sort_list


def test_sort_list_ascending():
    """Тест сортировки списка в случайном порядке"""
    assert sort_list([3, 1, 2, 5, 4]) == [1, 2, 3, 4, 5]


def test_sort_list_descending():
    """Тест сортировки списка в убывающем порядке"""
    assert sort_list([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_sort_list_mixed():
    """Тест сортировки списка с отрицательными числами"""
    assert sort_list([-1, 3, 0, -2, 2]) == [-2, -1, 0, 2, 3]


@pytest.mark.parametrize("numbers, expected", [
    ([7, 2, 5, 3], [2, 3, 5, 7]),       # Обычный случай
    ([10, -10, 0], [-10, 0, 10]),       # С отрицательными числами
    ([], []),                           # Пустой список
    ([1], [1]),                         # Список из одного элемента
    ([5, 5, 3, 3, 1], [1, 3, 3, 5, 5]), # С дубликатами
])
def test_sort_list_parametrized(numbers, expected):
    """
    Параметризованный тест для функции sort_list
    
    Args:
        numbers (list): Список для сортировки
        expected (list): Ожидаемый отсортированный список
    """
    assert sort_list(numbers) == expected


# Комментарий:
# Тестирование крайних случаев (boundary cases):
# 1. Пустой список
# 2. Список из одного элемента
# 3. Список с дубликатами
# 4. Список с отрицательными числами