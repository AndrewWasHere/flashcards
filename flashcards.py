"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
import argparse
import csv
import logging
import os
import itertools
from lib.deck import Deck
from lib.flashcard import Flashcard
from lib.quiz import QuizTypes, Quiz

_logger = logging.getLogger(__name__)


def natural_number(string):
    """
    Determines if string is a natural number.

    :param string:
    :return:
    """
    try:
        val = int(string)
        if val < 0:
            raise ValueError

    except ValueError:
        raise argparse.ArgumentTypeError(
            '{} is not a natural number.'.format(string)
        )

    return val


def parse_command_line():
    """
    Parse arguments from the command line.

    :return args:
    """
    def setup_create_parser():
        cp = subparsers.add_parser('create', help='Create a new deck.')
        cp.add_argument(
            'deck',
            type=str,
            help='Filename of flashcard deck.'
        )
        cp.set_defaults(func=create)

    def setup_swap_parser():
        cp = subparsers.add_parser(
            'swap',
            help='Create a new deck by swapping questions and answers.'
        )
        cp.add_argument(
            'deck',
            type=str,
            help='Filename of source flashcard deck.'
        )
        cp.add_argument(
            'dest',
            type=str,
            help='Filename of destination flashcard deck.'
        )
        cp.set_defaults(func=swap)

    def setup_quiz_parser():
        qp = subparsers.add_parser('quiz', help='Run a quiz.')
        qp.add_argument(
            'deck',
            type=str,
            help='Filename of flashcard deck.'
        )

        # Card use settings.
        qp.add_argument(
            '--all',
            dest='cards',
            action='store_const',
            const='all',
            help='Use all flashcards in the quiz.'
        )
        qp.add_argument(
            '-n', '--number',
            dest='cards',
            type=natural_number,
            help='Number of flashcards to use in the quiz.'
        )

        # Game type settings.
        qp.add_argument(
            '-f', '--fill', '--fill-in-the-blank',
            dest='game_type',
            action='store_const',
            const=QuizTypes.fill_in_the_blank
        )
        qp.add_argument(
            '-m', '--multiple', '--multiple-choice',
            dest='game_type',
            action='store_const',
            const=QuizTypes.multiple_choice
        )
        qp.add_argument(
            '--selections',
            type=natural_number,
            default=4,
            help='Number of multiple choice answers to offer.'
        )

        qp.add_argument(
            '--hard',
            type=natural_number,
            default=1,
            help='Hard cards weight.'
        )
        qp.add_argument(
            '--med',
            type=natural_number,
            default=1,
            help='Medium cards weight.'
        )
        qp.add_argument(
            '--easy',
            type=natural_number,
            default=1,
            help='Easy card weight.'
        )

        # Default values.
        qp.set_defaults(
            # Quiz launcher.
            func=quiz,

            # Settings.
            cards=20,
            game_type=QuizTypes.fill_in_the_blank
        )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--log',
        nargs='?',
        help='Name of log file.'
    )
    parser.add_argument(
        '-v',
        dest='verbosity',
        action='count',
        default=0,
        help='Verbosity of logging.'
    )
    subparsers = parser.add_subparsers()

    setup_create_parser()
    setup_quiz_parser()
    setup_swap_parser()

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        exit()

    if hasattr(args, 'deck'):
        args.deck = os.path.abspath(os.path.expanduser(args.deck))

    if hasattr(args, 'dest'):
        args.dest = os.path.abspath(os.path.expanduser(args.dest))

    return args


def setup_logging(logfile, level):
    """Set up logging.

    Args:
        logfile (str): Path to log file.
        level (int): Log level. Higher is more detailed.
    """
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = levels[min(len(levels) - 1, level)]
    logging.basicConfig(filename=logfile, level=log_level)


def create(args):
    """Create a new flashcard deck.

    Args:
        args (argparse.Namespace): command line arguments.
    """
    _logger.info('Creating deck {}.'.format(args.deck))

    if os.path.exists(args.deck):
        raise ValueError('{} already exists.'.format(args.deck))

    name = input('Deck Name: ')
    deck = Deck(name)
    print('Enter an empty question to finish.')
    for idx in itertools.count(1):
        q = input('Question #{}: '.format(idx))
        if not q:
            break

        a = input('Answer #{}: '.format(idx))
        deck.add_card(Flashcard(q, a))

    deck.save(args.deck)


def swap(args):
    """Swap-create a new flashcard deck.

    Create a new flashcard deck by swapping questions and answers.

    Args:
        args (argparse.Namespace): command line arguments.
    """
    print(
        'Swapping questions and answers from {} and saving to {}.'.format(
            args.deck,
            args.dest
        )
    )
    src = Deck.load(args.deck)
    dest = Deck(src.name)
    for c in src:
        dest.add_card(Flashcard(c.answer, c.question))

    dest.save(args.dest)


def quiz(args):
    """Quiz the user with flashcard deck.

    Args:
        args (argparse.Namespace): command line arguments.
    """
    def fill_in_the_blank_question():
        print('{idx}) {question}'.format(idx=idx, question=q.question))
        ans = input('==> ')
        while ans == '':
            ans = input('==> ')
        return ans

    def multiple_choice_question():
        print('{idx}) {question}'.format(idx=idx, question=q.question))
        answer_set = []
        for i, choice in enumerate(q.answers):
            sel = chr(ord('a') + i)
            answer_set.append(sel)
            print(
                '  {letter}) {choice}'.format(
                    letter=sel,
                    choice=choice
                )
            )

        ans = input('==> ')
        while ans not in answer_set:
            ans = input('==> ')

        ans = ord(ans) - ord('a')
        return ans

    _logger.info('Quizzing with deck {}'.format(args.deck))

    playing = True
    while playing:
        # Build quiz.
        the_quiz = Quiz(args.deck, args.hard, args.med, args.easy)
        quiz_name = the_quiz.name()

        # Play quiz.
        print(quiz_name)
        print('=' * len(quiz_name))

        for idx, q in enumerate(
            the_quiz.run(args.cards, args.game_type, args.selections),
            1
        ):
            answer = (
                fill_in_the_blank_question()
                if args.game_type == QuizTypes.fill_in_the_blank else
                multiple_choice_question()
            )
            result, correct_answer = q.submit(answer)
            print(
                '{affirmation}. The answer is {answer}'.format(
                    affirmation='Correct' if result else 'Incorrect',
                    answer=(
                        correct_answer
                        if args.game_type == QuizTypes.fill_in_the_blank else
                        q.answers[correct_answer]
                    )
                )
            )

        # End of quiz.
        correct, attempts = the_quiz.score()
        print(
            'You got {correct} out of {total} correct.'.format(
                correct=correct,
                total=attempts
            )
        )
        playing = input('Play again (y/n)? ').lower().startswith('y')


def main():
    args = parse_command_line()
    setup_logging(args.log, args.verbosity)
    _logger.info(args)
    args.func(args)

if __name__ == '__main__':
    main()