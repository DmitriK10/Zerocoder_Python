# Допустим, мы получили двумерный список с числами в виде строк
data = [
    ['100', '200', '300'],
    ['400', '500', '600']
]

numbers = []   # список для хранения преобразованных чисел

for row in data:
    for text in row:
        number = int(text)   # преобразование строки в целое число
        numbers.append(number)

print(numbers)