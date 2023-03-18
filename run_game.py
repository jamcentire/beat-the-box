from typing import Callable
import random

from strategies import (
    dummy,
    prioritize_extremes,
    prioritize_middle
)

outcomes = []

def execute_game(strat: Callable = None) -> bool:
    # 2 = 2 up to 14 = Ace
    deck = list(range(2,15)) * 4
    random.shuffle(deck)

    board = deck[0:9]
    del deck[0:9]

    while len(deck) > 0:
        #print("-------------------------- NEW ROUND ---------------------------------------------")
        #print("CARDS REMAINING:", len(deck))
        #print("BOARD STATE:", board)

        # If all piles are flipped, we lose
        if len(board) == 0:
            #print("YOU LOSE")
            return False

        board_posn, eval_guess = strat(board)
        #print(f"GUESS: position {board_posn} with comparator {eval_guess}")

        new_card = deck.pop()
        #print("NEW CARD VAL:", new_card)

        if new_card == board[board_posn]:
            # We never choose "same" - only Higher or Lower. So a "same" result means we automatically lose
            #print("LOL YOU GOT SAMED")
            del board[board_posn]
            continue

        if eval_guess(new_card, board[board_posn]):
            # If we guessed right, replace the card
            #print("Nailed it")
            board[board_posn] = new_card
        else:
            # If we guessed wrong, flip over the pile
            #print("Fuck me")
            del board[board_posn]

    # If we go through the entire deck, we win
    #print("YOU WIN!!!")
    return True

num_runs = 10000

for i in range(0,num_runs):
    outcomes.append(execute_game(strat=prioritize_middle))

wins = outcomes.count(True)
win_pcg = 100 * wins / num_runs
losses = outcomes.count(False)
loss_pcg = 100 * losses / num_runs

print(f"Wins: {wins} ({win_pcg}%)")
print(f"Losses: {losses} ({loss_pcg}%)")
