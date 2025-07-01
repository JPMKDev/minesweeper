from window import Window
from point import *

class Cell:
    def __init__(self, window=None):
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window

    def draw(self, newX1, newY1, newX2, newY2):
        self.__x1 = newX1
        self.__y1 = newY1
        self.__x2 = newX2
        self.__y2 = newY2
        if self.__win is None:
            return
        self.__win.draw_line(Line(Point(self.__x1,self.__y2), Point(self.__x2,self.__y2)), "black")
        self.__win.draw_line(Line(Point(self.__x1,self.__y1), Point(self.__x2,self.__y1)), "black")
        self.__win.draw_line(Line(Point(self.__x1,self.__y1), Point(self.__x1,self.__y2)), "black")
        self.__win.draw_line(Line(Point(self.__x2,self.__y1), Point(self.__x2,self.__y2)), "black")

    def center(self):
        return Point((self.__x1+self.__x2)/2,(self.__y1+self.__y2)/2)

    """
    def draw_move(self, to_cell, undo=False):
        center_self = self.center()
        center_other = to_cell.center()
        self.__win.draw_line(Line(center_self, center_other), "gray" if undo else "red")
    """