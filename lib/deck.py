"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""


class Deck:
    """Collection of Flashcards."""
    def __init__(self, name):
        self.name = name
        self._cards = []

    def __iter__(self):
        return (c for c in self._cards)

    def __len__(self):
        return len(self._cards)

    # File IO
    @classmethod
    def load(cls, filename):
        """Load a deck.

        Args:
            filename (str): Path to deck file.

        Raises:
            ValueError: filename is not a valid deck.
        """

    def save(self, filename, overwrite=False):
        """Save the deck to file.

        Args:
            filename (str): Path to deck file.
            overwrite (bool): Overwrite existing file flag.
                True -> Overwrite file if it exists.
                False -> Raise exception if file exists.

        Raises:
            ValueError: filename exists.
        """

    # Deck Creation interfaces.
    def add_card(self, card):
        """Add a flashcard to the deck.

        Args:
            card (Flashcard): card to add to the deck.
        """
        self._cards.append(card)

    # Other interfaces.
    def answers(self):
        """
        Return a set of all answers.
        """
        a = frozenset((c.answer for c in self._cards))
        return a