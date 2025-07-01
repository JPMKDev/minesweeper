from tkinter import Tk, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Minesweeper")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(master=self.__root, height=height, width=width)
        self.__canvas.pack()
        self.running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while(self.running):
            self.redraw()
    
    def close(self):
        self.running = False

    def draw_line(self, line, color):
        line.draw(self.__canvas, color)