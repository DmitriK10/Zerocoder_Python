import unittest
from main import divide

class TestDivide(unittest.TestCase):
    def test_divide_success(self):
        #Тестируем успешные случаи деления#
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(6, 3), 2)
        self.assertEqual(divide(70, 2), 35)

    def test_divide_by_zero(self):
        #Тестируем деление на ноль - должно вызывать ValueError#
        self.assertRaises(ValueError, divide, 6, 0)

if __name__ == '__main__':
    unittest.main()