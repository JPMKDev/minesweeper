import random
from time import sleep
from tkinter import *
from tkinter import ttk
from cell import *
from gameover import GameOverPopup
    
class Minefield:
    def __init__(
        self,
        num_rows,
        num_cols,
        root,
        parent=None, #parent should be the innermost frame
        main_frame=None, #main_frame of the window
        seed=None #seed is used to generate the minefield randomly
    ):
        self.root = root
        self.num_rows = 2 if num_rows<2 else num_rows
        self.num_cols = 2 if num_cols<2 else num_cols
        self.__parent = parent
        self.__main_frame = main_frame
        self.__available_mines = (self.num_cols * self.num_rows)//6
        self.__cells = []
        self.__counter = IntVar()
        self.__counter.initialize(0)
        self.__boom_counter = IntVar()
        self.__boom_counter.initialize(0)
        self.flagged = IntVar()
        self.flagged.initialize(0)
        if seed is not None:
            random.seed(seed) 
        self.__create_cells()

    def get_cells(self):
        return self.__cells
    
    def get_root(self):
        return self.root.get_root()

    def __inc_counter(self, cell):
        cell.reveal()
        if cell.is_mine:
            self.__boom_counter.set(self.__boom_counter.get() + 1)
        else:
            self.__counter.set(self.__counter.get() + 1)

    def __create_cells(self):
        ttk.Label(self.__main_frame, text="Cells Opened: ").grid(column=0, row=0, sticky=(W, E))
        ttk.Label(self.__main_frame, textvariable=self.__counter).grid(column=1, row=0, sticky=(W, E))
        ttk.Label(self.__main_frame, text="Bombs Marked: ").grid(column=2, row=0, sticky=(W, E))
        ttk.Label(self.__main_frame, textvariable=self.flagged).grid(column=3, row=0, sticky=(W, E))
        #print(num_mines)
        self.__place_cells(6, self.num_rows, row_end=True)
        self.__get_values()

    def __place_cells(self, density, rows=0, row_end=True, cols=0, col_end=True):
        init_huh = self.__cells == []
        if rows > 0:
            for y in range(rows):
                y_pos = y + (0 if init_huh or not row_end else self.num_rows)
                row = []
                for x in range(self.num_cols):
                    is_mine = False
                    if self.__available_mines > 0:
                        is_mine = random.randint(0,density)==0
                        if is_mine:
                            self.__available_mines -= 1
                    print(f"creating cell @ ({x},{y_pos})")
                    row.append(Cell(x, y_pos, is_mine, self.__parent, self.__inc_counter, self))
                if row_end:
                    self.__cells.append(row)
                else:
                    self.__cells.insert(0, row)
        if cols > 0:
            for y in range(self.num_rows):
                    row = self.__cells[y]
                    is_mine = False
                    if self.__available_mines > 0:
                        is_mine = random.randint(0,3)==0
                        if is_mine:
                            self.__available_mines -= 1
                    x = self.num_cols if col_end else 0
                    print(f"creating cell @ ({x},{y})")
                    cell = Cell(x, y, is_mine, self.__parent, self.__inc_counter, self)
                    if col_end:
                        row.append(cell)
                    else:
                        row.insert(0, cell)
    
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
                self.__available_mines += self.num_rows
                for y in range(self.num_rows):
                    for x in range(self.num_cols):
                        self.__cells[y][x].shift_right()
                self.__place_cells(3, cols=1, col_end=False)
                self.num_cols += 1
                self.__get_values(x1=0, x2=2)
            case 2: #Down
                self.__available_mines += self.num_cols
                self.__place_cells(3, rows=1, row_end=True)
                self.num_rows += 1
                self.__get_values(y1=self.num_rows-2, y2=self.num_rows)
            case 6: #Right
                self.__available_mines+=self.num_rows
                self.__place_cells(3, cols=1, col_end=True)
                self.num_cols += 1
                self.__get_values(x1=self.num_cols-2, x2=self.num_cols)
            case 8: #Up
                self.__available_mines += self.num_cols
                for y in range(self.num_rows):
                    for x in range(self.num_cols):
                        self.__cells[y][x].shift_down()
                self.__place_cells(3, rows=1, row_end=False)
                self.num_rows += 1
                self.__get_values(y1=0, y2=2)
        #self.__canvas.config(scrollregion=self.__canvas.bbox("all"))

    def game_over(self, x, y):
        max_distance = max(self.num_rows, self.num_cols)
        boom_speed = 80
        for i in range(max_distance):
            for cell in self.__get_go_cells_ring(x, y, i):
                if cell.game_over():
                    boom_speed *= 0.95
            self.__main_frame.update_idletasks()
            sleep(0.01 * boom_speed)
        sleep(0.5)
        GameOverPopup(self)
        return
    
    def __get_go_cells_ring(self, cx, cy, distance):
        cells= []
        for y in range(self.num_rows):
            for x in range(self.num_cols):
                if ((y == cy-distance or y == cy+distance) and (x >= cx-distance and x <= cx+distance)) or \
                   ((x == cx-distance or x == cx+distance) and (y >= cy-distance and y <= cy+distance)):
                    cells.append(self.__cells[y][x])
        return cells