#AZ03 1. Создай гистограмму для случайных данных, сгенерированных с помощью функции `numpy.random.normal`.
# Параметры нормального распределения
#mean = 0 # Среднее значение
#std_dev = 1 # Стандартное отклонение
#num_samples = 1000 # Количество образцов
# Генерация случайных чисел, распределенных по нормальному распределению
#data = np.random.normal(mean, std_dev, num_samples)
import numpy as np
import matplotlib.pyplot as plt

mean = 0                        # Среднее значение
std_dev = 1                     # Стандартное отклонение
num_samples = 1000              # Количество образцов

data = np.random.normal(mean, std_dev, num_samples)

# Построение гистограммы
plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, edgecolor='black', alpha=0.7, color='skyblue')
plt.title('Гистограмма нормального распределения')
plt.xlabel('Значение')
plt.ylabel('Частота')
plt.grid(True, alpha=0.3)
plt.axvline(mean, color='red', linestyle='dashed', linewidth=2, label=f'Среднее = {mean}')
plt.legend()
plt.show()

# Вывод статистики
print(f"Среднее значение: {np.mean(data):.4f}")
print(f"Стандартное отклонение: {np.std(data):.4f}")