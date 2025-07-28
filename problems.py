import numpy as np

# -------- Tic Tac Toe --------
class TicTacToeState:
    def __init__(self, board=None, player=1):
        self.board = np.zeros((3,3), dtype=int) if board is None else board
        self.player = player

    def get_legal_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def apply_move(self, move):
        i, j = move
        new_board = self.board.copy()
        new_board[i, j] = self.player
        return TicTacToeState(new_board, -self.player)

    def is_terminal(self):
        return self.get_winner() is not None or len(self.get_legal_moves()) == 0

    def get_winner(self):
        for i in range(3):
            if abs(sum(self.board[i, :])) == 3: return np.sign(sum(self.board[i, :]))
            if abs(sum(self.board[:, i])) == 3: return np.sign(sum(self.board[:, i]))
        diag1 = sum(self.board[i, i] for i in range(3))
        diag2 = sum(self.board[i, 2 - i] for i in range(3))
        if abs(diag1) == 3: return np.sign(diag1)
        if abs(diag2) == 3: return np.sign(diag2)
        return None

    def print_board(self):
        symbols = {1: "X", -1: "O", 0: "."}
        for row in self.board:
            print(" ".join(symbols[x] for x in row))
        print()

# -------- Reversi (placeholder) --------
class ReversiState:
    def __init__(self, board=None, player=1):
        self.board = np.zeros((8,8), dtype=int) if board is None else board
        if board is None:
            self.board[3,3], self.board[4,4] = -1, -1
            self.board[3,4], self.board[4,3] = 1, 1
        self.player = player

    def get_legal_moves(self):
        return [(i, j) for i in range(8) for j in range(8) if self.board[i, j] == 0]

    def apply_move(self, move):
        i, j = move
        new_board = self.board.copy()
        new_board[i, j] = self.player
        return ReversiState(new_board, -self.player)

    def is_terminal(self):
        return len(self.get_legal_moves()) == 0

    def get_winner(self):
        score = np.sum(self.board)
        return 1 if score > 0 else -1 if score < 0 else 0

    def print_board(self):
        symbols = {1: "X", -1: "O", 0: "."}
        for row in self.board:
            print(" ".join(symbols[x] for x in row))
        print()

# -------- Checkers (placeholder) --------
class CheckersState:
    def __init__(self, board=None, player=1):
        self.board = np.zeros((8,8), dtype=int) if board is None else board
        self.player = player

    def get_legal_moves(self):
        return [(i, j) for i in range(8) for j in range(8) if self.board[i, j] == 0]

    def apply_move(self, move):
        i, j = move
        new_board = self.board.copy()
        new_board[i, j] = self.player
        return CheckersState(new_board, -self.player)

    def is_terminal(self):
        return len(self.get_legal_moves()) == 0

    def get_winner(self):
        score = np.sum(self.board)
        return 1 if score > 0 else -1 if score < 0 else 0

    def print_board(self):
        symbols = {1: "X", -1: "O", 0: "."}
        for row in self.board:
            print(" ".join(symbols[x] for x in row))
        print()
