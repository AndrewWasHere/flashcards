"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
import datetime


class Flashcard:
    def __init__(self, question=None, answer=None):
        # Card contents.
        self.question = question
        self.answer = answer

        # Card statistics.
        self._last_shown = None
        self._attempts = 0
        self._correct = 0

    def __str__(self):
        return '{question}, {answer}, {attempts}, {correct}, {last}'.format(
            question=self.question,
            answer=self.answer,
            attempts=self._attempts,
            correct=self._correct,
            last=str(self._last_shown) if self._last_shown else ''
        )

    def correct(self):
        """
        Tally a correct answer.

        :return:
        """
        self._correct += 1
        self._attempts += 1
        self._last_shown = datetime.datetime.utcnow()

    def incorrect(self):
        """
        Tally an incorrect answer.

        :return:
        """
        self._attempts += 1
        self._last_shown = datetime.datetime.utcnow()

    @staticmethod
    def headers():
        return 'Question, Answer, Attempts, Correct, Last Shown'