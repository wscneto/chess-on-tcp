import chess

class GameState:
    def __init__(self):
        self.board = chess.Board()
        self.selected_square = None
        self.my_turn = True
        self.game_over = False
        self.result = None

    def make_move(self, move):
        if move in self.board.legal_moves:
            self.board.push(move)
            self.my_turn = False
            self._check_game_over()
            return True
        return False

    def receive_move(self, move):
        self.board.push(move)
        self.my_turn = True
        self._check_game_over()

    def _check_game_over(self):
        if self.board.is_checkmate():
            self.game_over = True
            self.result = "Checkmate! You won!" if not self.my_turn else "Checkmate! You lost!"
        elif self.board.is_stalemate():
            self.game_over = True
            self.result = "Stalemate!"
        return self.game_over

    def reset(self):
        self.board.reset()
        self.selected_square = None
        self.my_turn = True
        self.game_over = False
        self.result = None