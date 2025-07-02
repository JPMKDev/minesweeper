import random
from time import sleep
from tkinter import *
from tkinter import ttk
from cell import *
    
class Minefield:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        window=None,
        seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self.__cells = []
        self.__counter = IntVar()
        self.__counter.initialize(0)
        if seed is not None:
            random.seed(seed) 
        self.__create_cells(self.__inc_counter)

    def __inc_counter(self):
        self.__counter.set(self.__counter.get() + 1)

    def __create_cells(self, button_func):
        ttk.Label(self.window.get_canvas(), textvariable=self.__counter).grid(column=0, row=0, sticky=(W, E))
        for y in range(self.num_rows):
            row = []
            for x in range(self.num_cols):
                row.append(Cell(x, y+1, self.window, button_func))
            self.__cells.append(row)
    
    def __draw_cell(self, x, y):
        self.__cells[y][x].draw()
        self.__animate()
    
    def __animate(self, multiplier=1):
        if self.window is not None:
            self.window.redraw()
            sleep(.01*multiplier)