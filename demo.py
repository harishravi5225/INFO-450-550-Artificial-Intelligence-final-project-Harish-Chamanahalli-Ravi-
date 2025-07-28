import sys
from problems import TicTacToeState, ReversiState, CheckersState
from algorithms import RandomAgent, MinimaxAgent

def tictactoe_eval(state): return 0 if state.get_winner() is None else 1000 * state.get_winner()
def simple_eval(state): return 0  # placeholder

if __name__ == "__main__":
    game = sys.argv[1] if len(sys.argv) > 1 else "tictactoe"
    if game == "tictactoe": state, eval_fn = TicTacToeState(), tictactoe_eval
    elif game == "reversi": state, eval_fn = ReversiState(), simple_eval
    elif game == "checkers": state, eval_fn = CheckersState(), simple_eval
    else: raise ValueError("Unknown game")

    agent1 = MinimaxAgent(max_depth=2, eval_fn=eval_fn)
    agent2 = RandomAgent()
    agents = {1: agent1, -1: agent2}

    while not state.is_terminal():
        state.print_board()
        agent = agents[state.player]
        move = agent.select_move(state)
        if move is None: break
        state = state.apply_move(move)

    state.print_board()
    print("Winner:", state.get_winner())
