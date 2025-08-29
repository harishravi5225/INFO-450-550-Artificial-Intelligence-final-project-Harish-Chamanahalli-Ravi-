import numpy as np
import random

# -------------------
# Tic Tac Toe
# -------------------

class TicTacToeState:
    def __init__(self, board=None, player=1):
        if board is None:
            self.board = np.zeros((3,3), dtype=int)
        else:
            self.board = board
        self.player = player

    def get_legal_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def apply_move(self, move):
        i, j = move
        new_board = self.board.copy()
        new_board[i, j] = self.player
        return TicTacToeState(new_board, -self.player)

    def is_terminal(self):
        if self.get_winner() is not None:
            return True
        return len(self.get_legal_moves()) == 0

    def get_winner(self):
        for i in range(3):
            if abs(sum(self.board[i, :])) == 3:
                return np.sign(sum(self.board[i, :]))
            if abs(sum(self.board[:, i])) == 3:
                return np.sign(sum(self.board[:, i]))
        diag1 = sum(self.board[i, i] for i in range(3))
        if abs(diag1) == 3:
            return np.sign(diag1)
        diag2 = sum(self.board[i, 2 - i] for i in range(3))
        if abs(diag2) == 3:
            return np.sign(diag2)
        return None

    def print_board(self):
        symbols = {1: "X", -1: "O", 0: "."}
        for row in self.board:
            print(" ".join(symbols[x] for x in row))
        print()

# --- Evaluation Functions for Tic Tac Toe ---

def ttt_simple_count_heuristic(state, player):
    return np.sum(state.board == player) - np.sum(state.board == -player)

def ttt_line_control_heuristic(state, player):
    score = 0
    for i in range(3):
        row = state.board[i, :]
        col = state.board[:, i]
        score += line_score(row, player)
        score += line_score(col, player)
    diag1 = [state.board[i, i] for i in range(3)]
    diag2 = [state.board[i, 2 - i] for i in range(3)]
    score += line_score(diag1, player)
    score += line_score(diag2, player)
    return score

def line_score(line, player):
    if -player not in line:
        return list(line).count(player)
    return 0

# -------------------
# Checkers
# -------------------

class CheckersState:
    def __init__(self, board=None, player=1):
        if board is None:
            self.board = self.initial_board()
        else:
            self.board = board
        self.player = player

    def initial_board(self):
        b = np.zeros((8,8), dtype=int)
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    b[i, j] = -1
        for i in range(5,8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    b[i, j] = 1
        return b

    def get_legal_moves(self):
        moves = []
        dirs = [(-1, -1), (-1, 1)] if self.player == 1 else [(1, -1), (1, 1)]
        for i in range(8):
            for j in range(8):
                if self.board[i,j] == self.player:
                    for di,dj in dirs:
                        ni,nj = i+di,j+dj
                        if 0 <= ni <8 and 0 <= nj <8 and self.board[ni,nj]==0:
                            moves.append(((i,j),(ni,nj)))
                        ni2,nj2 = i+2*di,j+2*dj
                        if 0 <= ni2 <8 and 0 <= nj2 <8:
                            if self.board[ni,nj]==-self.player and self.board[ni2,nj2]==0:
                                moves.append(((i,j),(ni2,nj2)))
        return moves

    def apply_move(self, move):
        (i1,j1),(i2,j2)=move
        new_board = self.board.copy()
        new_board[i2,j2]=new_board[i1,j1]
        new_board[i1,j1]=0
        if abs(i2 - i1)==2:
            mi, mj = (i1 + i2)//2, (j1 + j2)//2
            new_board[mi,mj]=0
        return CheckersState(new_board,-self.player)

    def is_terminal(self):
        return len(self.get_legal_moves())==0

    def get_winner(self):
        if self.is_terminal():
            return -self.player
        return None

    def print_board(self):
        symbols={1:"r",-1:"b",0:"."}
        for row in self.board:
            print(" ".join(symbols[x] for x in row))
        print()
    def count_pieces(self):
        white = black = white_kings = black_kings = 0
        for row in self.board:
            for piece in row:
                if piece == 1:
                    white += 1
                elif piece == -1:
                    black += 1
                elif piece == 2:
                    white_kings += 1
                elif piece == -2:
                    black_kings += 1
        return white, black, white_kings, black_kings

# --- Evaluation Functions for Checkers ---

def checkers_simple_heuristic(state, player):
    return np.sum(state.board == player) - np.sum(state.board == -player)

def checkers_positional_heuristic(state, player):
    score = 0
    for i in range(8):
        for j in range(8):
            if state.board[i, j] == player:
                score += 5
                if 2 <= i <= 5 and 2 <= j <= 5:
                    score += 3
            elif state.board[i, j] == -player:
                score -= 5
                if 2 <= i <= 5 and 2 <= j <= 5:
                    score -= 3
    return score

# -------------------
# Reversi
# -------------------

class ReversiState:

    def __init__(self, board=None, player=1):
        if board is None:
            self.board = self.initial_board()
        else:
            self.board = board
        self.player = player

    def initial_board(self):
        b = np.zeros((8, 8), dtype=int)
        b[3, 3] = b[4, 4] = -1
        b[3, 4] = b[4, 3] = 1
        return b

    def get_legal_moves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i, j] == 0 and self.has_flippable(i, j):
                    moves.append((i, j))
        return moves

    def has_flippable(self, i, j):
        return len(self.flipped_discs(i, j)) > 0

    def flipped_discs(self, i, j):
        flips = []
        dirs = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)]
        for dx, dy in dirs:
            temp = []
            x, y = i + dx, j + dy
            while 0 <= x < 8 and 0 <= y < 8:
                if self.board[x, y] == -self.player:
                    temp.append((x, y))
                elif self.board[x, y] == self.player:
                    flips.extend(temp)
                    break
                else:
                    break
                x += dx
                y += dy
        return flips

    def apply_move(self, move):
        i, j = move
        new_board = self.board.copy()
        new_board[i, j] = self.player
        for x, y in self.flipped_discs(i, j):
            new_board[x, y] = self.player
        return ReversiState(new_board, -self.player)

    def is_terminal(self):
        return len(self.get_legal_moves()) == 0 and \
               len(ReversiState(self.board, -self.player).get_legal_moves()) == 0

    def get_winner(self):
        if not self.is_terminal():
            return None
        count = np.sum(self.board)
        if count > 0:
            return 1
        elif count < 0:
            return -1
        else:
            return 0

    def count_discs(self):
        white = 0
        black = 0
        for row in self.board:
            for cell in row:
                if cell == 1:
                    white += 1
                elif cell == -1:
                    black += 1
        return white, black

    def print_board(self):
        symbols = {1: "X", -1: "O", 0: "."}
        for row in self.board:
            print(" ".join(symbols[x] for x in row))
        print()

# --- Evaluation Functions for Reversi ---

def reversi_simple_count(state, player):
    return np.sum(state.board == player) - np.sum(state.board == -player)

def reversi_corner_mobility_heuristic(state, player):
    score = reversi_simple_count(state, player)
    corners = [(0,0), (0,7), (7,0), (7,7)]
    for i, j in corners:
        if state.board[i,j] == player:
            score += 10
        elif state.board[i,j] == -player:
            score -= 10
    score += len(state.get_legal_moves())
    return score
# ---------------------------------------------
# TICTACTOE Heuristics
# ---------------------------------------------
def tictactoe_simple_heuristic(state, player):
    # Simple: +1 for win, -1 for loss, 0 otherwise
    winner = state.get_winner()
    if winner == player:
        return 1
    elif winner == -player:
        return -1
    else:
        return 0

def tictactoe_refined_heuristic(state, player):
    # Refined: Count center and corners control + simple outcome
    winner = state.get_winner()
    if winner == player:
        return 10
    elif winner == -player:
        return -10

    board = state.board
    score = 0
    opponent = -player

    # Center control
    if board[1][1] == player:
        score += 2
    elif board[1][1] == opponent:
        score -= 2

    # Corner control
    corners = [(0,0), (0,2), (2,0), (2,2)]
    for i, j in corners:
        if board[i][j] == player:
            score += 1
        elif board[i][j] == opponent:
            score -= 1

    return score

# ---------------------------------------------
# CHECKERS Heuristics
# ---------------------------------------------
def checkers_simple_heuristic(state, player):
    white, black, white_kings, black_kings = state.count_pieces()
    if player == 1:
        return white + 1.5 * white_kings - black - 1.5 * black_kings
    else:
        return black + 1.5 * black_kings - white - 1.5 * white_kings

def checkers_refined_heuristic(state, player):
    white, black, white_kings, black_kings = state.count_pieces()
    if player == 1:
        material = white + 2 * white_kings - black - 2 * black_kings
    else:
        material = black + 2 * black_kings - white - 2 * white_kings

    mobility = len(state.get_legal_moves())
    return material + 0.1 * mobility

# ---------------------------------------------
# REVERSI Heuristics
# ---------------------------------------------
def reversi_simple_heuristic(state, player):
    white, black = state.count_discs()
    return white - black if player == 1 else black - white

def reversi_refined_heuristic(state, player):
    white, black = state.count_discs()
    if player == 1:
        disc_diff = white - black
    else:
        disc_diff = black - white

    corners = [(0,0), (0,7), (7,0), (7,7)]
    board = state.board
    corner_score = 0
    for i, j in corners:
        if board[i][j] == player:
            corner_score += 5
        elif board[i][j] == -player:
            corner_score -= 5

    mobility = len(state.get_legal_moves())
    return disc_diff + corner_score + 0.1 * mobility

