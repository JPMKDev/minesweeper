from tkinter import *

class GameOverPopup:
    def __init__(self, parent, message="You Lost!", color="red"):
        root = parent.get_root()
        self.top = Toplevel(root)
        self.top.title("Game Over")
        self.top.geometry("200x100")
        self.top.resizable(False, False)
        Label(self.top, text=message, font=("Arial", 16), fg=color).pack(padx=20, pady=10)
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