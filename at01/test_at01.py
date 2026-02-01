import unittest
from main_at01 import add, subtract, multiply, divide, check, modulo

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 5), 7)
        self.assertNotEqual(add(3, 7), 9)

    def test_subtract(self):
        self.assertEqual(subtract(7, 4), 3)
        self.assertNotEqual(subtract(4, 2), 1)

    def test_multiply(self):
        self.assertNotEqual(multiply(2, 5), 12)
        self.assertEqual(multiply(3, 6), 18)

    def test_divide(self):
        self.assertNotEqual(divide(4, 2), 3)
        self.assertEqual(divide(20, 5), 4)

    def test_divide_by_zero(self):
        self.assertRaises(ValueError, divide, 6, 0)

class TestCheck(unittest.TestCase):
    def test_check(self):
        self.assertTrue(check(2))
        self.assertTrue(check(6))
        self.assertTrue(check(220))
        self.assertFalse(check(1))
        self.assertFalse(check(3))
        self.assertFalse(check(57))

class TestModulo(unittest.TestCase):
    def test_modulo_success(self):
        self.assertEqual(modulo(10, 3), 1)
        self.assertEqual(modulo(20, 6), 2)
        self.assertEqual(modulo(15, 4), 3)
        self.assertEqual(modulo(8, 2), 0)

    def test_modulo_by_zero(self):
        self.assertRaises(ValueError, modulo, 10, 0)
        self.assertRaises(ValueError, modulo, 0, 0)
        self.assertRaises(ValueError, modulo, -5, 0)

    def test_modulo_negative(self):
        # В Python остаток от деления всегда неотрицательный
        self.assertEqual(modulo(-10, 3), 2)      # было -1, исправлено на 2
        self.assertEqual(modulo(10, -3), -2)     # было 1, исправлено на -2
        self.assertEqual(modulo(-10, -3), -1)    # остается -1

if __name__ == '__main__':
    unittest.main()