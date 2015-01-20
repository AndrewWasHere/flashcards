"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
import unittest
from lib.quiz import QuizTools


class QuizToolsTestCase(unittest.TestCase):
    def test_correct_below_threshold(self):
        self.assertTrue(
            QuizTools.correct_below_threshold(0, 0, 0.0)
        )
        self.assertTrue(
            QuizTools.correct_below_threshold(1, 2, 0.5)
        )
        self.assertFalse(
            QuizTools.correct_below_threshold(2, 3, 0.5)
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
