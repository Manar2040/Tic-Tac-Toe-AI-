# gui.py
import tkinter as tk
from logic import TicTacToe, PLAYER, AI


class TicTacToeGUI:
    """
    Everything visual lives here.  It talks to one TicTacToe
    object for the rules / state, but never does Minimax itself.
    """
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Tic-Tac-Toe")

        # --- Allow user to pick who starts ----------------------------
        self.starter_var = tk.StringVar(value=PLAYER)

        starter_frame = tk.Frame(master)
        starter_frame.grid(row=0, column=0, columnspan=3, pady=2)

        tk.Label(starter_frame, text="Who starts:").pack(side=tk.LEFT)
        tk.Radiobutton(starter_frame, text="You (X)",
                       variable=self.starter_var, value=PLAYER).pack(side=tk.LEFT)
        tk.Radiobutton(starter_frame, text="AI (O)",
                       variable=self.starter_var, value=AI).pack(side=tk.LEFT)

        # --- Create the game-logic object -----------------------------
        self.game = TicTacToe(self.starter_var.get())

        # --- Status label ---------------------------------------------
        self.status = tk.Label(master, text="", font=("Helvetica", 14))
        self.status.grid(row=1, column=0, columnspan=3, pady=5)

        # --- 3×3 buttons ----------------------------------------------
        self.buttons = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                b = tk.Button(master, text='', font=("Helvetica", 20),
                              width=4, height=2,
                              command=lambda i=i, j=j: self.on_click(i, j))
                b.grid(row=i + 2, column=j)   # +2 because of the top rows
                self.buttons[i][j] = b

        # --- Restart button -------------------------------------------
        tk.Button(master, text="Restart",
                  command=self.restart).grid(row=5, column=0, columnspan=3, pady=5)

        # --- Start the first game -------------------------------------
        self.initial_start()

    # ------------------------------------------------------------------
    # Game start / restart helpers
    # -----------------------------------------a-------------------------
    def initial_start(self):
        """Start the very first match when the window opens."""
        self.update_board()
        if self.game.turn == PLAYER:
            self.status.config(text="Your turn!")
        else:
            self.status.config(text="AI is thinking…")
            self.master.after(300, self.ai_turn)

    def restart(self):
        """Called when the user presses the Restart button."""
        starter = self.starter_var.get()
        self.game.reset(starter)
        self.update_board()

        if starter == PLAYER:
            self.status.config(text="Your turn!")
        else:
            self.status.config(text="AI is thinking…")
            self.master.after(300, self.ai_turn)

    # ------------------------------------------------------------------
    # User and AI moves
    # ------------------------------------------------------------------
    def on_click(self, i, j):
        """Handle a human click on cell (i, j)."""
        if self.game.player_move(i, j):
            self.update_board()
            if self.handle_end():
                return
            self.status.config(text="AI is thinking…")
            self.master.after(300, self.ai_turn)

    def ai_turn(self):
        """Let the AI move, then update GUI."""
        self.game.ai_move()
        self.update_board()
        if not self.handle_end():
            self.status.config(text="Your turn!")

    # ------------------------------------------------------------------
    # GUI helpers
    # ------------------------------------------------------------------
    def update_board(self):
        """Write current board symbols into the Tkinter buttons."""
        for i in range(3):
            for j in range(3):
                symbol = self.game.board[i][j]
                self.buttons[i][j]['text']  = symbol
                self.buttons[i][j]['state'] = 'disabled' if symbol else 'normal'

    def handle_end(self) -> bool:
        """Check whether the match is over and show a message."""
        result = self.game.winner()
        if result:
            text = {"X": "You win!",
                    "O": "AI wins!",
                    "DRAW": "It's a draw!"}[result]
            self.status.config(text=text)
            # disable every button
            for row in self.buttons:
                for btn in row:
                    btn['state'] = 'disabled'
            return True
        return False