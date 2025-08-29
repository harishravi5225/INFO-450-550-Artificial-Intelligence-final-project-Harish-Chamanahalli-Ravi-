import sys
import time
from problems import (
    TicTacToeState,
    CheckersState,
    ReversiState,
    tictactoe_simple_heuristic,
    tictactoe_refined_heuristic,
    checkers_simple_heuristic,
    checkers_refined_heuristic,
    reversi_simple_heuristic,
    reversi_refined_heuristic,
)
from algorithms import MinimaxAgent, MCTSAgent, RandomAgent

# Available game classes
GAMES = {
    "tictactoe": TicTacToeState,
    "checkers": CheckersState,
    "reversi": ReversiState,
}

# Heuristic functions for Minimax agents
HEURISTICS = {
    "tictactoe": {
        "simple": tictactoe_simple_heuristic,
        "refined": tictactoe_refined_heuristic,
    },
    "checkers": {
        "simple": checkers_simple_heuristic,
        "refined": checkers_refined_heuristic,
    },
    "reversi": {
        "simple": reversi_simple_heuristic,
        "refined": reversi_refined_heuristic,
    },
}

# Agent factory
def get_agent(agent_name, game_name):
    if agent_name == "random":
        return RandomAgent()
    elif agent_name == "mcts":
        return MCTSAgent(num_simulations=100)
    elif agent_name in HEURISTICS[game_name]:
        return MinimaxAgent(max_depth=3, eval_fn=HEURISTICS[game_name][agent_name])
    else:
        raise ValueError(f"Unknown agent: {agent_name}")

# Main function to run experiments
def run_games(game_name, agent1_name, agent2_name, num_games):
    GameClass = GAMES[game_name]
    agent1 = get_agent(agent1_name, game_name)
    agent2 = get_agent(agent2_name, game_name)
    agents = {1: agent1, -1: agent2}

    wins = {1: 0, -1: 0, 0: 0}
    total_moves = 0
    total_time = 0.0

    for i in range(num_games):
        state = GameClass(player=1)
        move_count = 0
        start_time = time.perf_counter()

        while not state.is_terminal():
            agent = agents[state.player]
            move = agent.select_move(state)
            if move is None:
                break
            state = state.apply_move(move)
            move_count += 1

        end_time = time.perf_counter()
        game_time = end_time - start_time
        total_time += game_time
        total_moves += move_count

        winner = state.get_winner()
        wins[winner] += 1
        print(f"Game {i+1}: Winner = {winner}, Moves = {move_count}, Time = {game_time:.2f}s")

    print("\nResults after", num_games, "games:")
    print(f"{agent1_name} wins: {wins[1]}")
    print(f"{agent2_name} wins: {wins[-1]}")
    print(f"Draws: {wins[0]}")
    print(f"Average moves per game: {total_moves / num_games:.2f}")
    print(f"Average time per move: {total_time / total_moves:.4f} seconds")

# Command-line usage
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python comparisons.py [game] [agent1] [agent2] [num_games]")
        print("Example: python comparisons.py checkers simple mcts 20")
        sys.exit(1)

    game_name = sys.argv[1].lower()
    agent1_name = sys.argv[2].lower()
    agent2_name = sys.argv[3].lower()
    num_games = int(sys.argv[4])

    run_games(game_name, agent1_name, agent2_name, num_games)
