"""
Copyright 2015, Andrew Lin.
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from lib import quiz
from lib.flashcard import Flashcard


def mocked_card(question, answer, correct=0, attempts=0):
    card = MagicMock(spec=Flashcard)
    card.question = question
    card.answer = answer
    card.n_correct = correct
    card.n_attempts = attempts
    return card


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
        card1 = mocked_card('q1', 'a')
        card2 = mocked_card('q2', 'a')
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
        card1 = mocked_card('q1', 'a')
        card2 = mocked_card('q2', 'a')
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


class CardComparatorsTestCase(unittest.TestCase):
    def setUp(self):
        deck_filename = 'filename'
        card1 = mocked_card('q1', 'a')
        card2 = mocked_card('q2', 'a')
        cards = [card1, card2]
        mocked_deck = MagicMock(spec=quiz.Deck)
        mocked_deck.__iter__.return_value = cards
        mocked_deck.__len__.return_value = len(cards)

        with patch.object(quiz.Deck, 'load', return_value=mocked_deck):
            self.quiz = quiz.Quiz(deck_filename)

    def test_is_hard(self):
        """Quiz._is_hard() method test."""
        for card in [
            mocked_card('q', 'a', 0, 0),
            mocked_card('q', 'a', 70, 100),
            mocked_card('q', 'a', 2, 2),
        ]:
            self.assertTrue(self.quiz._is_hard(card))

    def test_is_not_hard(self):
        """Quiz._is_hard() method test."""
        card = mocked_card('q', 'a', 80, 100)

        self.assertFalse(self.quiz._is_hard(card))

    def test_is_medium(self):
        """Quiz._is_medium() method test."""
        for card in [
            mocked_card('q', 'a', 9, 9),
            mocked_card('q', 'a', 85, 100)
        ]:
            self.assertTrue(self.quiz._is_medium(card))

    def test_is_not_medium(self):
        """Quiz._is_medium() method test."""
        card = mocked_card('q', 'a', 95, 100)

        self.assertFalse(self.quiz._is_medium(card))


class DeckIteratorTestCase(unittest.TestCase):
    def setUp(self):
        self.hard_cards = [
            mocked_card('hard question', 'hard answer', 4, 10),
            mocked_card('hard question', 'hard answer', 5, 10),
            mocked_card('hard question', 'hard answer', 6, 10),
            mocked_card('hard question', 'hard answer', 7, 10),
        ]
        self.medium_cards = [
            mocked_card('medium question', 'medium answer', 8, 10),
            mocked_card('medium question', 'medium answer', 85, 100),
            mocked_card('medium question', 'medium answer', 5, 5),
        ]
        self.easy_cards = [
            mocked_card('easy question', 'easy answer', 95, 100),
            mocked_card('easy question', 'easy answer', 100, 100),
        ]
        self.cards = self.hard_cards + self.medium_cards + self.easy_cards
        self.mocked_deck = MagicMock(spec=quiz.Deck)
        self.mocked_deck.__iter__.return_value = self.cards
        self.mocked_deck.__len__.return_value = len(self.cards)

    def test_sort_deck(self):
        """Quiz._sort_deck() method test."""
        with patch.object(quiz.Deck, 'load', return_value=self.mocked_deck):
            q = quiz.Quiz('mocked deck')

        h, m, e = q._sort_deck(self.mocked_deck)

        self.assertEqual(len(h), len(self.hard_cards))
        self.assertEqual(len(m), len(self.medium_cards))
        self.assertEqual(len(e), len(self.easy_cards))
        self.assertEqual(frozenset(h), frozenset(self.hard_cards))
        self.assertEqual(frozenset(m), frozenset(self.medium_cards))
        self.assertEqual(frozenset(e), frozenset(self.easy_cards))

    def test_card_generator(self):
        """Quiz._card_generator() method test."""
        hard_weight = 3
        medium_weight = 2
        easy_weight = 1
        n_cards = hard_weight + medium_weight + easy_weight

        with patch.object(quiz.Deck, 'load', return_value=self.mocked_deck):
            q = quiz.Quiz(
                'mocked deck',
                hard_weight,
                medium_weight,
                easy_weight
            )

        h = []
        m = []
        e = []
        for count, c in enumerate(q._card_generator()):
            if count >= n_cards:
                break

            if c.question.startswith('hard'):
                h.append(c)
            elif c.question.startswith('medium'):
                m.append(c)
            elif c.question.startswith('easy'):
                e.append(c)
            else:
                raise ValueError('Unexpected card in deck: {}'.format(c))

        self.assertEqual(len(h), hard_weight)
        self.assertEqual(len(m), medium_weight)
        self.assertEqual(len(e), easy_weight)

    def test_deck_runner(self):
        """Quiz._deck_runner() method test."""
        hard_weight = 3
        medium_weight = 2
        easy_weight = 1
        n_cards = hard_weight + medium_weight + easy_weight
        mult = 2

        with patch.object(quiz.Deck, 'load', return_value=self.mocked_deck):
            q = quiz.Quiz(
                'mocked deck',
                hard_weight,
                medium_weight,
                easy_weight
            )

        h = []
        m = []
        e = []
        for c in q._deck_runner(mult * n_cards):
            if c.question.startswith('hard'):
                h.append(c)
            elif c.question.startswith('medium'):
                m.append(c)
            elif c.question.startswith('easy'):
                e.append(c)
            else:
                raise ValueError('Unexpected card in deck: {}'.format(c))

        self.assertEqual(len(h), mult * hard_weight)
        self.assertEqual(len(m), mult * medium_weight)
        self.assertEqual(len(e), mult * easy_weight)


if __name__ == '__main__':
    unittest.main(verbosity=2)
