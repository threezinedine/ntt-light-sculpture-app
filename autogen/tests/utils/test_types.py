import unittest
from utils.types import convert_type


class TypeConverterTest(unittest.TestCase):
    def test_convert_raw_type(self):
        self.assertEqual(convert_type("int"), "int")
        self.assertEqual(convert_type("float"), "float")
        self.assertEqual(convert_type("double"), "float")
        self.assertEqual(convert_type("bool"), "bool")
