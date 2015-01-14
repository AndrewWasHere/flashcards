"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
import unittest
from lib.data_types import Const


class TestConsts(Const):
    foo = 'foo'
    bar = 'bar'
    baz = 'baz'


class DataTypesTestCase(unittest.TestCase):
    def test_access(self):
        """
        Verify that constant values are returned by references.

        :return:
        """
        self.assertEqual(TestConsts.foo, 'foo')
        self.assertEqual(TestConsts.bar, 'bar')
        self.assertEqual(TestConsts.baz, 'baz')

    def test_all(self):
        """
        Verify that defined constants are the only things returned
        in all() interface.

        :return:
        """
        consts = ['foo', 'bar', 'baz']
        for c in consts:
            self.assertTrue(c in TestConsts.all())

        for c in TestConsts.all():
            self.assertTrue(c in consts)


if __name__ == '__main__':
    unittest.main(verbosity=2)
