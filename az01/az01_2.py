# AZ01 Определите среднюю зарплату (Salary) по городу (City) - используйте файл приложенный к дз - dz.csv

import pandas as pd

# Загрузка данных из файла dz.csv
dz = pd.read_csv('dz.csv')

# Группировка по городу и вычисление средней зарплаты
average_salary = dz.groupby('City')['Salary'].mean().round(2)

# Вывод результата
print("СРЕДНЯЯ ЗАРПЛАТА:")
print(f"\nСРЕДНЯЯ {dz.columns[2].upper()} ПО {dz.columns[1].upper()}:")
for city, salary in average_salary.items():
    print(f"{dz.columns[1]}: {city}, {dz.columns[2]}: {salary}")


