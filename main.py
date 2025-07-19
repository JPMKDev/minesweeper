import tkinter as tk
from root import *


if __name__ == '__main__':
    root = Root()
    #root.geometry("1000x1000")
    root.create_minefield(20, 20)
    #root.create_minefield(40, 40)

    root.wait_for_close()