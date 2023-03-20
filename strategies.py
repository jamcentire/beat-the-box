from typing import Callable, List, Tuple
import operator
import random

# We assume that the operator will be applied as op(new_card, card_on_board), and that a
# correct guess will evaluate to True
class Guess:
    HIGHER = operator.gt
    LOWER = operator.lt

class Strategy:
    EXTREMES_FIRST = 'extremes_first'
    MIDDLE_FIRST = 'middle_first'
    RANDOM = 'random'
    DUMMY = 'dummy'

class PlayerBrain:
    CARD_COUNTING = False
    STRATEGY = Strategy.DUMMY
    deck = []

    def __init__(self, card_counting: bool = False, strategy: str = Strategy.DUMMY) -> None:
        self.CARD_COUNTING = card_counting
        self.STRATEGY = strategy
        self.deck = list(range(2,15)) * 4

    # Our card counter sees the card and updates their internal deck model
    def see_card(self, card: int) -> None:
        del self.deck[self.deck.index(card)]

    def _guess_higher_or_lower(self, val: int) -> Callable:
        # If we're counting cards, find the best chance
        if self.CARD_COUNTING:
            lower = [card for card in self.deck if card < val]
            higher = [card for card in self.deck if card > val]
            return Guess.HIGHER if len(higher) > len(lower) else Guess.LOWER

        # Else, we naively guess higher for low value and lower for high values
        if val < 8:
            return Guess.HIGHER
        elif val > 8:
            return Guess.LOWER
        return random.choice([Guess.HIGHER, Guess.LOWER])

    # all strategy functions will take in the board state and return a tuple
    # containing the chosen position, and whether the next card is guessed to be
    # higher or lower
    def make_guess(self, board: List[int]) -> Tuple[int, Callable]:
        if self.STRATEGY == Strategy.EXTREMES_FIRST:
            return self._prioritize_extremes(board)
        elif self.STRATEGY == Strategy.MIDDLE_FIRST:
            return self._prioritize_middle(board)
        elif self.STRATEGY == Strategy.RANDOM:
            return self._random_choice(board)
        elif self.STRATEGY == Strategy.DUMMY:
            return self._dummy(board)

    def _dummy(self, board: List[int]) -> Tuple[int, Callable]:
        """
        A stupid strategy, for testing
        """
        return 0, Guess.HIGHER

    def _prioritize_middle(self, board: List[int]) -> Tuple[int, Callable]:
        """
        Go for the middlemost card values on the table, saving the "good cards" for the end.
        Lauren Lam's strategy.
        8 is the middle value of 2-14, so we use that as our reference
        """
        guess_posn = -1
        guess_pile_value = 0
        min_distance = 7 # Any real card will outperform this

        for posn, value in enumerate(board):
            distance = abs(value - 8)
            # TODO there's probably a cleaner way to do this
            if distance < min_distance:
                guess_posn = posn
                guess_pile_value = value
                min_distance = distance

        return guess_posn, self._guess_higher_or_lower(guess_pile_value)

    def _prioritize_extremes(self, board: List[int]) -> Tuple[int, Callable]:
        """
        Go for the easiest wins first (values furthest from the middle). My proposed strategy.
        8 is the middle value of 2-14, so we use that as our reference
        """
        guess_posn = -1
        guess_pile_value = 0
        max_distance = 0 # Any real card will outperform this

        for posn, value in enumerate(board):
            distance = abs(value - 8)
            # TODO there's probably a cleaner way to do this
            if distance > max_distance:
                guess_posn = posn
                guess_pile_value = value
                max_distance = distance

        return guess_posn, self._guess_higher_or_lower(guess_pile_value)

    def _random_choice(self, board: List[int]) -> Tuple[int, Callable]:
        """
        Every round, choose a random pile to play on.
        """

        guess_posn = random.randrange(len(board))
        return guess_posn, self._guess_higher_or_lower(board[guess_posn])
