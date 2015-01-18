"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
from collections import namedtuple
import csv
import os
from lib.data_types import Const
from lib.flashcard import Flashcard


CardData = namedtuple(
    'CardData',
    ['question', 'answer', 'attempts', 'correct', 'last_shown']
)


class Deck:
    """Collection of Flashcards."""
    class ReservedWords(Const):
        """Reserved words in deck file."""
        name = 'Name:'
        quiz = 'Quiz:'

    def __init__(self, name):
        self.name = name
        self._cards = []

    def __iter__(self):
        return (c for c in self._cards)

    def __len__(self):
        return len(self._cards)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.name == other.name and
            len(self._cards) == len(other) and
            frozenset(self._cards) == frozenset([c for c in other])
        )

    # File IO
    @classmethod
    def load(cls, filename):
        """Load a deck.

        Args:
            filename (str): Path to deck file.

        Raises:
            ValueError: filename is not a valid deck.
        """
        name = ''
        deck = None
        with open(filename, 'r', newline='') as f:
            # Parse reserved keywords until we hit the beginning of quiz data.
            for line in f:
                if cls._starts_with_reserved_word(line):
                    if line.startswith(cls.ReservedWords.name):
                        name = cls._deck_name(line)
                    elif line.startswith(cls.ReservedWords.quiz):
                        break

            else:
                raise ValueError('{} not a deck file.'.format(filename))

            # Quiz data is csv.
            deck = cls(name)
            csvreader = csv.reader(f)
            for idx, row in enumerate(csvreader):
                if idx == 0:
                    continue

                card = Flashcard(*row)
                deck.add_card(card)

        return deck

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
        if os.path.isfile(filename) and not overwrite:
            raise ValueError('{} exists.'.format(filename))

        with open(filename, 'w', newline='') as f:
            deckwriter = csv.writer(f)
            deckwriter.writerow(
                [
                    '{keyword} {value}'.format(
                        keyword=self.ReservedWords.name,
                        value=self.name
                    ),
                    ]
            )
            deckwriter.writerow(
                [
                    self.ReservedWords.quiz,
                ]
            )
            deckwriter.writerow(
                Flashcard.headers().split(', ')
            )
            for c in self._cards:
                deckwriter.writerow(str(c).split(', '))

    # Deck Creation interfaces.
    def add_card(self, card):
        """Add a flashcard to the deck.

        Args:
            card (Flashcard): card to add to the deck.
        """
        self._cards.append(card)

    # Other interfaces.
    def answers(self):
        """Return a set of all answers."""
        a = frozenset((c.answer for c in self._cards))
        return a

    @classmethod
    def _starts_with_reserved_word(cls, line):
        """Starts with a reserved word.

        Returns:
            (bool):
            True -> line starts with a reserved word.
            False -> line does not start with a reserved word.
        """
        for w in cls.ReservedWords.all():
            if line.startswith(w):
                return True

        return False

    @classmethod
    def _deck_name(cls, line):
        """Extract deck name from line.

        Args:
            line (str): Name line from deck file.

        Returns:
            name (str): Deck name.
        """
        tokens = line.split(':')
        name = tokens[1].strip()

        return name
