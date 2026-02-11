# Сортировка выбором (Selection Sort)
def selection_sort(arr):
    # 1. Проходим по всему списку
    for i in range(len(arr)):
        # 2. Предполагаем, что минимальный элемент - первый в неотсортированной части
        min_index = i

        # 3. Ищем минимальный элемент в оставшейся части списка
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j

        # 4. Меняем местами найденный минимальный элемент с первым в неотсортированной части
        arr[i], arr[min_index] = arr[min_index], arr[i]

# 5. Пример использования
numbers = [64, 25, 12, 22, 11]
selection_sort(numbers)
print(numbers)  # [11, 12, 22, 25, 64]