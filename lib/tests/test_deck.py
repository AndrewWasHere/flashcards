"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
import unittest
from lib.deck import Deck


class DeckTestCase(unittest.TestCase):
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

    def test_iterate(self):
        """Iteration tests."""
        deck_name = 'test deck'
        cards = ['card 0', 'card 1', 'card 2']
        deck = Deck(deck_name)
        for c in cards:
            deck.add_card(c)

        deck_cards = [c for c in deck]
        self.assertEqual(frozenset(cards), frozenset(deck_cards))


if __name__ == '__main__':
    unittest.main(verbosity=2)
