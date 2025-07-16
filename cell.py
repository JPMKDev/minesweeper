from functools import partial
from tkinter import *

class Cell:
    def __init__(self,x, y, is_mine, parent_frame, button_func=None, minefield=None):
        self.__x = x
        self.__y = y
        self.__parent_frame = parent_frame
        self.is_mine = is_mine
        self.is_revealed = False
        self.value = 0
        self.revealed_value = StringVar()
        self.revealed_value.set("?")
        self.__minefield = minefield
        self.btn = Button(self.__parent_frame, height=1, width=1, textvariable=self.revealed_value, command=partial(button_func, self))
        self.btn.grid(column=x, row=y, sticky='news')

    def __repr__(self):
        return f"Cell {self.is_mine}(@{self.__x},{self.__y}) sees {self.value}"
    
    def shift_right(self):
        self.__x += 1
        self.btn.grid(column=self.__x, row=self.__y, sticky='news')
    
    def shift_down(self):
        self.__y += 1
        self.btn.grid(column=self.__x, row=self.__y, sticky='news')
        
    
    def reveal(self):
        if self.__x == 0:
            self.__minefield.expand(4)
        if self.__y == 0:
            self.__minefield.expand(8) #up
        if self.__y == self.__minefield.num_rows - 1:
            self.__minefield.expand(2)#down
        if self.__x == self.__minefield.num_cols - 1:
            self.__minefield.expand(6)#right
        self.revealed_value.set(f"{self.value}{"*"if self.is_mine else ""}")
        #self.btn.grid(column=self.__x + 20, row=self.__y+1)
        self.is_revealed = True
        match(self.value):
            case 0:
                self.btn.config(bg="LightCyan3", activebackground="LightCyan2")
                adj_cells = self.get_adjacent_cells()
                for cell in adj_cells:
                    if cell is not None and not cell.is_revealed:
                        cell.reveal()
            case 1:
                self.btn.config(bg="PaleTurquoise3", activebackground="PaleTurquoise2")
            case 2:
                self.btn.config(bg="PaleGreen3", activebackground="PaleGreen1")
            case 3:
                self.btn.config(bg="SpringGreen3", activebackground="SpringGreen2")
            case 4:
                self.btn.config(bg="Yellow3", activebackground="Yellow2")
            case 5:
                self.btn.config(bg="Firebrick2", activebackground="Firebrick1")
            case 6:
                self.btn.config(bg="OrangeRed3", activebackground="OrangeRed2")
            case 7:
                self.btn.config(bg="Red3", activebackground="Red2")
            case _: #8
                self.btn.config(bg="Purple3", activebackground="Purple2")


            

    def get_adjacent_cells(self):
        l_exist = self.__x != 0 #check left
        r_exist = self.__x < len(self.__minefield.get_cells()[self.__y])-1 #check right
        u_exist = self.__y != 0 #check up
        d_exist = self.__y < len(self.__minefield.get_cells())-1 #check down
        cells = self.__minefield.get_cells()
        adjacent = []
        # numpad notation
        adjacent.append(cells[self.__y+1][self.__x-1] if d_exist and l_exist else None) #1
        adjacent.append(cells[self.__y+1][self.__x] if d_exist else None) #2
        adjacent.append(cells[self.__y+1][self.__x+1] if d_exist and r_exist else None) #3
        adjacent.append(cells[self.__y][self.__x-1] if l_exist else None) #4
        adjacent.append(cells[self.__y][self.__x+1] if r_exist else None) #6
        adjacent.append(cells[self.__y-1][self.__x-1] if u_exist and l_exist else None) #7
        adjacent.append(cells[self.__y-1][self.__x] if u_exist else None) #8
        adjacent.append(cells[self.__y-1][self.__x+1] if u_exist and r_exist else None) #9

        return adjacent
    
    def get_value(self):
        value = 0
        adj_cells = self.get_adjacent_cells()
        for cell in adj_cells:
            value += 1 if cell is not None and cell.is_mine else 0
        self.value = value