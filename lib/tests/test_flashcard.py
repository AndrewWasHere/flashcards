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
        self.assertEqual(card.n_attempts, 0)
        self.assertEqual(card.n_correct, 0)
        self.assertEqual(card.last_shown, None)

    def test_correct(self):
        """
        Test correct interface.
        """
        card = Flashcard('question', 'answer')
        correct = card.n_correct
        attempts = card.n_attempts
        card.correct()

        self.assertEqual(card.n_correct, correct + 1)
        self.assertEqual(card.n_attempts, attempts + 1)
        self.assertTrue(isinstance(card.last_shown, datetime))

    def test_incorrect(self):
        """
        Test incorrect interface.
        """
        card = Flashcard('question', 'answer')
        correct = card.n_correct
        attempts = card.n_attempts
        card.incorrect()

        self.assertEqual(card.n_correct, correct)
        self.assertEqual(card.n_attempts, attempts + 1)
        self.assertTrue(isinstance(card.last_shown, datetime))

    def test_display(self):
        """
        Test display interfaces (__str__ and header).
        """
        card = Flashcard('Question', 'Answer')
        card.n_attempts = 'Attempts'
        card.n_correct = 'Correct'
        card.last_shown = 'Last Shown'
        self.assertEqual(str(card), card.headers())

if __name__ == '__main__':
    unittest.main(verbosity=2)
