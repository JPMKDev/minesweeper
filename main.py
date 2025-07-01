from window import Window
from minefield import Minefield

if __name__ == '__main__':
    win = Window(820,820)
    m1 = Minefield(10, 10, 20, 20, 40, 40, win)

    win.wait_for_close()