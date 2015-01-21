"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
import datetime
import tempfile
import unittest
from lib.deck import Deck, CardData
from lib.flashcard import Flashcard


class DeckCreationTestCase(unittest.TestCase):
    """Unittests for Deck class."""
    def test_creation(self):
        """Constructor tests."""
        deck_name = 'test deck'
        deck = Deck(deck_name)
        self.assertEqual(deck.name, deck_name)
        self.assertEqual(len(deck), 0)

    def test_add_card(self):
        """add_card() interface tests."""
        deck_name = 'test deck'
        cards = ['card 0', 'card 1', 'card 2']
        deck = Deck(deck_name)
        for idx, c in enumerate(cards, 1):
            deck.add_card(c)
            self.assertEqual(len(deck), idx)


class DeckManipulationTestCase(unittest.TestCase):
    def setUp(self):
        self.deck_name = 'test deck'
        self.deck = Deck(self.deck_name)
        self.cards = [
            Flashcard('q0', 'a0', 0, 0, str(datetime.datetime.utcnow())),
            Flashcard('q1', 'a1', 0, 0, str(datetime.datetime.utcnow())),
            Flashcard('q2', 'a2', 0, 0, str(datetime.datetime.utcnow()))
        ]
        for c in self.cards:
            self.deck.add_card(c)

    def test_iterate(self):
        """Iteration tests."""
        self.assertEqual(
            frozenset(c for c in self.deck),
            frozenset(self.cards)
        )

    def test_len(self):
        """__len__() tests."""
        self.assertEqual(len(self.cards), len(self.deck))

    def test_equality(self):
        """__eq__() tests."""
        other_deck = Deck('other deck')
        for c in self.cards:
            other_deck.add_card(c)

        other_other_deck = Deck(self.deck_name)

        self.assertEqual(self.deck, self.deck)
        self.assertNotEqual(self.deck, other_deck)
        self.assertNotEqual(self.deck, other_other_deck)
        self.assertNotEqual(self.deck, 'not a deck')

    def test_load_and_save(self):
        """load() and save() interface tests."""
        # Save and load the deck.
        with tempfile.NamedTemporaryFile(mode='w', newline='') as tf:
            self.deck.save(tf.name, overwrite=True)
            saved_deck = Deck.load(tf.name)

        # Test.
        self.assertEqual(saved_deck, self.deck)

    def test_sample_deck_file(self):
        """Load sample deck from README.md test."""
        sample = """Name: Sample Deck
Quiz:
Question,Answer,Attempts,Correct,Last Shown
1 + 1, 2
1 + 2, 3
1 + 3, 4
1 + 4, 5
1 + 5, 6
1 + 6, 7
1 + 7, 8
1 + 8, 9
1 + 9, 10
"""
        with tempfile.NamedTemporaryFile(mode='w', newline='') as tf:
            with open(tf.name, 'w') as f:
                f.write(sample)

            saved_deck = Deck.load(tf.name)
            self.assertEqual(saved_deck.name, 'Sample Deck')
            self.assertEqual(len(saved_deck), 9)

    def test_answers(self):
        """answers() interface tests."""
        expected_answers = frozenset([c.answer for c in self.cards])
        self.assertEqual(frozenset(self.deck.answers()), expected_answers)


class DeckUtilsTestCase(unittest.TestCase):
    """Unittests for Deck utilities."""
    def test_starts_with_reserved_word(self):
        """_starts_with_reserved_word() interface tests."""
        for w in Deck.ReservedWords.all():
            self.assertTrue(
                Deck._starts_with_reserved_word(
                    '{} is a reserved word'.format(w)
                )
            )

    def test_does_not_start_with_reserved_word(self):
        """_starts_with_reserved_word() interface tests."""
        self.assertFalse(
            Deck._starts_with_reserved_word('This is not a reserved word.')
        )

    def test_deck_name(self):
        """_deck_name() interface tests."""
        deck_name = 'Mr. Neutron'
        named = Deck._deck_name(
            '{} {}'.format(Deck.ReservedWords.name, deck_name)
        )

        self.assertEqual(named, deck_name)

if __name__ == '__main__':
    unittest.main(verbosity=2)
