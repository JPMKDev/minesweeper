from functools import partial
from window import Window
from point import *
from tkinter import *
from tkinter import ttk

class Cell:
    def __init__(self,x, y, is_mine, window=None, button_func=None, parent=None):
        self.__x = x
        self.__y = y
        self.__win = window
        self.is_mine = is_mine
        self.is_revealed = False
        self.value = 0
        self.revealed_value = StringVar()
        self.revealed_value.set("?")
        self.__parent = parent
        self.btn = Button(self.__win.get_canvas(), textvariable=self.revealed_value, command=partial(button_func, self)).grid(column=x, row=y+1, sticky=W)

    def __repr__(self):
        return f"Cell {self.is_mine}(@{self.__x},{self.__y}) sees {self.value}"
    
    def reveal(self):
        self.revealed_value.set(f"{self.value}{"*"if self.is_mine else ""}")
        self.is_revealed = True
        if self.value == 0:
            cells = self.__parent.get_cells()
            directions_exist = self.direction_exist_huh()
            # numpad notation
            if(directions_exist[3] and directions_exist[0]): #1
                if not cells[self.__y+1][self.__x-1].is_revealed:
                    cells[self.__y+1][self.__x-1].reveal()
            if(directions_exist[3]): #2
                if not cells[self.__y+1][self.__x].is_revealed:
                    cells[self.__y+1][self.__x].reveal()
            if(directions_exist[3] and directions_exist[1]): #3
                if not cells[self.__y+1][self.__x+1].is_revealed:
                    cells[self.__y+1][self.__x+1].reveal()
            if(directions_exist[0]): #4
                if not cells[self.__y][self.__x-1].is_revealed:
                    cells[self.__y][self.__x-1].reveal()
            if(directions_exist[1]): #6
                if not cells[self.__y][self.__x+1].is_revealed:
                    cells[self.__y][self.__x+1].reveal()
            if(directions_exist[2] and directions_exist[0]): #7
                if not cells[self.__y-1][self.__x-1].is_revealed:
                    cells[self.__y-1][self.__x-1].reveal()
            if(directions_exist[2]): #8
                if not cells[self.__y-1][self.__x].is_revealed:
                    cells[self.__y-1][self.__x].reveal()
            if(directions_exist[2] and directions_exist[1]): #9
                if not cells[self.__y-1][self.__x+1].is_revealed:
                    cells[self.__y-1][self.__x+1].reveal()

    def direction_exist_huh(self):
        l_exist = self.__x != 0 #check left
        r_exist = self.__x < len(self.__parent.get_cells()[self.__y])-1 #check right
        u_exist = self.__y != 0 #check up
        d_exist = self.__y < len(self.__parent.get_cells())-1 #check down
        return (l_exist, r_exist, u_exist, d_exist)
    
    def get_value(self):
        value = 0
        directions_exist = self.direction_exist_huh()
        cells = self.__parent.get_cells()
        # numpad notation
        if(directions_exist[3] and directions_exist[0]): #1
            value += 1 if cells[self.__y+1][self.__x-1].is_mine else 0
        if(directions_exist[3]): #2
            value += 1 if cells[self.__y+1][self.__x].is_mine else 0
        if(directions_exist[3] and directions_exist[1]): #3
            value += 1 if cells[self.__y+1][self.__x+1].is_mine else 0
        if(directions_exist[0]): #4
            value += 1 if cells[self.__y][self.__x-1].is_mine else 0
        if(directions_exist[1]): #6
            value += 1 if cells[self.__y][self.__x+1].is_mine else 0
        if(directions_exist[2] and directions_exist[0]): #7
            value += 1 if cells[self.__y-1][self.__x-1].is_mine else 0
        if(directions_exist[2]): #8
            value += 1 if cells[self.__y-1][self.__x].is_mine else 0
        if(directions_exist[2] and directions_exist[1]): #9
            value += 1 if cells[self.__y-1][self.__x+1].is_mine else 0
        self.value = value