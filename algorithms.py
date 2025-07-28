import random

class RandomAgent:
    def select_move(self, state):
        moves = state.get_legal_moves()
        return random.choice(moves) if moves else None

class MinimaxAgent:
    def __init__(self, max_depth, eval_fn):
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    def select_move(self, state):
        best_score = -float('inf')
        best_move = None
        for move in state.get_legal_moves():
            score = self.min_value(state.apply_move(move), 1)
            if score > best_score:
                best_score, best_move = score, move
        return best_move

    def max_value(self, state, depth):
        if state.is_terminal() or depth >= self.max_depth:
            return self.eval_fn(state)
        v = -float('inf')
        for move in state.get_legal_moves():
            v = max(v, self.min_value(state.apply_move(move), depth + 1))
        return v

    def min_value(self, state, depth):
        if state.is_terminal() or depth >= self.max_depth:
            return self.eval_fn(state)
        v = float('inf')
        for move in state.get_legal_moves():
            v = min(v, self.max_value(state.apply_move(move), depth + 1))
        return v
