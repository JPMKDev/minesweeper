import tkinter as tk
from window import *
from minefield import Minefield


if __name__ == '__main__':
    root = Root()
    win = Window(root, 1000, 1000)
    m1 = Minefield(10, 10, 20, 20, 40, 40, win)
    #m1 = Minefield(10, 10, 3, 3, 40, 40, win)

    root.wait_for_close()