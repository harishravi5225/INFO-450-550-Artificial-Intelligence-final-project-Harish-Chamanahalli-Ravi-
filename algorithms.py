import random
import math

class MinimaxAgent:
    def __init__(self, depth=3):
        self.depth = depth

    def minimax(self, state, depth, maximizing):
        if state.is_terminal() or depth == 0:
            return state.evaluate(), None

        best_move = None

        if maximizing:
            max_eval = -math.inf
            for move in state.get_legal_moves():
                eval, _ = self.minimax(state.apply_move(move), depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in state.get_legal_moves():
                eval, _ = self.minimax(state.apply_move(move), depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def select_move(self, state):
        _, move = self.minimax(state, self.depth, True)
        return move

class MCTSAgent:
    def __init__(self, simulations=100):
        self.simulations = simulations

    def select_move(self, state):
        legal_moves = state.get_legal_moves()
        move_wins = {move: 0 for move in legal_moves}

        for move in legal_moves:
            for _ in range(self.simulations):
                sim_state = state.apply_move(move)
                winner = self.simulate_random(sim_state)
                if winner == state.current_player:
                    move_wins[move] += 1

        best_move = max(move_wins, key=move_wins.get)
        return best_move

    def simulate_random(self, state):
        while not state.is_terminal():
            move = random.choice(state.get_legal_moves())
            state = state.apply_move(move)
        return state.get_winner()
