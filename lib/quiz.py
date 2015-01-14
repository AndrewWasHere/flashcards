"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
from collections import namedtuple
import random
import itertools
from lib.data_types import Const
from lib.deck import Deck


class QuizTypes(Const):
    """
    Quiz types.
    """
    fill_in_the_blank = 'fill in the blank'
    multiple_choice = 'multiple choice'


Question = namedtuple('Question', ['question', 'answers', 'submit_fn'])
Sorted = namedtuple('Sorted', ['hard', 'medium', 'easy'])


class Quiz:
    """
    Flashcard quiz model.
    """
    def __init__(self, deck, hard_weight=1, medium_weight=1, easy_weight=1):
        """
        Construct a Quiz.

        :param deck: Path to deck file.
        :param hard_weight:
        :param medium_weight:
        :param easy_weight:
        :return:
        """
        self._deck = Deck.load(deck)
        self._decks = Sorted(*self._sort_deck(self._deck))
        self._weights = Sorted(hard_weight, medium_weight, easy_weight)
        self._attempts = 0
        self._correct = 0

    def run(self, card_count, quiz_type, selections=None):
        """
        Generator of questions based on cards in the deck.

        :param card_count: Number of questions in run.
        :param quiz_type: QuizType.
        :param selections: Maximum number of selections if multiple choice.
        :yields Question:
        """
        def multiple_choice_answers():
            """
            Generate correct answer and multiple choice answers to choose from.
            :return:
            """
            remaining_answers = (
                a
                for a in (all_answers - frozenset([card.answer]))
            )
            answer_set = (
                [card.answer] +
                random.sample(remaining_answers, selections - 1)
            )
            random.shuffle(answer_set)
            correct = answer_set.index(card.answer)
            return correct, answer_set

        def submit(answer):
            """
            Submit answer to question.

            Answers to multiple choice question must be an integer corresponding
            to the list index of the selection. Answers to fill-in-the-blank
            questions are strings.

            :param answer:
            :return result, correct_answer: boolean, str.
                True -> Correct answer.
                False -> Incorrect answer.
            """
            if answer == correct_answer:
                card.correct()
                self._correct += 1
                result = True

            else:
                card.incorrect()
                result = False

            self._attempts += 1
            return result, correct_answer

        # Execution starts here. ###############################################

        self._correct = self._attempts = 0

        if card_count == 'all':
            card_count = len(self._deck)

        all_answers = (
            self._deck.answers()
            if quiz_type == QuizTypes.multiple_choice else
            None
        )

        for card in self._deck_runner(card_count):
            question = card.question
            correct_answer, answers = (
                (card.answer, None)
                if quiz_type == QuizTypes.fill_in_the_blank else
                multiple_choice_answers()
            )

            yield Question(question, answers, submit)

    def score(self):
        """
        Returns quiz score.

        :return correct, attempts:
        """
        return self._correct, self._attempts

    def _deck_runner(self, cards):
        """
        Compose a deck to quiz with, and iterate.
        """
        # Combine cards into quiz deck based on queue weights.
        deck = [
            c
            for _, c in itertools.takewhile(
                lambda x: x[0] < cards,
                enumerate(self._card_generator())
            )
        ]
        random.shuffle(deck)

        # Iterate.
        for card in deck:
            yield card

    def _card_generator(self):
        def get_card(idx, deck):
            if idx == 0:
                random.shuffle(deck)

            c = deck[idx]
            idx += 1
            if idx >= len(deck):
                idx = 0

            return c, idx

        hard_deck = self._decks.hard[:]
        medium_deck = self._decks.medium[:]
        easy_deck = self._decks.easy[:]
        hard_idx = medium_idx = easy_idx = 0

        while True:
            if len(hard_deck) > 0:
                for _ in range(self._weights.hard):
                    card, hard_idx = get_card(hard_idx, hard_deck)
                    yield card

            if len(medium_deck) > 0:
                for _ in range(self._weights.medium):
                    card, medium_idx = get_card(medium_idx, medium_deck)
                    yield card

            if len(easy_deck) > 0:
                for _ in range(self._weights.easy):
                    card, easy_idx = get_card(easy_idx, easy_deck)
                    yield card

    def _sort_deck(self, deck):
        hard = []
        medium = []
        easy = []
        for c in deck:
            if self._is_hard(c):
                hard.append(c)
            elif self._is_medium(c):
                medium.append(c)
            else:
                easy.append(c)

        return hard, medium, easy

    @staticmethod
    def _is_hard(card):
        return False

    @staticmethod
    def _is_medium(card):
        return False

