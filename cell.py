from tkinter import *

from gameover import GameOverPopup

# Cell class represents a single cell in the Minesweeper game
# It handles the cell's state, appearance, and interactions
class Cell:
    #initialize a cell with its position, whether it is a mine, the parent frame, and the minefield it belongs to
    def __init__(self, x, y, is_mine, parent_frame, minefield=None):
        self.__x = x
        self.__y = y
        self.__parent_frame = parent_frame
        self.is_mine = is_mine
        self.is_revealed = False #set some default values
        self.locked = False
        self.flagged = False
        self.value = 0
        self.revealed_value = StringVar()
        self.revealed_value.set("?")
        self.__minefield = minefield
        self.btn = Button(self.__parent_frame, height=1, width=1, textvariable=self.revealed_value, command=self.__click)
        self.__btn_color = self.btn.cget("bg") #store default colors for the button so they can be restored
        self.__btn_active_color = self.btn.cget("activebackground")
        self.btn.bind("<Button-3>", lambda event: self.__mark())  # bind a right click to the mark function
        self.btn.grid(column=x, row=y, sticky='news') #place the button in the grid

    #what the cell does when clicked
    def __click(self):
        if not self.__minefield.first_clicked: #prevent the first click from being a mine
            self.is_mine = False
            self.get_value()
            adjacent = self.__get_adjacent_cells()
            for cell in adjacent:
                if cell is not None:
                    cell.get_value()
            self.__minefield.first_click()
        self.__reveal()
        if not self.is_mine: #if the cell is not a mine, increment the counter of opened cells
            self.__minefield.counter.set(self.__minefield.counter.get() + 1)

    #string representation of the cell
    #this is used for debugging and logging purposes
    def __repr__(self):
        return f"Cell {self.is_mine}(@{self.__x},{self.__y}) sees {self.value}"
    
    #shift the cell to the right
    def shift_right(self):
        self.__x += 1
        self.btn.grid(column=self.__x, row=self.__y, sticky='news')
    
    #shift the cell down
    def shift_down(self):
        self.__y += 1
        self.btn.grid(column=self.__x, row=self.__y, sticky='news')

    #mark the cell as a mine or unmark it    
    def __mark(self):
        if not self.is_revealed and self.__minefield.first_clicked: #disable marking until the first click
            self.btn.config(relief=SUNKEN, state=DISABLED, bg="darkgray", activebackground="darkgray")
            if self.is_mine and not self.locked: #if the marked cell is a mine, lock it and add it to the flagged count. yes this means you can cheat by marking and attempting to unmark every cell. This is a prototype and not meant to be a complete game
                self.flagged = True
                self.locked = True
                num_flagged = self.__minefield.flagged+1
                if num_flagged >= self.__minefield.goal:
                    self.__minefield.game_over_victory()
                self.__minefield.update_flagged(num_flagged)
            elif self.flagged and not self.locked :
                self.flagged = False
                self.btn.config(relief=RAISED, state=NORMAL, bg=self.__btn_color, activebackground=self.__btn_active_color)
            else:
                self.flagged = True
    
    #reveal the cell
    def __reveal(self):
        if self.is_mine: #if the cell is a mine, end the game
            self.__minefield.game_over(self.__x, self.__y)
            return
        if self.__x == 0:#if the cell is on an edge, expand the minefield
            self.__minefield.expand(4)#left
        if self.__y == 0:
            self.__minefield.expand(8) #up
        if self.__y == self.__minefield.num_rows - 1:
            self.__minefield.expand(2)#down
        if self.__x == self.__minefield.num_cols - 1:
            self.__minefield.expand(6)#right
        self.revealed_value.set(f"{self.value}{"*"if self.is_mine else ""}") #reveal the value of the cell
        #self.btn.grid(column=self.__x + 20, row=self.__y+1)
        self.is_revealed = True
        match(self.value): #set the color of the button based on the value of the cell
            case 0:
                self.btn.config(bg="LightCyan3", activebackground="LightCyan2")
                adj_cells = self.__get_adjacent_cells()
                for cell in adj_cells:
                    if cell is not None and not cell.is_revealed:
                        cell.btn.invoke()
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

    #if the cell is a mine, turn red and return True, otherwise return False
    def game_over(self):
        if self.is_mine:
            self.btn.config(bg="red", activebackground="red", text="*", state=DISABLED)
            return True
        else:
            return False
        
    #get the adjacent cells of the cell, used to calculate the value of the cell
    def __get_adjacent_cells(self):
        cells = self.__minefield.get_cells()
        l_exist = self.__x != 0 #check left
        r_exist = self.__x < len(cells[self.__y])-1 #check right
        u_exist = self.__y != 0 #check up
        d_exist = self.__y < len(cells)-1 #check down
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

    #get the value of the cell, which is the number of adjacent mines    
    def get_value(self):
        value = 0
        adj_cells = self.__get_adjacent_cells()
        for cell in adj_cells:
            value += 1 if cell is not None and cell.is_mine else 0
        self.value = value