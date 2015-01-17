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
        """Constructor.

        Construct a flashcard quiz.

        Args:
            deck (str): Path to deck file.
            hard_weight (int): Favor (with respect to other weights) to give to
                hard flashcards.
            medium_weight (int): Favor (with respect to other weights) to give to
                medium flashcards.
            easy_weight (int): Favor (with respect to other weights) to give to
                easy flashcards.
        """
        self._deck = Deck.load(deck)
        self._decks = Sorted(*self._sort_deck(self._deck))
        self._weights = Sorted(hard_weight, medium_weight, easy_weight)
        self._attempts = 0
        self._correct = 0

    def run(self, card_count, quiz_type, selections=None):
        """Run quiz.

        Generator of questions based on cards in the deck.

        Args:
            card_count (int): Number of questions in run.
            quiz_type (QuizType): Quiz type.
            selections (int): Maximum number of selections if multiple choice.

        Yields:
            (Question):
        """
        def multiple_choice_answers():
            """Multiple choice answers.

            Generate correct answer and multiple choice answers to choose from.

            Returns:
                correct, answer_set (int, str): correct answer and answer set.
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
            """Submit answer to question.

            Answers to multiple choice question must be an integer corresponding
            to the list index of the selection. Answers to fill-in-the-blank
            questions are strings.

            Args:
                answer (int or str):

            Returns:
                result, correct_answer (boolean, str): Answer was correct
                    indicator (True -> Answer was correct. False -> Answer was
                    incorrect.), and the correct answer.

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
        """Quiz score.

        Returns:
            correct, attempts (int, int): Number questions answered correctly,
                and number of questions attempted.
        """
        return self._correct, self._attempts

    def _deck_runner(self, n_cards):
        """Compose a deck to quiz with, and iterate.

        Args:
            n_cards (int): number of cards to run through.

        Yields:
            card (Flashcard): card from the deck.
        """
        # Combine cards into quiz deck based on queue weights.
        deck = [
            c
            for _, c in itertools.takewhile(
                lambda x: x[0] < n_cards,
                enumerate(self._card_generator())
            )
        ]
        random.shuffle(deck)

        # Iterate.
        for card in deck:
            yield card

    def _card_generator(self):
        """Card generator.

        Selects cards from the deck based on the card weights (hard, medium and
        easy). Shuffles them, then deals them.

        Yields:
            card (Flashcard): card from the deck.
        """
        def get_card(idx, deck):
            """Get a card from the specified deck.

            Return the specified card from the passed in deck. If the last card
            from the deck has been gotten, shuffle the deck and start over.

            Args:
                idx (int): index of card to return.
                deck (list): flashcards in the deck.

            Returns:
                c, idx (Flashcard, int): The next card, and the index to get
                    from next time.
            """
            if idx == 0:
                random.shuffle(deck)

            c = deck[idx]
            idx += 1
            if idx >= len(deck):
                idx = 0

            return c, idx

        # Make copies to play with.
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
        """Sort the deck into hard, medium, and easy cards.

        Args:
            deck (Deck): deck to sort

        Returns:
            hard, medium, easy (list, list, list): Cards sorted into three
                sets.
        """
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
        """Is card of hard difficulty?

        Args:
            card (Flashcard): card to classify.

        Returns:
            (boolean): True -> Hard. False -> Not hard.
        """
        return False

    @staticmethod
    def _is_medium(card):
        """Is card of medium difficulty?

        Args:
            card (Flashcard): card to classify.

        Returns:
            (boolean): True -> Medium. False -> Not medium.
        """
        return False

