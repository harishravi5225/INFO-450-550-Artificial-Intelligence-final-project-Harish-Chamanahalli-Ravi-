class TicTacToeState:
    def __init__(self, board=None, current_player='X'):
        self.board = board or [' '] * 9
        self.current_player = current_player

    def get_legal_moves(self):
        return [i for i, v in enumerate(self.board) if v == ' ']

    def apply_move(self, move):
        new_board = self.board.copy()
        new_board[move] = self.current_player
        next_player = 'O' if self.current_player == 'X' else 'X'
        return TicTacToeState(new_board, next_player)

    def is_terminal(self):
        return self.get_winner() is not None or ' ' not in self.board

    def get_winner(self):
        lines = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for a,b,c in lines:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]
        return None

    def evaluate(self):
        winner = self.get_winner()
        if winner == 'X':
            return 1
        elif winner == 'O':
            return -1
        return 0

    def display(self):
        for i in range(0, 9, 3):
            print(self.board[i:i+3])
        print()