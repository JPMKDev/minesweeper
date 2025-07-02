from tkinter import *
from tkinter import ttk

class Root:
    def __init__(self):
        self.__root = Tk()
        self.__root.title("Minesweeper")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.main_frame = ttk.Frame(self.__root, padding="3 3 12 12")
        self.main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while(self.running):
            self.redraw()
    
    def close(self):
        self.running = False

class Window:
    def __init__(self, root, width, height):
        self.__root = root
        self.__parent = self.__root.main_frame
        self.__canvas = Canvas(master=self.__parent, height=height, width=width)
        self.__canvas.pack()
        self.running = False
    
    def get_canvas(self):
        return self.__canvas

    def redraw(self):
        self.__root.redraw()