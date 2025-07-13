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
        self.__place_cells(6, self.num_rows, row_end=True)
        self.__get_values()

    def __place_cells(self, density, rows=0, row_end=True, cols=0, col_end=True):
        init_huh = self.__cells == []
        if rows > 0 and row_end:
            for y in range(rows):
                y_pos = y + (0 if init_huh else self.num_rows)
                row = []
                for x in range(self.num_cols):
                    is_mine = False
                    if self.__available_mines > 0:
                        is_mine = random.randint(0,density)==0
                        if is_mine:
                            self.__available_mines -= 1
                    print(f"creating cell @ ({x},{y_pos})")
                    row.append(Cell(x, y_pos, is_mine, self.__parent, self.__inc_counter, self))
                self.__cells.append(row)
            
    
    def __get_values(self, x1=0, x2=None, y1=0, y2=None):
        if x2 is None:
            x2 = self.num_cols
        if y2 is None:
            y2 = self.num_rows
        for y in range(y1, y2):
            for x in range(x1, x2):
                self.__cells[y][x].get_value()


    def expand(self, direction): #direction should be in numpad notation
        match direction:
            case 4: #Left
                pass #left expansion is not implemented
            case 2: #Down
                self.__available_mines += self.num_cols
                self.__place_cells(3, rows=1, row_end=True)
                self.num_rows += 1
                self.__get_values(y1=self.num_rows-2, y2=self.num_rows)
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
                self.__get_values(x1=self.num_cols-2, x2=self.num_cols)
            case 8: #Up
                pass #up expansion is not implemented
        #self.__canvas.config(scrollregion=self.__canvas.bbox("all"))
    
    def __draw_cell(self, x, y):
        self.__cells[y][x].draw()
        self.__animate()
    
    def __animate(self, multiplier=1):
        if self.master is not None:
            self.master.redraw()
            sleep(.01*multiplier)