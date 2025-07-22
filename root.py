from tkinter import *
from tkinter import ttk
from minefield import Minefield

class Root:
    def __init__(self):
        self.__root = Tk()
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.columnconfigure(0, weight=1)
        self.__root.title("Minesweeper")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__main_frame = ttk.Frame(self.__root, padding="3 3 12 12")
        self.__main_frame.grid(sticky="news")

        self.__canvas_frame = Frame(self.__main_frame)
        self.__canvas_frame.grid(row=2, column=0, columnspan=12, pady=(5,0), sticky='nw')
        self.__canvas_frame.grid_rowconfigure(0, weight=1)
        self.__canvas_frame.grid_columnconfigure(0, weight=1)
        self.__canvas_frame.grid_propagate(False)

        self.__canvas = Canvas(self.__canvas_frame)
        self.__canvas.grid(row=0, column=0, sticky="news")

        self.__vsb = Scrollbar(self.__canvas_frame, orient="vertical", command=self.__canvas.yview)
        self.__vsb.grid(row=0, column=1, sticky='ns')
        self.__canvas.configure(yscrollcommand=self.__vsb.set)

        self.__hsb = Scrollbar(self.__canvas_frame, orient="horizontal", command=self.__canvas.xview)
        self.__hsb.grid(row=1, column=0, sticky='ew')
        self.__canvas.configure(xscrollcommand=self.__hsb.set)

        self.__board_frame = Frame(self.__canvas)
        self.__canvas.create_window((0, 0), window=self.__board_frame, anchor='nw')

        self.minefield = None

    def get_root(self):
        return self.__root

    def geometry(self, geometry):
        self.__root.geometry(geometry)

    def create_minefield(self, num_rows, num_cols, goal=100, seed=None):
        self.minefield = Minefield(num_rows, num_cols, self, goal, self.__board_frame, self.__main_frame, seed=seed)
        self.__board_frame.update_idletasks()
        self.__resize_canvas_frame()

    def __resize_canvas_frame(self):
        cells = self.minefield.get_cells()
        first5columns_width = cells[0][0].btn.winfo_width() * 25
        first5rows_height = cells[0][0].btn.winfo_height() * 25
        self.__canvas_frame.config(width=first5columns_width + self.__vsb.winfo_width(), height=first5rows_height + self.__hsb.winfo_height())
        self.__canvas.config(scrollregion=self.__canvas.bbox("all"))


    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
        self.__canvas.config(scrollregion=self.__canvas.bbox("all"))

    def wait_for_close(self):
        self.running = True
        while(self.running):
            self.redraw()
    
    def close(self):
        self.running = False