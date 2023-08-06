#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_py_calc
----------------------------------

Tests for `py_calc` module.
"""

import unittest

#import sys
#sys.path.append('/Users/dinesh/Documents/python_packaging/py_calc')

from py_calc import calc

class TestPy_calc(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add(self):
        self.assertEqual(calc.add(10, 5), 15)
        self.assertEqual(calc.add(-1, 1), 0)
        self.assertEqual(calc.add(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(calc.subtract(10, 5), 5)
        self.assertEqual(calc.subtract(-1, 1), -2)
        self.assertEqual(calc.subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(calc.multiply(10, 5), 50)
        self.assertEqual(calc.multiply(-1, 1), -1)
        self.assertEqual(calc.multiply(-1, -1), 1)

    def test_divide(self):
        self.assertEqual(calc.divide(10, 5), 2)
        self.assertEqual(calc.divide(-1, 1), -1)
        self.assertEqual(calc.divide(-1, -1), 1)
        #self.assertEqual(calc.divide(5, 2), 2.5)

        with self.assertRaises(ValueError):
            calc.divide(10, 0)


if __name__ == '__main__':
    unittest.main()
