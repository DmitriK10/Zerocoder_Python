data = [
    [100, 110, 120],
    [400, 500, 600],
    [150, 130, 140]
]

filtered = []   # список для отфильтрованных значений

for row in data:
    for item in row:
        if item > 190:      # условие отбора
            filtered.append(item)

print(filtered)