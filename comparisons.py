from problems import TicTacToeState
from algorithms import MinimaxAgent, MCTSAgent

def play_game(agent1, agent2):
    state = TicTacToeState()
    agents = {'X': agent1, 'O': agent2}
    while not state.is_terminal():
        move = agents[state.current_player].select_move(state)
        state = state.apply_move(move)
    return state.get_winner()

def run_experiments(games=10):
    minimax = MinimaxAgent(depth=3)
    mcts = MCTSAgent(simulations=50)
    results = {'X': 0, 'O': 0, 'Draw': 0}

    for i in range(games):
        winner = play_game(minimax, mcts)
        if winner:
            results[winner] += 1
        else:
            results['Draw'] += 1

    print("Results after", games, "games:")
    for k, v in results.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    run_experiments()
