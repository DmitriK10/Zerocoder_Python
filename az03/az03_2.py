#AZ03 2. Построй диаграмму рассеяния для двух наборов случайных данных, сгенерированных с помощью функции `numpy.random.rand`.​
#import numpy as np
#random_array = np.random.rand(5) # массив из 5 случайных чисел
#print(random_array)
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)                  # Для воспроизводимости результатов
x = np.random.rand(100) * 10        # 100 случайных чисел от 0 до 10
y = np.random.rand(100) * 10        # 100 случайных чисел от 0 до 10

# Построение диаграммы рассеяния
plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.7, c='green', edgecolors='black', s=50)
plt.title('Диаграмма рассеяния случайных данных')
plt.xlabel('X (случайные значения)')
plt.ylabel('Y (случайные значения)')
plt.grid(True, alpha=0.3)

# Добавление линии тренда
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, p(x), "r--", alpha=0.8, linewidth=2, label=f'Линия тренда: y={z[0]:.2f}x+{z[1]:.2f}')
plt.legend()

plt.show()

# Вывод корреляции
correlation = np.corrcoef(x, y)[0, 1]
print(f"Коэффициент корреляции: {correlation:.4f}")