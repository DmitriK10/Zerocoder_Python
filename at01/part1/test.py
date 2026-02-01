import unittest
from main import add, subtract, multiply, divide

class TestMath(unittest.TestCase):
    def test_add(self):
        # Тест 1: правильный результат (2+5=7)
        self.assertEqual(add(2, 5), 7)
        # Тест 2: НЕПРАВИЛЬНЫЙ результат (3+7≠9)
        self.assertEqual(add(3, 7), 9)  # Эта строка вызовет ошибку!

    def test_subtract(self):
        # Тест 1: правильный результат (7-4=3)
        self.assertEqual(subtract(7, 4), 3)
        # Тест 2: НЕПРАВИЛЬНЫЙ результат (4-2≠1)
        self.assertEqual(subtract(4, 2), 1)  # Эта строка вызовет ошибку!

    def test_multiply(self):
        # Тест 1: НЕПРАВИЛЬНЫЙ результат (2×5≠12)
        self.assertEqual(multiply(2, 5), 12)  # Эта строка вызовет ошибку!
        # Тест 2: правильный результат (3×6=18)
        self.assertEqual(multiply(3, 6), 18)

    def test_divide(self):
        # Тест 1: НЕПРАВИЛЬНЫЙ результат (4÷2≠3)
        self.assertEqual(divide(4, 2), 3)  # Эта строка вызовет ошибку!
        # Тест 2: правильный результат (20÷5=4)
        self.assertEqual(divide(20, 5), 4)

if __name__ == '__main__':
    unittest.main()