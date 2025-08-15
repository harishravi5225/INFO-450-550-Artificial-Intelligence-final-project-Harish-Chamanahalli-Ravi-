import sys
from problems import TicTacToeState, CheckersState, ReversiState
from algorithms import MinimaxAgent, RandomAgent
import numpy as np

def tictactoe_eval(state, player):
    winner = state.get_winner()
    if winner == player:
        return 1000
    elif winner == -player:
        return -1000
    return 0

def checkers_eval(state, player):
    return np.sum(state.board) * player

def reversi_eval(state, player):
    return np.sum(state.board) * player

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
        raise ValueError("Unknown game")

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
