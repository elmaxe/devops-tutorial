import unittest
import random
from src.app import some_func

class TestApp(unittest.TestCase):
    "Blabla"

    def test_some_func(self):
        "desc"

        self.assertEqual(0, some_func())