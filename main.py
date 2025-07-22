import tkinter as tk
from root import *


if __name__ == '__main__':
    root = Root()
    #root.geometry("1000x1000")
    root.create_minefield(20, 20, goal=5)
    #root.create_minefield(40, 40, goal=30)

    root.wait_for_close()