from typing import Callable, List
import random

from strategies import (
    PlayerBrain,
    Strategy
)

outcomes = []
guesses = []


def execute_game(strat: str = Strategy.DUMMY, card_counting: bool = False) -> bool:
    # 2 = 2 up to 14 = Ace
    deck = list(range(2,15)) * 4
    random.shuffle(deck)
    player = PlayerBrain(card_counting, strat)

    board = deck[0:9]
    del deck[0:9]

    while len(deck) > 0:
        # If all piles are flipped, we lose
        if len(board) == 0:
            return False

        # Use our strategy to choose a pile and guess higher or lower
        board_posn, eval_guess = player.make_guess(board)
        new_card = deck.pop()
        player.see_card(new_card)

        if new_card == board[board_posn]:
            # We never choose "same" - only Higher or Lower. So a "same" result means we automatically lose
            del board[board_posn]
            guesses.append(False)
            continue

        if eval_guess(new_card, board[board_posn]):
            # If correct, replace top card of pile with new card
            board[board_posn] = new_card
            guesses.append(True)
        else:
            # If incorrect, flip over pile
            del board[board_posn]
            guesses.append(False)

    # If we go through the entire deck, we win
    return True

num_runs = 10000

for i in range(0,num_runs):
    outcomes.append(execute_game(strat=Strategy.RANDOM, card_counting=True))

wins = outcomes.count(True)
win_pcg = 100 * wins / num_runs
losses = outcomes.count(False)
loss_pcg = 100 * losses / num_runs
guess_pcg = 100 * guesses.count(True) / len(guesses)

print(f"Wins: {wins} ({win_pcg}%)")
print(f"Losses: {losses} ({loss_pcg}%)")
print(f"Guesses: {guess_pcg}% correct")
