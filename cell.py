from window import Window
from point import *
from tkinter import *
from tkinter import ttk

class Cell:
    def __init__(self,x, y, is_mine, window=None, button_func=None):
        self.__win = window
        self.__is_mine = is_mine
        self.__is_revealed = False
        self.btn = Button(self.__win.get_canvas(), text="?", command=button_func).grid(column=x, row=y, sticky=W)