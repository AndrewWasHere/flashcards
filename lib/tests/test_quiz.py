"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from lib import quiz
from lib.flashcard import Flashcard


class QuizTestCase(unittest.TestCase):
    """Unittests for Quiz class."""
    def test_initialization(self):
        """Initialization tests."""
        deck_filename = 'filename'

        with patch.object(quiz.Deck, 'load') as mock_load:
            q = quiz.Quiz(deck_filename)

        mock_load.assert_called_with(deck_filename)
        self.assertEqual(q.score(), (0, 0))

    def test_fill_in_the_blank(self):
        """Fill in the blank, correct answer tests."""
        deck_filename = 'filename'
        # cards = []
        card1 = self.mocked_card('q1', 'a')
        card2 = self.mocked_card('q2', 'a')
        cards = [card1, card2]
        card_questions = [c.question for c in cards]
        mocked_deck = MagicMock(spec=quiz.Deck)
        mocked_deck.__iter__.return_value = cards
        mocked_deck.__len__.return_value = len(cards)

        with patch.object(quiz.Deck, 'load', return_value=mocked_deck):
            q = quiz.Quiz(deck_filename)
            for idx, question in enumerate(
                q.run(
                    'all',
                    quiz.QuizTypes.fill_in_the_blank
                )
            ):
                self.assertTrue(question.question in card_questions)
                question.submit('a')

            mocked_deck.answers.assert_not_called()
            self.assertEqual(idx, len(cards) - 1)
            self.assertEqual(q.score()[0], len(cards))
            self.assertEqual(q.score()[1], len(cards))

    def test_fill_in_the_blank_incorrect(self):
        """Fill in the blank, incorrect answer tests."""
        deck_filename = 'filename'
        # cards = []
        card1 = self.mocked_card('q1', 'a')
        card2 = self.mocked_card('q2', 'a')
        cards = [card1, card2]
        card_questions = [c.question for c in cards]
        mocked_deck = MagicMock(spec=quiz.Deck)
        mocked_deck.__iter__.return_value = cards
        mocked_deck.__len__.return_value = len(cards)

        with patch.object(quiz.Deck, 'load', return_value=mocked_deck):
            q = quiz.Quiz(deck_filename)
            for idx, question in enumerate(
                q.run(
                    'all',
                    quiz.QuizTypes.fill_in_the_blank
                )
            ):
                self.assertTrue(question.question in card_questions)
                question.submit('b')

            mocked_deck.answers.assert_not_called()
            self.assertEqual(idx, len(cards) - 1)
            self.assertEqual(q.score()[0], 0)
            self.assertEqual(q.score()[1], len(cards))

    def test_multiple_choice_correct(self):
        """Multiple choice, correct answer tests."""

    def test_multiple_choice_incorrect(self):
        """Multiple choice, incorrect answer tests."""

    def mocked_card(self, question, answer):
        card = MagicMock(spec=Flashcard)
        card.question = question
        card.answer = answer
        card.n_correct = 0
        card.n_attempts = 0
        return card

if __name__ == '__main__':
    unittest.main(verbosity=2)
