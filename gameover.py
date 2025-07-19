from tkinter import *
from tkinter import ttk

class GameOverPopup:
    def __init__(self, parent, message="Game Over!"):
        self.top = Toplevel(parent.get_root())
        self.top.title("Game Over")
        self.top.grab_set()
        self.top.resizable(False, False)
        self.top.transient(parent.get_root())
        Label(self.top, text=message, font=("Arial", 16), fg="red").pack(padx=20, pady=10)
        Button(self.top, text="OK", command=self.close).pack(pady=(0, 10))
        # Disable all cells in the minefield
        for row in parent.get_cells():
            for cell in row:
                try:
                    cell.btn.config(state=DISABLED)
                except Exception:
                    pass
    def close(self):
        self.top.destroy()