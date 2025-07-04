from functools import partial
from window import Window
from point import *
from tkinter import *
from tkinter import ttk

class Cell:
    def __init__(self,x, y, is_mine, window=None, button_func=None):
        self.__x = x
        self.__y = y
        self.__win = window
        self.is_mine = is_mine
        self.is_revealed = False
        self.value = 0
        self.revealed_value = StringVar()
        self.revealed_value.set("?")
        self.btn = Button(self.__win.get_canvas(), textvariable=self.revealed_value, command=partial(button_func, self)).grid(column=x, row=y+1, sticky=W)

    def __repr__(self):
        return f"Cell {self.is_mine}(@{self.__x},{self.__y}) sees {self.value}"
    
    def reveal(self):
        self.revealed_value.set(f"{self.value}{"*"if self.is_mine else ""}")
        self.is_revealed = True
        #print(self)
    
    def get_value(self, cells):
        value = 0
        l_exist = self.__x != 0 #check left
        r_exist = self.__x < len(cells[self.__y])-1 #check right
        u_exist = self.__y != 0 #check up
        d_exist = self.__y < len(cells)-1 #check down
        # numpad notation
        if(d_exist and l_exist): #1
            value += 1 if cells[self.__y+1][self.__x-1].is_mine else 0
        if(d_exist): #2
            value += 1 if cells[self.__y+1][self.__x].is_mine else 0
        if(d_exist and r_exist): #3
            value += 1 if cells[self.__y+1][self.__x+1].is_mine else 0
        if(l_exist): #4
            value += 1 if cells[self.__y][self.__x-1].is_mine else 0
        if(r_exist): #6
            value += 1 if cells[self.__y][self.__x+1].is_mine else 0
        if(u_exist and l_exist): #7
            value += 1 if cells[self.__y-1][self.__x-1].is_mine else 0
        if(u_exist): #8
            value += 1 if cells[self.__y-1][self.__x].is_mine else 0
        if(u_exist and r_exist): #9
            value += 1 if cells[self.__y-1][self.__x+1].is_mine else 0
        self.value = value