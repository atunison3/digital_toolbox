# tests/test_other.py

import unittest

from digital_toolbox.other import foo


class TestOther(unittest.TestCase):
    def test_foo(self):
        result = foo()
        expected = "Hello World"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
