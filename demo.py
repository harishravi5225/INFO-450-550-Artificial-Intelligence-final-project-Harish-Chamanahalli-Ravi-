from problems import TicTacToeState
from algorithms import MinimaxAgent

def demo_game():
    state = TicTacToeState()
    agent = MinimaxAgent(depth=2)

    while not state.is_terminal():
        state.display()
        if state.current_player == 'X':
            move = agent.select_move(state)
        else:
            move = int(input("Enter your move (0-8): "))
        state = state.apply_move(move)

    state.display()
    winner = state.get_winner()
    if winner:
        print("Winner:", winner)
    else:
        print("Draw.")

if __name__ == "__main__":
    demo_game()
