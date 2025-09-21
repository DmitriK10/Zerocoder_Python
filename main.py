# main.py в ветке main
def area_circle(radius):
    """Вычисляет площадь круга."""
    return 3.14159 * radius ** 2

# Для проверки функций потом
if __name__ == "__main__":
    print(f"Площадь круга с радиусом 5: {area_circle(5)}")