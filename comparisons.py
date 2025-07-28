import time
from problems import TicTacToeState
from algorithms import RandomAgent, MinimaxAgent

def tictactoe_eval(state): return 0 if state.get_winner() is None else 1000 * state.get_winner()

def play_game(initial_state, agent1, agent2):
    state = initial_state
    agents = {1: agent1, -1: agent2}
    while not state.is_terminal():
        move = agents[state.player].select_move(state)
        if move is None: break
        state = state.apply_move(move)
    return state.get_winner()

if __name__ == "__main__":
    agent1 = MinimaxAgent(max_depth=2, eval_fn=tictactoe_eval)
    agent2 = RandomAgent()

    wins, losses, draws = 0, 0, 0
    for _ in range(10):  # run 10 games
        result = play_game(TicTacToeState(), agent1, agent2)
        if result == 1: wins += 1
        elif result == -1: losses += 1
        else: draws += 1

    print(f"Results over 10 games: Wins={wins}, Losses={losses}, Draws={draws}")
