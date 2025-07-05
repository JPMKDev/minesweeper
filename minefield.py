import random
from time import sleep
from tkinter import *
from tkinter import ttk
from cell import *
from functools import partial
    
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
        self.num_rows = 2 if num_rows<2 else num_rows
        self.num_cols = 2 if num_cols<2 else num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self.__cells = []
        self.__counter = IntVar()
        self.__counter.initialize(0)
        self.__boom_counter = IntVar()
        self.__boom_counter.initialize(0)
        if seed is not None:
            random.seed(seed) 
        self.__create_cells(self.__inc_counter)

    def get_cells(self):
        return self.__cells

    def __inc_counter(self, cell):
        cell.reveal()
        if cell.is_mine:
            self.__boom_counter.set(self.__boom_counter.get() + 1)
        else:
            self.__counter.set(self.__counter.get() + 1)

    def __create_cells(self, button_func):
        ttk.Label(self.window.get_canvas(), textvariable=self.__counter).grid(column=0, row=0, sticky=(W, E))
        ttk.Label(self.window.get_canvas(), textvariable=self.__boom_counter).grid(column=1, row=0, sticky=(W, E))
        num_mines = (self.num_cols * self.num_rows)//10
        #print(num_mines)
        for y in range(self.num_rows):
            row = []
            for x in range(self.num_cols):
                is_mine = False
                if num_mines > 0:
                    is_mine = random.randint(0,9)==0
                    if is_mine:
                        num_mines -= 1
                print(f"creating cell @ ({x},{y})")
                row.append(Cell(x, y, is_mine, self.window, button_func, self))
            self.__cells.append(row)
        #print(self.__cells)
        for y in range(self.num_rows):
            for x in range(self.num_cols):
                self.__cells[y][x].get_value()
    
    def __draw_cell(self, x, y):
        self.__cells[y][x].draw()
        self.__animate()
    
    def __animate(self, multiplier=1):
        if self.window is not None:
            self.window.redraw()
            sleep(.01*multiplier)