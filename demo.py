import sys
import numpy as np
from problems import TicTacToeState, CheckersState, ReversiState
from algorithms import MinimaxAgent, RandomAgent

# -----------------------------
# Evaluation Functions
# -----------------------------

def tictactoe_eval(state, player):
    winner = state.get_winner()
    if winner == player:
        return 1000
    elif winner == -player:
        return -1000
    return 0  # Neutral evaluation

def checkers_eval(state, player):
    white, black, white_kings, black_kings = state.count_pieces()
    if player == 1:
        return white + 2 * white_kings - (black + 2 * black_kings)
    else:
        return black + 2 * black_kings - (white + 2 * white_kings)

def reversi_eval(state, player):
    white, black = state.count_discs()
    return white - black if player == 1 else black - white

# -----------------------------
# Main Loop
# -----------------------------

if __name__ == "__main__":
    game = sys.argv[1] if len(sys.argv) > 1 else "tictactoe"

    if game == "tictactoe":
        state = TicTacToeState(player=1)
        eval_fn = tictactoe_eval
    elif game == "checkers":
        state = CheckersState(player=1)
        eval_fn = checkers_eval
    elif game == "reversi":
        state = ReversiState(player=1)
        eval_fn = reversi_eval
    else:
        raise ValueError("Unknown game: choose from 'tictactoe', 'checkers', or 'reversi'")

    minimax_agent = MinimaxAgent(max_depth=3, eval_fn=eval_fn, use_move_ordering=True)
    random_agent = RandomAgent()
    agents = {1: minimax_agent, -1: random_agent}

    while not state.is_terminal():
        state.print_board()
        agent = agents[state.player]
        move = agent.select_move(state)
        if move is None:
            break
        state = state.apply_move(move)

    state.print_board()
    winner = state.get_winner()
    print("Winner:", winner)
