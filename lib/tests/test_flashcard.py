"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
from datetime import datetime
import unittest
from lib.flashcard import Flashcard


class FlashcardTestCase(unittest.TestCase):
    def test_construction(self):
        """
        Test construction of a flashcard.
        """
        question = 'q'
        answer = 'a'
        card = Flashcard(question, answer)

        self.assertEqual(card.question, question)
        self.assertEqual(card.answer, answer)
        self.assertEqual(card._attempts, 0)
        self.assertEqual(card._correct, 0)
        self.assertEqual(card._last_shown, None)

    def test_correct(self):
        """
        Test correct interface.
        """
        card = Flashcard('question', 'answer')
        correct = card._correct
        attempts = card._attempts
        card.correct()

        self.assertEqual(card._correct, correct + 1)
        self.assertEqual(card._attempts, attempts + 1)
        self.assertTrue(isinstance(card._last_shown, datetime))

    def test_incorrect(self):
        """
        Test incorrect interface.
        """
        card = Flashcard('question', 'answer')
        correct = card._correct
        attempts = card._attempts
        card.incorrect()

        self.assertEqual(card._correct, correct)
        self.assertEqual(card._attempts, attempts + 1)
        self.assertTrue(isinstance(card._last_shown, datetime))

    def test_display(self):
        """
        Test display interfaces (__str__ and header).
        """
        card = Flashcard('Question', 'Answer')
        card._attempts = 'Attempts'
        card._correct = 'Correct'
        card._last_shown = 'Last Shown'
        self.assertEqual(str(card), card.headers())

if __name__ == '__main__':
    unittest.main(verbosity=2)
