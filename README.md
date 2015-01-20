# Flashcards
A card-based quiz written in Python.

## Requirements
* Python 3.2 or greater.

For unittests:

* Mock (https://pypi.python.org/pypi/mock) (Python 3.2 only).

## Design
The flashcards application follows the MVC design pattern. User interaction
is separated from the implementation so that the application can be easily
ported between systems without a complete rewrite.

So, for instance, a gtk front end could be written with a Quiz mixin to present
the user with a GUI interface instead of the text-based one that flashcards.py
presents. Or the Quiz class could be wrapped inside a web API to create a 
client-server-based interface.

Flashcards.py is the application, presenting card questions and answers, and
translating user input for the Quiz class.

The Quiz class contains the 'smarts' of the game. It separates the cards into
hard, medium, and easy questions based on the previous scores of the deck.

The Deck class is responsible for holding and serving up Flashcards.

The Flashcard class contains the question, answer, and statistics on how that
question was answered and when.

## Deck File Format
Deck files are csv files with some format requirements, so they can be created
in your favorite spreadsheet software.

The deck files are divided into two sections: The deck description section, and
the quiz section.

### Deck Description Section
The deck description section is composed of keyword-value pairs in the first
cell of the row. The keyword is followed by a colon, then the value.
The special keywords are:

* Name -- The name of the deck, e.g. Single Digit Addition
* Quiz -- Specifies the beginning of the quiz section.

### Quiz Section
The quiz section begins with a header row describing the values in the row.
It is defined to be 'Question, Answer, Attempts, Correct, Last Shown'.

Following the header row are rows containing the card data -- one row for each
card.

The 'Question' value is the question statement.

The 'Answer value is the corresponding correct answer (case insensitive).

The 'Attempts' value is the number of times the question has been attempted.
This can be left blank if you are creating decks in a spreadsheet.

The 'Correct' value is the number of times the question has been answered
correctly. This can be left blank if you are creating decks in a spreadsheet.

The 'Last Shown' value is the ISO-format date-time string of the UTC time of
the last time this question has been attempted. This ca be left blank if you
are creating decks in a spreadsheet.

### Sample Deck File
Name: Sample Deck
Quiz:
Question,Answer,Attempts,Correct,Last Shown
1 + 1, 2
1 + 2, 3
1 + 3, 4
1 + 4, 5
1 + 5, 6
1 + 6, 7
1 + 7, 8
1 + 8, 9
1 + 9, 10

## License
This work is licensed under a Creative Commons
Attribute-NonCommercial-ShareAlike 4.0 International License.
[http://creativecommons.org/licenses/by-nc-sa/4.0/]
(http://creativecommons.org/licenses/by-nc-sa/4.0/)