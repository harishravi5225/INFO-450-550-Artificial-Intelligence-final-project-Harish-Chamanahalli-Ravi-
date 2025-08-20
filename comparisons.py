import sys
import time
import numpy as np
from problems import TicTacToeState, CheckersState, ReversiState
from algorithms import MinimaxAgent, RandomAgent, MCTSAgent

# Evaluation functions
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
    board = state.board
    score = np.sum(board) * player
    corners = [(0,0),(0,7),(7,0),(7,7)]
    for i,j in corners:
        if board[i,j]==player:
            score += 10
        elif board[i,j]==-player:
            score -=10
    return score

def play_game(initial_state, agent1, agent2, verbose=False):
    state = initial_state
    agents = {1: agent1, -1: agent2}
    move_times = {1: [], -1: []}
    num_moves = 0

    while not state.is_terminal():
        current_player = state.player
        agent = agents[current_player]
        start_time = time.time()
        move = agent.select_move(state)
        end_time = time.time()

        if move is None:
            break

        elapsed = end_time - start_time
        move_times[current_player].append(elapsed)

        state = state.apply_move(move)
        num_moves += 1

        if verbose:
            state.print_board()

    winner = state.get_winner()
    return {
        "winner": winner,
        "num_moves": num_moves,
        "avg_time_p1": sum(move_times[1])/len(move_times[1]) if move_times[1] else 0,
        "avg_time_p2": sum(move_times[-1])/len(move_times[-1]) if move_times[-1] else 0
    }

def run_experiments(game, opponent="mcts", num_games=20):
    # Select game and evaluation function
    if game == "tictactoe":
        state_class = TicTacToeState
        eval_fn = tictactoe_eval
    elif game == "checkers":
        state_class = CheckersState
        eval_fn = checkers_eval
    elif game == "reversi":
        state_class = ReversiState
        eval_fn = reversi_eval
    else:
        raise ValueError("Unknown game")

    # Minimax always as Agent1
    agent1 = MinimaxAgent(
        max_depth=3,
        eval_fn=eval_fn,
        use_move_ordering=True
    )

    # Choose opponent agent
    if opponent == "mcts":
        agent2 = MCTSAgent(num_simulations=20)
    elif opponent == "random":
        agent2 = RandomAgent()
    else:
        raise ValueError("Unknown opponent type (must be 'mcts' or 'random')")

    results = []
    for i in range(num_games):
        # Alternate who starts
        if i % 2 == 0:
            state = state_class(player=1)
            res = play_game(state, agent1, agent2)
        else:
            state = state_class(player=-1)
            res = play_game(state, agent2, agent1)
            # Flip winner perspective
            if res["winner"] is not None:
                res["winner"] *= -1
            res["avg_time_p1"], res["avg_time_p2"] = res["avg_time_p2"], res["avg_time_p1"]

        results.append(res)

    # Aggregate results
    wins = sum(1 for r in results if r["winner"] == 1)
    losses = sum(1 for r in results if r["winner"] == -1)
    draws = sum(1 for r in results if r["winner"] == 0 or r["winner"] is None)
    avg_moves = sum(r["num_moves"] for r in results) / num_games
    avg_time_p1 = sum(r["avg_time_p1"] for r in results) / num_games
    avg_time_p2 = sum(r["avg_time_p2"] for r in results) / num_games

    print(f"\n=== Results over {num_games} games ({game} - Minimax vs {opponent}) ===")
    print("Agent1 (Minimax) Wins:", wins)
    print("Agent1 Losses:", losses)
    print("Draws:", draws)
    print("Average moves per game:", avg_moves)
    print("Average time per move (Agent1): {:.4f}s".format(avg_time_p1))
    print("Average time per move (Agent2): {:.4f}s".format(avg_time_p2))

if __name__ == "__main__":
    game = sys.argv[1] if len(sys.argv) > 1 else "tictactoe"
    opponent = sys.argv[2] if len(sys.argv) > 2 else "mcts"
    num_games = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    run_experiments(game=game, opponent=opponent, num_games=num_games)

