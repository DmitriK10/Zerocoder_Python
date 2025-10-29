import pandas as pd
import random

# Создаем учеников и предметы
students = ['Аня', 'Борис', 'Вика', 'Гриша', 'Даша', 'Егор', 'Женя', 'Зоя', 'Иван', 'Ксюша']
subjects = ['Математика', 'Физика', 'Химия', 'Биология', 'Литература']

# Создаем DataFrame с оценками
data = {'Ученик': students}
for subject in subjects:
    data[subject] = [random.randint(2, 5) for _ in range(len(students))]

df = pd.DataFrame(data)

print("=== АНАЛИЗ ОЦЕНОК УЧЕНИКОВ ===\n")

# Основная статистика по предметам
for subject in subjects:
    print(f"{subject}:")
    print(f"  Средняя: {df[subject].mean():.2f}")
    print(f"  Медиана: {df[subject].median()}")
    print(f"  Стандартное отклонение: {df[subject].std():.2f}")

# Квартили для математики
print(f"\nМатематика - квартили:")
print(f"  Q1: {df['Математика'].quantile(0.25)}")
print(f"  Q3: {df['Математика'].quantile(0.75)}")
print(f"  IQR: {df['Математика'].quantile(0.75) - df['Математика'].quantile(0.25)}")

# Общая статистика
print(f"\nОбщая статистика:")
print(df[subjects].describe())