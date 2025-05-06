# logic.py
import math

# symbols
PLAYER = 'X'
AI     = 'O'
EMPTY  = ''


class TicTacToe:
    """
    Pure game-logic class.
    No Tkinter or print statements – can be unit-tested in isolation.
    """
    def __init__(self, starter: str = PLAYER):
        # 3×3 board filled with EMPTY strings
        self.board = [[EMPTY] * 3 for _ in range(3)]
        # Whose turn is it now?
        self.turn  = starter

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def reset(self, starter: str = PLAYER) -> None:
        """Clear the board and set who starts."""
        self.__init__(starter)

    def free_cells_exist(self) -> bool:
        """Return True if at least one cell is still EMPTY."""
        return any(c == EMPTY for row in self.board for c in row)

    # ------------------------------------------------------------------
    # win / score detection
    # ------------------------------------------------------------------
    def _score_position(self) -> int:
        """
        Internal helper that returns
        10   if AI already wins,
        -10  if PLAYER already wins,
         0   otherwise.
        """
        b = self.board

        # rows
        for row in b:
            if row[0] == row[1] == row[2] != EMPTY:
                return 10 if row[0] == AI else -10

        # columns
        for col in range(3):
            if b[0][col] == b[1][col] == b[2][col] != EMPTY:
                return 10 if b[0][col] == AI else -10

        # diagonals
        if b[0][0] == b[1][1] == b[2][2] != EMPTY:
            return 10 if b[0][0] == AI else -10
        if b[0][2] == b[1][1] == b[2][0] != EMPTY:
            return 10 if b[0][2] == AI else -10

        return 0

    def winner(self):
        """
        Return 'O' for AI win, 'X' for player win, 'DRAW' for tie,
        or None if the game is still going on.
        """
        score = self._score_position()
        if score == 10:
            return AI
        if score == -10:
            return PLAYER
        if not self.free_cells_exist():
            return "DRAW"
        return None

    # ------------------------------------------------------------------
    # minimax with alpha–beta pruning
    # ------------------------------------------------------------------
    def _minimax(self, is_max: bool, alpha=-math.inf, beta=math.inf) -> int:
        score = self._score_position()
        # terminal node
        if score != 0 or not self.free_cells_exist():
            return score

        if is_max:                              # AI branch
            best = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == EMPTY:
                        self.board[i][j] = AI
                        best = max(best, self._minimax(False, alpha, beta))
                        self.board[i][j] = EMPTY
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            return best
            return best
        else:                                   # Player branch
            best = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == EMPTY:
                        self.board[i][j] = PLAYER
                        best = min(best, self._minimax(True, alpha, beta))
                        self.board[i][j] = EMPTY
                        beta = min(beta, best)
                        if beta <= alpha:
                            return best
            return best

    def best_move_for_ai(self):
        """Return (row, col) where the AI should move."""
        best_val = -math.inf
        move     = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = AI
                    val = self._minimax(False)
                    self.board[i][j] = EMPTY
                    if val > best_val:
                        best_val, move = val, (i, j)
        return move

    # ------------------------------------------------------------------
    # public move methods
    # ------------------------------------------------------------------
    def player_move(self, i: int, j: int) -> bool:
        """Place 'X' if it's player's turn and the cell is free."""
        if self.turn == PLAYER and self.board[i][j] == EMPTY:
            self.board[i][j] = PLAYER
            self.turn = AI
            return True
        return False

    def ai_move(self) -> None:
        """Compute and do AI move if it is AI's turn."""
        if self.turn == AI:
            i, j = self.best_move_for_ai()
            if i != -1:
                self.board[i][j] = AI
            self.turn = PLAYER