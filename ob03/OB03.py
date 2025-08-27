###Создайте базовый класс `Animal`, который будет содержать общие атрибуты (например, `name`, `age`) и методы (`make_sound()`, `eat()`) для всех животных.
###2. Реализуйте наследование, создав подклассы `Bird`, `Mammal`, и `Reptile`, которые наследуют от класса `Animal`. Добавьте специфические атрибуты и переопределите методы, если требуется (например, различный звук для `make_sound()`).
###3. Продемонстрируйте полиморфизм: создайте функцию `animal_sound(animals)`, которая принимает список животных и вызывает метод `make_sound()` для каждого животного.
###4. Используйте композицию для создания класса `Zoo`, который будет содержать информацию о животных и сотрудниках. Должны быть методы для добавления животных и сотрудников в зоопарк.
###5. Создайте классы для сотрудников, например, `ZooKeeper`, `Veterinarian`, которые могут иметь специфические методы (например, `feed_animal()` для `ZooKeeper` и `heal_animal()` для `Veterinarian`).
###Дополнительно:
###Попробуйте добавить дополнительные функции в вашу программу, такие как сохранение информации о зоопарке в файл и возможность её загрузки, чтобы у вашего зоопарка было "постоянное состояние" между запусками программы.
# Главный класс для животных
class Animal:
    def __init__(self, name, age):
        self.name = name                        # Имя животного
        self.age = age                          # Возраст животного

    def make_sound(self):
        return f"{self.name} издает звук"       # Общий звук для всех животных

    def eat(self):
        return f"{self.name} кушает"            # Животное ест

# Класс для птиц
class Bird(Animal):
    def make_sound(self):
        return f"{self.name} говорит: Чирик!"   # Специфический звук птицы

# Класс для млекопитающих
class Mammal(Animal):
    def make_sound(self):
        return f"{self.name} говорит: Рррр!"   # Специфический звук млекопитающего

# Класс для рептилий
class Reptile(Animal):
    def make_sound(self):
        return f"{self.name} говорит: Шшшш!"   # Специфический звук рептилии

# Класс для смотрителя зоопарка
class ZooKeeper:
    def __init__(self, name):
        self.name = name                            # Имя смотрителя

    def feed_animal(self, animal):
        return f"{self.name} кормит {animal.name}"  # Метод кормления животного

# Класс для ветеринара
class Veterinarian:
    def __init__(self, name):
        self.name = name                            # Имя ветеринара

    def heal_animal(self, animal):
        return f"{self.name} лечит {animal.name}"   # Метод лечения животного

# Главный класс для зоопарка
class Zoo:
    def __init__(self, name):
        self.name = name                            # Название зоопарка
        self.animals = []                           # Список животных в зоопарке
        self.employees = []                         # Список сотрудников зоопарка

    def add_animal(self, animal):
        self.animals.append(animal)                 # Добавляем животное в список
        print(f"Добавлено животное: {animal.name}")

    def add_employee(self, employee):
        self.employees.append(employee)             # Добавляем сотрудника в список
        print(f"Добавлен сотрудник: {employee.name}")

# Демонстрация работы
print("=== ЗООПАРК ===")

# Создаем зоопарк
my_zoo = Zoo("ЗОО")

# Создаем животных
animal1 = Bird("Попугай Кеша", 2)
animal2 = Mammal("Тигр Лео", 5)
animal3 = Reptile("Удав Гена", 3)

# Добавляем животных
my_zoo.add_animal(animal1)
my_zoo.add_animal(animal2)
my_zoo.add_animal(animal3)

# Создаем сотрудников
keeper = ZooKeeper("Иван")
vet = Veterinarian("Мария")

# Добавляем сотрудников
my_zoo.add_employee(keeper)
my_zoo.add_employee(vet)

# Демонстрируем работу сотрудников
print(f"{keeper.feed_animal(animal1)}")
print(f"{vet.heal_animal(animal2)}")

new_zoo = Zoo("Новый зоопарк")
