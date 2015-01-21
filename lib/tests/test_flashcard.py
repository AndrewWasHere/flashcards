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
    """Unittests for Flashcard class."""
    def test_construction_defaults(self):
        """Constructor tests -- defaults."""
        card = Flashcard()

        self.assertEqual(card.question, None)
        self.assertEqual(card.answer, None)
        self.assertEqual(card.n_attempts, 0)
        self.assertEqual(card.n_correct, 0)
        self.assertEqual(card.last_shown, None)

    def test_construction(self):
        """Constructor tests."""
        def verify(c):
            self.assertEqual(c.question, question)
            self.assertEqual(c.answer, answer)
            self.assertEqual(c.n_attempts, attempts)
            self.assertEqual(c.n_correct, correct)
            self.assertEqual(c.last_shown, timestamp)

        question = 'q'
        answer = 'a'
        attempts = 42
        correct = 17
        timestamp = datetime.utcnow()

        card = Flashcard(question, answer, attempts, correct, str(timestamp))
        verify(card)

        card = Flashcard(
            question,
            answer,
            str(attempts),
            str(correct),
            str(timestamp)
        )
        verify(card)

    def test_correct(self):
        """correct interface tests."""
        card = Flashcard('question', 'answer')
        correct = card.n_correct
        attempts = card.n_attempts
        card.correct()

        self.assertEqual(card.n_correct, correct + 1)
        self.assertEqual(card.n_attempts, attempts + 1)
        self.assertTrue(isinstance(card.last_shown, datetime))

    def test_incorrect(self):
        """incorrect() interface tests."""
        card = Flashcard('question', 'answer')
        correct = card.n_correct
        attempts = card.n_attempts
        card.incorrect()

        self.assertEqual(card.n_correct, correct)
        self.assertEqual(card.n_attempts, attempts + 1)
        self.assertTrue(isinstance(card.last_shown, datetime))

    def test_display(self):
        """Display interfaces (__str__ and header) tests."""
        card = Flashcard('Question', 'Answer')
        card.n_attempts = 'Attempts'
        card.n_correct = 'Correct'
        card.last_shown = 'Last Shown'
        self.assertEqual(str(card), card.headers())

    def test_equality(self):
        """__eq__() interface tests."""
        card = Flashcard('q', 'a', 2027, 19, str(datetime.utcnow()))
        card_prime = Flashcard('q', 'a', 27, 9, str(datetime.utcnow()))

        self.assertEqual(card, card)
        self.assertNotEqual(card, card_prime)
        self.assertNotEqual(card, str(card))

    def test_hash(self):
        """__hash__() interface tests."""
        card = Flashcard('q', 'a', 2027, 19, str(datetime.utcnow()))
        card_prime = Flashcard('q', 'a', 27, 9, str(datetime.utcnow()))

        _ = {card: card_prime}  # Hashable items can be dictionary keys.
        self.assertEqual(hash(card), hash(card))
        self.assertNotEqual(hash(card), hash(card_prime))


if __name__ == '__main__':
    unittest.main(verbosity=2)
