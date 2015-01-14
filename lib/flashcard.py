"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""


class Flashcard:
    def __init__(self):
        # Card contents.
        self.question = None
        self.answer = None

        # Card statistics.
        self._last_shown = None
        self._attempts = None
        self._correct = None

    def correct(self):
        """
        Tally a correct answer.

        :return:
        """
        self._correct += 1
        self._attempts += 1

    def incorrect(self):
        """
        Tally an incorrect answer.

        :return:
        """
        self._attempts += 1