"""
Copyright 2015, Andrew Lin.
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
import datetime


class Flashcard:
    """Question-answer pair."""
    def __init__(
        self,
        question=None,
        answer=None,
        attempts=0,
        correct=0,
        last_shown=None
    ):
        # Card contents.
        self.question = question.strip() if question else None
        self.answer = answer.strip() if question else None

        # Card statistics.
        self.n_attempts = int(attempts) if attempts else 0
        self.n_correct = int(correct) if correct else 0
        self.last_shown = datetime.datetime.strptime(
            last_shown.strip(),
            '%Y-%m-%d %H:%M:%S.%f'
        ) if last_shown else None

    def __eq__(self, other):
        result = (
            isinstance(other, self.__class__) and
            self.question == other.question and
            self.answer == other.answer and
            self.n_attempts == other.n_attempts and
            self.n_correct == other.n_correct and
            self.last_shown == other.last_shown
        )

        return result

    def __hash__(self):
        return hash(str(self))

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