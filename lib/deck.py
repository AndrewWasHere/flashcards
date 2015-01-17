"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""


class Deck:
    def __init__(self, name):
        self.name = name
        self._cards = []

    def __iter__(self):
        """
        Deck iterator.
        """
        return (c for c in self._cards)

    def __len__(self):
        """
        Number of cards in the deck.
        """
        return len(self._cards)

    # File IO
    @classmethod
    def load(cls, filename):
        """
        Load a deck.
        """

    def save(self, filename):
        """
        Save the deck to file.
        """

    # Deck Creation interfaces.
    def append(self, card):
        """
        Add a flashcard to the deck.
        """
        self._cards.append(card)

    # Other interfaces.
    def answers(self):
        """
        Return a set of all answers.
        """
        a = frozenset((c.answer for c in self._cards))
        return a