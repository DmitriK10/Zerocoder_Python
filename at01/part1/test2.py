import unittest
from main import add, subtract, multiply, divide

class TestMath(unittest.TestCase):
    def test_add(self):
        # Тест 1: правильный результат (2+5=7) - используем assertEqual
        self.assertEqual(add(2, 5), 7)
        # Тест 2: проверяем, что 3+7 НЕ равно 9 - используем assertNotEqual
        self.assertNotEqual(add(3, 7), 9)

    def test_subtract(self):
        # Тест 1: правильный результат (7-4=3)
        self.assertEqual(subtract(7, 4), 3)
        # Тест 2: проверяем, что 4-2 НЕ равно 1
        self.assertNotEqual(subtract(4, 2), 1)

    def test_multiply(self):
        # Тест 1: проверяем, что 2×5 НЕ равно 12
        self.assertNotEqual(multiply(2, 5), 12)
        # Тест 2: правильный результат (3×6=18)
        self.assertEqual(multiply(3, 6), 18)

    def test_divide(self):
        # Тест 1: проверяем, что 4÷2 НЕ равно 3
        self.assertNotEqual(divide(4, 2), 3)
        # Тест 2: правильный результат (20÷5=4)
        self.assertEqual(divide(20, 5), 4)

if __name__ == '__main__':
    unittest.main()