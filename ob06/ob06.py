#OB06 Создайте простую текстовую боевую игру, где игрок и компьютер управляют героями с различными характеристиками.
# Игра состоит из раундов, в каждом раунде игроки по очереди наносят урон друг другу, пока у одного из героев не закончится здоровье.
# Требования:
#1. Используйте ООП (Объектно-Ориентированное Программирование) для создания классов героев.
#2. Игра должна быть реализована как консольное приложение.
from abc import ABC, abstractmethod
import random

# Абстрактный класс героя
class Hero(ABC):
    def __init__(self, name, health=100, attack_power=20):
        self.name = name                    # Имя героя
        self.health = health                # Уровень здоровья
        self.attack_power = attack_power    # Сила атаки

    @abstractmethod
    def attack(self, other):
        # Абстрактный метод для атаки
        pass

    def calculate_damage(self) -> int:
        """Расчет случайного урона в диапазоне ±50% от базовой силы"""
        variation = random.randint(-10, 10)          # 50% от 20 = 10 (случайное отклонение)
        return max(1, self.attack_power + variation)    # Гарантируем минимальный урон = 1

    def is_alive(self):
        # Поверка, жив ли герой (здоровье > 0)
        return self.health > 0

    def __str__(self):
        # Строковое представление объекта
        return f"{self.name} (Здоровье: {self.health}, Сила: {self.attack_power})"


# Класс Воин
class Warrior(Hero):
    def attack(self, other):                    # Реализация метода атаки для воина
        damage = self.calculate_damage()        # Рассчет случайного урона
        other.health -= damage
        return damage


# Класс игры
class Game:
    def __init__(self, player_name):
        # Создание игроков
        self.player = Warrior(player_name)
        self.computer = Warrior("Компьютер")

    def start(self):                            # Метод, запускающий игру
        print("Начинается битва героев!")
        print(f"{self.player} vs {self.computer}")
        print("-" * 30)

        # Очередность ходов
        attackers = [self.player, self.computer]
        current = 0                             # Индекс текущего атакующего

        # Основной игровой цикл
        while self.player.is_alive() and self.computer.is_alive():
            attacker = attackers[current]
            defender = attackers[1 - current]   # Противник (0→1, 1→0)

            # Выполняется атака
            damage = attacker.attack(defender)
            print(f"{attacker.name} атакует {defender.name} и наносит {damage} урона!")
            print(f"{defender.name} осталось здоровья: {max(0, defender.health)}")
            print("-" * 30)

            # Передача хода следующему игроку
            current = 1 - current

        if self.player.is_alive():
            print(f"Победил {self.player.name}! Поздравляем!")
        else:
            print(f"Победил {self.computer.name}. Попробуйте еще раз!")


# Точка входа в программу
if __name__ == "__main__":
    print("Добро пожаловать в игру 'Битва героев'!")
    name = input("Введите имя вашего героя: ")  # Запрос имени игрока

    game = Game(name)
    game.start()