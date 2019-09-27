from django.test import TestCase
from app.calc import add, subtract


class CalcTests(TestCase):

    def test_add_numbers(self):
        """Test that two numbers are added"""
        self.assertEqual(add(3, 8), 11)

    def test_subtract_numbers(self):
        """Tests that difference between numbers is correct"""
        self.assertEqual(subtract(3, 8), -5)
