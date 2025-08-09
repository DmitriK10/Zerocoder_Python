# *Дополнительное задание:
# Ты разрабатываешь программное обеспечение для сети магазинов. Каждый магазин в этой сети имеет свои особенности, но также
# существуют общие характеристики, такие как адрес, название и ассортимент товаров. Ваша задача — создать класс `Store`,
# который можно будет использовать для создания различных магазинов.
# Класс магазина
# Класс для представления магазина
class Store:
    def __init__(self, name, address):
        # Инициализируем атрибуты класса
        self.name = name  # Название магазина
        self.address = address  # Адрес магазина
        self.items = {}  # Словарь товаров: {товар: цена}

    def add_item(self, item, price):
        # Добавление товара в магазин
        self.items[item] = price

    def remove_item(self, item):
        #Удаление товара из магазина
        if item in self.items:
            del self.items[item]

    def get_price(self, item):
        # Возвращает цену товара или None, если товара нет
        return self.items.get(item)

    def update_price(self, item, new_price):
        # Обновление цены существующего товара
        if item in self.items:
            self.items[item] = new_price


# Создаем три магазина
store1 = Store("Фруктовый рай", "ул. Садовая, 10")
store2 = Store("ГаджетЛенд", "пр. Технический, 25")
store3 = Store("Книжная лавка", "бул. Читателей, 7")

# Добавляем товары в магазины
store1.add_item("Яблоки", 89)
store1.add_item("Бананы", 129)
store1.add_item("Апельсины", 119)

store2.add_item("Наушники", 2499)
store2.add_item("Зарядка", 899)
store2.add_item("Чехол", 499)

store3.add_item("Роман", 450)
store3.add_item("Детектив", 380)
store3.add_item("Фэнтези", 520)

# Тестируем методы на первом магазине
print("Тестируем магазин:", store1.name)
print("Список товаров начальный:", store1.items)

# Добавляем новый товар
store1.add_item("Груши", 95)
print("Список товаров после добавления груш:", store1.items)

# Обновляем цену
store1.update_price("Яблоки", 99)
print("Список товаров после обновления цены яблок:", store1.items)

# Получаем цену товара
print("Цена бананов:", store1.get_price("Бананы"))
print("Цена груш:", store1.get_price("Груши"))

# Удаляем товар
store1.remove_item("Апельсины")
print("Список товаров после удаления апельсинов:", store1.items)