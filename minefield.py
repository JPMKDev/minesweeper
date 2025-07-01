import random
from time import sleep
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
        self.__create_cells()
        #self.__break_entrance_and_exit()
        if seed is not None:
            random.seed(seed) 
        #self.__break_walls(0, 0)
        #self.__reset_cells_visited()

    def __create_cells(self):
        for y in range(self.num_rows):
            row = []
            for x in range(self.num_cols):
                row.append(Cell(self.window))
            self.__cells.append(row)
        for y in range(len(self.__cells)):
            for x in range(len(self.__cells[y])):
                self.__draw_cell(x, y)
    
    def __draw_cell(self, x, y):
        x_offset = self.x1+self.cell_size_x * x
        y_offset = self.y1+self.cell_size_y * y
        self.__cells[y][x].draw(x_offset, y_offset, x_offset+self.cell_size_x, y_offset+self.cell_size_y)
        self.__animate()
    
    def __animate(self, multiplier=1):
        if self.window is not None:
            self.window.redraw()
            sleep(.01*multiplier)
    
    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[-1][-1].has_bottom_wall = False
        self.__draw_cell(self.num_cols-1, self.num_rows-1)

    def __break_walls(self, x, y):
        current_row = self.__cells[y]
        current = current_row[x]
        current.visited = True
        while(True):
            to_visit = []
            if x>0:
                if not self.__cells[y][x-1].visited:
                    to_visit.append(("left", x-1, y))
            if y>0:
                if not self.__cells[y-1][x].visited:
                    to_visit.append(("top", x, y-1))
            if x<self.num_cols-1:
                if not self.__cells[y][x+1].visited:
                    to_visit.append(("right", x+1, y))
            if y<self.num_rows-1:
                if not self.__cells[y+1][x].visited:
                    to_visit.append(("bottom", x,y+1))
            if len(to_visit) == 0:
                self.__draw_cell(x,y)
                return
            next = random.choice(to_visit)
            #print(next)
            if next[0] == "left":
                current.has_left_wall = False
                self.__cells[next[2]][next[1]].has_right_wall = False
            if next[0] == "right":
                current.has_right_wall = False
                self.__cells[next[2]][next[1]].has_left_wall = False
            if next[0] == "top":
                current.has_top_wall = False
                self.__cells[next[2]][next[1]].has_bottom_wall = False
            if next[0] == "bottom":
                current.has_bottom_wall = False
                self.__cells[next[2]][next[1]].has_top_wall = False
            self.__draw_cell(x, y)
            self.__break_walls(next[1], next[2])

    def __reset_cells_visited(self):
        for row in self.__cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, x, y):
        self.__animate(multiplier=4)
        current = self.__cells[y][x]
        current.visited = True
        if y==self.num_rows-1 and x==self.num_cols-1:
            return True
        for direction in ["right", "down", "left", "up"]:
            target = None
            match direction:
                case "right":
                    if x+1 < self.num_cols and not current.has_right_wall:
                        target = (x+1, y)
                case "down":
                    if y+1 < self.num_rows and not current.has_bottom_wall:
                        target = (x, y+1)
                case "left":
                    if x-1 >= 0 and not current.has_left_wall:
                        target = (x-1, y)
                case "up":
                    if y-1 >= 0 and not current.has_top_wall:
                        target = (x, y-1)
            if target is not None:
                target_cell = self.__cells[target[1]][target[0]]
                if target_cell.visited:
                    continue
                current.draw_move(target_cell)
                path_good = self._solve_r(target[0], target[1])
                if path_good: return path_good
                current.draw_move(target_cell, undo=True)
        return False