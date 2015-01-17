"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
import datetime


class Flashcard:
    """Question-answer pair."""
    def __init__(self, question=None, answer=None):
        # Card contents.
        self.question = question
        self.answer = answer

        # Card statistics.
        self.last_shown = None
        self.n_attempts = 0
        self.n_correct = 0

    def __str__(self):
        return '{question}, {answer}, {attempts}, {correct}, {last}'.format(
            question=self.question,
            answer=self.answer,
            attempts=self.n_attempts,
            correct=self.n_correct,
            last=str(self.last_shown) if self.last_shown else ''
        )

    def correct(self):
        """Tally a correct answer."""
        self.n_correct += 1
        self.n_attempts += 1
        self.last_shown = datetime.datetime.utcnow()

    def incorrect(self):
        """Tally an incorrect answer."""
        self.n_attempts += 1
        self.last_shown = datetime.datetime.utcnow()

    @staticmethod
    def headers():
        return 'Question, Answer, Attempts, Correct, Last Shown'