import unittest

from hello import greet


class GreetTests(unittest.TestCase):
    def test_default_greeting(self):
        self.assertEqual(greet(), "Hello, World!")

    def test_named_greeting(self):
        self.assertEqual(greet("Macey"), "Hello, Macey!")


if __name__ == "__main__":
    unittest.main()
