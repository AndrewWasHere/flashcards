"""
Copyright 2015, Andrew Lin.
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
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
