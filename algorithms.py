import random

# --------------------------
# Random Agent
# --------------------------

class RandomAgent:
    def select_move(self, state):
        moves = state.get_legal_moves()
        if not moves:
            return None
        return random.choice(moves)

# --------------------------
# Minimax Agent with Alpha-Beta Pruning
# --------------------------

class MinimaxAgent:
    def __init__(self, max_depth, eval_fn, use_move_ordering=False):
        """
        max_depth: int - maximum search depth
        eval_fn: function(state, player) -> float
        use_move_ordering: bool - whether to sort moves by heuristic value
        """
        self.max_depth = max_depth
        self.eval_fn = eval_fn
        self.use_move_ordering = use_move_ordering

    def select_move(self, state):
        best_score = -float('inf')
        best_move = None
        moves = state.get_legal_moves()
        if not moves:
            return None

        if self.use_move_ordering:
            random.shuffle(moves)

        for move in moves:
            child = state.apply_move(move)
            score = self.min_value(child, -float('inf'), float('inf'), 1)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def max_value(self, state, alpha, beta, depth):
        if state.is_terminal() or depth >= self.max_depth:
            return self.eval_fn(state, state.player)
        v = -float('inf')
        moves = state.get_legal_moves()
        if self.use_move_ordering:
            random.shuffle(moves)
        for move in moves:
            child = state.apply_move(move)
            v = max(v, self.min_value(child, alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, depth):
        if state.is_terminal() or depth >= self.max_depth:
            return self.eval_fn(state, state.player)
        v = float('inf')
        moves = state.get_legal_moves()
        if self.use_move_ordering:
            random.shuffle(moves)
        for move in moves:
            child = state.apply_move(move)
            v = min(v, self.max_value(child, alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

# --------------------------
# MCTS Agent (Monte Carlo Tree Search)
# --------------------------

class MCTSAgent:
    def __init__(self, num_simulations=50):
        """
        num_simulations: int - number of random playouts per move
        """
        self.num_simulations = num_simulations

    def select_move(self, state):
        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return None

        move_wins = {move: 0 for move in legal_moves}
        move_plays = {move: 0 for move in legal_moves}

        for move in legal_moves:
            for _ in range(self.num_simulations):
                result = self.simulate(state.apply_move(move))
                move_plays[move] += 1
                if result == state.player:
                    move_wins[move] += 1

        # Choose the move with the highest win rate
        best_move = max(
            legal_moves,
            key=lambda m: move_wins[m] / move_plays[m]
        )
        return best_move

    def simulate(self, state):
        """
        Play a random playout from the current state to terminal.
        Returns:
            winner (1 or -1) or 0/None for draw
        """
        current_state = state
        while not current_state.is_terminal():
            legal = current_state.get_legal_moves()
            if not legal:
                break
            move = random.choice(legal)
            current_state = current_state.apply_move(move)
        return current_state.get_winner()


