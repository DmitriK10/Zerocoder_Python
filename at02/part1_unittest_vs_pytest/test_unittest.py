import unittest


class TestMath(unittest.TestCase):
    """Тестовый класс для математических операций"""
    
    def test_add(self):
        """Тест сложения"""
        self.assertEqual(1 + 1, 2)  # Сравниваем 1+1 с 2
        
    def test_subtract(self):
        """Тест вычитания"""
        self.assertEqual(3 - 2, 1)  # Сравниваем 3-2 с 1


if __name__ == "__main__":
    unittest.main()  # Запуск тестов