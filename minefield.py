import random
from time import sleep
from tkinter import *
from tkinter import ttk
from cell import *
    
class Minefield:
    def __init__(
        self,
        num_rows,
        num_cols,
        parent=None, #parent should be the innermost frame
        canvas=None, #canvas should be the canvas which holds the parent and the scrollbar
        seed=None #seed is used to generate the minefield randomly
    ):
        self.num_rows = 2 if num_rows<2 else num_rows
        self.num_cols = 2 if num_cols<2 else num_cols
        self.__parent = parent
        self.__canvas = canvas
        self.__available_mines = (self.num_cols * self.num_rows)//6
        self.__cells = []
        self.__counter = IntVar()
        self.__counter.initialize(0)
        self.__boom_counter = IntVar()
        self.__boom_counter.initialize(0)
        if seed is not None:
            random.seed(seed) 
        self.__create_cells()

    def get_cells(self):
        return self.__cells

    def __inc_counter(self, cell):
        cell.reveal()
        if cell.is_mine:
            self.__boom_counter.set(self.__boom_counter.get() + 1)
        else:
            self.__counter.set(self.__counter.get() + 1)

    def __create_cells(self):
        #ttk.Label(self.master.get_canvas(), textvariable=self.__counter).grid(column=0, row=0, sticky=(W, E)) #replace get_canvas with root.mainframe
        #ttk.Label(self.master.get_canvas(), textvariable=self.__boom_counter).grid(column=1, row=0, sticky=(W, E))
        #print(num_mines)
        for y in range(self.num_rows):
            row = []
            for x in range(self.num_cols):
                is_mine = False
                if self.__available_mines > 0:
                    is_mine = random.randint(0,6)==0
                    if is_mine:
                        self.__available_mines -= 1
                print(f"creating cell @ ({x},{y})")
                row.append(Cell(x, y, is_mine, self.__parent, self.__inc_counter, self))
            self.__cells.append(row)
        #print(self.__cells)
        for y in range(self.num_rows):
            for x in range(self.num_cols):
                self.__cells[y][x].get_value()

    def expand(self, direction): #direction should be in numpad notation
        match direction:
            case 4: #Left
                pass #left expansion is not implemented
            case 2: #Down
                self.__available_mines += self.num_cols
                row = []
                for x in range(self.num_cols):
                    is_mine = False
                    if self.__available_mines > 0:
                        is_mine = random.randint(0,3)==0
                        if is_mine:
                            self.__available_mines -= 1
                    print(f"creating cell @ ({x},{self.num_rows})")
                    row.append(Cell(x, self.num_rows, is_mine, self.__parent, self.__inc_counter, self))
                self.__cells.append(row)
                self.num_rows += 1
                for y in range(self.num_rows-2, self.num_rows):
                    for x in range(self.num_cols):
                        self.__cells[y][x].get_value()
            case 6: #Right
                self.__available_mines+=self.num_rows
                for y in range(len(self.__cells)):
                    row = self.__cells[y]
                    is_mine = False
                    if self.__available_mines > 0:
                        is_mine = random.randint(0,3)==0
                        if is_mine:
                            self.__available_mines -= 1
                    print(f"creating cell @ ({self.num_cols},{y})")
                    row.append(Cell(self.num_cols, y, is_mine, self.__parent, self.__inc_counter, self))
                self.num_cols += 1
                for y in range(self.num_rows):
                    for x in range(self.num_cols-2, self.num_cols):
                        self.__cells[y][x].get_value()
            case 8: #Up
                pass #up expansion is not implemented
        self.__canvas.config(scrollregion=self.__canvas.bbox("all"))
    
    def __draw_cell(self, x, y):
        self.__cells[y][x].draw()
        self.__animate()
    
    def __animate(self, multiplier=1):
        if self.master is not None:
            self.master.redraw()
            sleep(.01*multiplier)