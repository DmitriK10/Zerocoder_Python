# main.py в ветке dev
def area_circle(radius):
    """Вычисляет площадь круга."""
    return 3.14159 * radius ** 2

def area_rectangle(length, width):
    """Вычисляет площадь прямоугольника."""
    return length * width

# Для проверки функций потом
if __name__ == "__main__":
    print(f"Площадь круга с радиусом 5: {area_circle(5)}")
    print(f"Площадь прямоугольника 4x6: {area_rectangle(4, 6)}")
