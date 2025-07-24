import random
from time import sleep
from tkinter import *
from tkinter import ttk
from cell import *
from gameover import GameOverPopup

# Minefield class represents the minefield in the Minesweeper game
# It handles the creation of cells, the game logic, and the user interface
class Minefield:
    def __init__(
        self,
        num_rows,
        num_cols,
        root,
        goal=100, #goal is the number of mines to be marked
        parent=None, #parent should be the innermost frame
        main_frame=None, #main_frame of the window
        seed=None #seed is used to generate the minefield randomly
    ):
        self.root = root
        self.num_rows = 2 if num_rows<2 else num_rows
        self.num_cols = 2 if num_cols<2 else num_cols
        self.goal = goal
        self.__parent = parent
        self.__main_frame = main_frame
        self.__available_mines = (self.num_cols * self.num_rows)//6
        self.__cells = []
        self.counter = IntVar()
        self.counter.initialize(0)
        self.flagged = 0
        self.flagged_str = StringVar()
        self.flagged_str.initialize("")
        self.first_clicked = False
        if seed is not None:
            random.seed(seed)
        
        ttk.Label(self.__main_frame, text="Cells Opened: ").grid(column=0, row=0, sticky=(W, E))
        ttk.Label(self.__main_frame, textvariable=self.counter).grid(column=1, row=0, sticky=(W, E))
        ttk.Label(self.__main_frame, text="Bombs Marked: ").grid(column=2, row=0, sticky=(W, E))
        ttk.Label(self.__main_frame, textvariable=self.flagged_str).grid(column=3, row=0, sticky=(W, E))
        self.__create_cells()

    #track if any cell has been clicked
    def first_click(self):
        self.first_clicked = True
        self.__available_mines += 1

    #accessor for the cells in the minefield
    def get_cells(self):
        return self.__cells
    
    #accessor for the tkinter root object
    def get_root(self):
        return self.root.get_root()
    
    #update the number of flagged cells with respect to the goal
    def update_flagged(self, new_flagged):
        self.flagged = new_flagged
        self.flagged_str.set(f"{self.flagged}/{self.goal}")
        #self.__main_frame.update_idletasks()

    #initialize the cells in the minefield
    def __create_cells(self):
        self.__place_cells(6, self.num_rows, row_end=True)
        self.__get_values()

    #place cells in the minefield with a given density and number of rows or 1 column
    #if row_end or col_end are true, the cells will be placed at the end of the row or column
    def __place_cells(self, density, rows=0, row_end=True, cols=False, col_end=True):
        init_huh = self.__cells == [] #if there are no cells yet, we need to initialize the minefield
        if rows > 0:
            for y in range(rows):
                y_pos = y + (0 if init_huh or not row_end else self.num_rows) #if initializing minefield, there is no offset
                row = []
                for x in range(self.num_cols):
                    is_mine = False
                    if self.__available_mines > 0:
                        is_mine = random.randint(0,density)==0 #calculate if this cell is a mine based on the density
                        if is_mine:
                            self.__available_mines -= 1
                    #print(f"creating cell @ ({x},{y_pos})")
                    row.append(Cell(x, y_pos, is_mine, self.__parent, self))
                if row_end: # if row_end is true, append the row to the end of the cells, else insert it at the beginning
                    self.__cells.append(row)
                else:
                    self.__cells.insert(0, row)
        if cols: # this should be able to add multiple columns but I did not find the need to implement it, so it is currently a boolean
            for y in range(self.num_rows): #for each row of cells:
                    row = self.__cells[y]
                    is_mine = False
                    if self.__available_mines > 0:
                        is_mine = random.randint(0,3)==0
                        if is_mine:
                            self.__available_mines -= 1
                    x = self.num_cols if col_end else 0
                    #print(f"creating cell @ ({x},{y})")
                    cell = Cell(x, y, is_mine, self.__parent, self)
                    if col_end: #add a cell to the beginning or end of the row
                        row.append(cell)
                    else:
                        row.insert(0, cell)
    
    #get the values of all cells between the given coordinates, inclusive
    def __get_values(self, x1=0, x2=None, y1=0, y2=None):
        if x2 is None:
            x2 = self.num_cols
        if y2 is None:
            y2 = self.num_rows
        for y in range(y1, y2):
            for x in range(x1, x2):
                self.__cells[y][x].get_value()

    #expand the minefield in a given direction
    #direction should be in numpad notation: 4=left, 2=down 6=right, 8=up
    def expand(self, direction):
        match direction:
            case 4: #Left
                self.__available_mines += self.num_rows
                for y in range(self.num_rows): #move the cells to the right to make space for the new column
                    for x in range(self.num_cols):
                        self.__cells[y][x].shift_right()
                self.__place_cells(3, cols=True, col_end=False) #place the new column at the beginning
                self.num_cols += 1
                self.__get_values(x1=0, x2=2) #get the values of the new cells and the adjacent cells
            case 2: #Down
                self.__available_mines += self.num_cols
                self.__place_cells(3, rows=1, row_end=True) #place a new row at the end
                self.num_rows += 1
                self.__get_values(y1=self.num_rows-2, y2=self.num_rows) #update the values of the new row and the adjacent cells
            case 6: #Right
                self.__available_mines+=self.num_rows
                self.__place_cells(3, cols=True, col_end=True) #place a new column at the end
                self.num_cols += 1
                self.__get_values(x1=self.num_cols-2, x2=self.num_cols) #update the values of the new column and the adjacent cells
            case 8: #Up
                self.__available_mines += self.num_cols
                for y in range(self.num_rows): #move the cells down to make space for the new row
                    for x in range(self.num_cols):
                        self.__cells[y][x].shift_down()
                self.__place_cells(3, rows=1, row_end=False) #place a new row at the beginning
                self.num_rows += 1
                self.__get_values(y1=0, y2=2) #update the values of the new row and the adjacent cells
        #self.__canvas.config(scrollregion=self.__canvas.bbox("all"))

    #end the game, starting with a mine at the given coordinates
    #this will reveal all cells in rings around the mine, and then show a game over popup
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
    
    #end the game with a victory popup
    def game_over_victory(self):
        GameOverPopup(self, "You win!", "green")
        return
    
    #get the cells in a ring around the given coordinates, at a given distance, helper function for game_over
    def __get_go_cells_ring(self, cx, cy, distance):
        cells= []
        for y in range(self.num_rows):
            for x in range(self.num_cols):
                if ((y == cy-distance or y == cy+distance) and (x >= cx-distance and x <= cx+distance)) or \
                   ((x == cx-distance or x == cx+distance) and (y >= cy-distance and y <= cy+distance)):
                    cells.append(self.__cells[y][x])
        return cells