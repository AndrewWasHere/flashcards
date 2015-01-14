"""
Copyright 2015, Andrew Lin

This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
import argparse
import logging
from lib.quiz import QuizTypes

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
        cp = subparsers.add_parser('create')
        cp.add_argument(
            'deck',
            type=str,
            help='Filename of flashcard deck.'
        )
        cp.set_defaults(func=create)

    def setup_quiz_parser():
        qp = subparsers.add_parser('quiz')
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

        # Default values.
        qp.set_defaults(
            # Quiz launcher.
            func=quiz,

            # Settings.
            cards=0,
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

    args = parser.parse_args()
    return args


def setup_logging(logfile, level):
    """
    Set up logging.

    :param logfile:
    :param level:
    :return:
    """
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = levels[min(len(levels) - 1, level)]
    logging.basicConfig(filename=logfile, filemode='a', level=log_level)


def create(args):
    """
    Create a new flashcard deck.

    :param args:
    :return:
    """
    _logger.info('Creating deck {}.'.format(args.deck))


def quiz(args):
    """
    Quiz user with flashcard deck.

    :param args:
    :return:
    """
    _logger.info('Quizzing with deck {}'.format(args.deck))


def main():
    args = parse_command_line()
    setup_logging(args.log, args.verbosity)
    _logger.info(args)
    args.func(args)

if __name__ == '__main__':
    main()