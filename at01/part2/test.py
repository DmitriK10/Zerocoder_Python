import unittest
from main import check

class TestCheck(unittest.TestCase):
    def test_check(self):
        # Тестируем четные числа - должны возвращать True
        self.assertTrue(check(2))
        self.assertTrue(check(6))
        self.assertTrue(check(220))
        
        # Тестируем нечетные числа - должны возвращать False
        self.assertFalse(check(1))
        self.assertFalse(check(3))
        self.assertFalse(check(57))

if __name__ == '__main__':
    unittest.main()