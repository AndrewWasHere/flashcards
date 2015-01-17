"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
import unittest
from lib.data_types import Const


class TestConsts(Const):
    """Constants to test."""
    foo = 'foo'
    bar = 'bar'
    baz = 'baz'


class ConstTestCase(unittest.TestCase):
    """Unittests for Const class."""
    def test_access(self):
        """Constant access tests."""
        self.assertEqual(TestConsts.foo, 'foo')
        self.assertEqual(TestConsts.bar, 'bar')
        self.assertEqual(TestConsts.baz, 'baz')

    def test_all(self):
        """all() interface tests."""
        consts = ['foo', 'bar', 'baz']
        for c in consts:
            self.assertTrue(c in TestConsts.all())

        for c in TestConsts.all():
            self.assertTrue(c in consts)


if __name__ == '__main__':
    unittest.main(verbosity=2)
