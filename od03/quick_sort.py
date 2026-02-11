# Быстрая сортировка (Quick Sort)
def quick_sort(s):
    # 1. Базовый случай рекурсии: если длина списка <= 1, возвращаем его
    if len(s) <= 1:
        return s

    # 2. Выбираем опорный элемент (первый элемент списка)
    element = s[0]

    # 3. Формируем левую часть: элементы меньше опорного
    left = list(filter(lambda i: i < element, s))

    # 4. Формируем центральную часть: элементы равные опорному
    center = [i for i in s if i == element]

    # 5. Формируем правую часть: элементы больше опорного
    right = list(filter(lambda i: i > element, s))

    # 6. Рекурсивно сортируем левую и правую части, объединяем с центром
    return quick_sort(left) + center + quick_sort(right)

# 7. Тестируем алгоритм на примере
print(quick_sort([5, 2, 9, 0, 1, 5, 3]))