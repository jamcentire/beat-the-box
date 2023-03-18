from typing import Callable, List, Tuple
import operator
import random

# We assume that the operator will be applied as op(guess, board_slot), and that a
# correct guess will evaluate to True
class Guess:
    HIGHER = operator.gt
    LOWER = operator.lt

# We naively guess higher for low value and lower for high values
def _guess_from_value(val: int) -> Callable:
    if val < 8:
        return Guess.HIGHER
    elif val > 8:
        return Guess.LOWER
    return random.choice([Guess.HIGHER, Guess.LOWER])

# all strategy functions will take in the board state and return a tuple
# containing the chosen position, and whether the next card is guessed to be
# higher or lower


def prioritize_middle(board: List[int]) -> Tuple[int, Callable]:
    """
    Go for the middlemost card values on the table, saving the "good cards" for the end.
    Lauren Lam's strategy.
    8 is the middle value of 2-14, so we use that as our reference
    """
    guess_posn = -1
    guess_value = 0
    min_distance = 7 # Any real card will outperform this

    for posn, value in enumerate(board):
        distance = abs(value - 8)
        # TODO there's probably a cleaner way to do this
        if distance < min_distance:
            guess_posn = posn
            guess_value = value
            min_distance = distance

    return guess_posn, _guess_from_value(guess_value)

def prioritize_extremes(board: List[int]) -> Tuple[int, Callable]:
    """
    Go for the easiest wins first (values furthest from the middle). My proposed strategy
    8 is the middle value of 2-14, so we use that as our reference
    """
    guess_posn = -1
    guess_value = 0
    max_distance = 0 # Any real card will outperform this

    for posn, value in enumerate(board):
        distance = abs(value - 8)
        # TODO there's probably a cleaner way to do this
        if distance > max_distance:
            guess_posn = posn
            guess_value = value
            max_distance = distance

    return guess_posn, _guess_from_value(guess_value)

def dummy(board: List[int]) -> Tuple[int, Callable]:
    """
    A stupid strategy, for testing
    """
    return 0, Guess.HIGHER
