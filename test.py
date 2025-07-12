import tkinter as tk

class Container:
    def __init__(self, rows, columns, parent, canvas):
        self.rows = rows
        self.columns = columns
        self.parent = parent
        self.canvas = canvas
        self.buttons = [[tk.Button() for j in range(columns)] for i in range(rows)]

    def generate_buttons(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                self.buttons[i][j] = tk.Button(self.parent, text=("%d,%d" % (i+1, j+1)), command=self.add_row, width=8, height=2)
                self.buttons[i][j].grid(row=i, column=j, sticky='news')

    def add_row(self):
        new_row = []
        for j in range(0, self.columns):
            btn = tk.Button(self.parent, text=("%d,%d" % (self.rows+1, j+1)), command=self.add_row, width=8, height=2)
            btn.grid(row=self.rows, column=j, sticky="news")
            new_row.append(btn)
        self.buttons.append(new_row)
        self.rows += 1
        self.parent.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

root = tk.Tk()
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame_main = tk.Frame(root, bg="gray")
frame_main.grid(sticky='news')

label1 = tk.Label(frame_main, text="Label 1", fg="green")
label1.grid(row=0, column=0, pady=(5, 0), sticky='nw')

label2 = tk.Label(frame_main, text="Label 2", fg="blue")
label2.grid(row=1, column=0, pady=(5, 0), sticky='nw')

label3 = tk.Label(frame_main, text="Label 3", fg="red")
label3.grid(row=3, column=0, pady=5, sticky='nw')

# Create a frame for the canvas with non-zero row&column weights
frame_canvas = tk.Frame(frame_main)
frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = tk.Canvas(frame_canvas, bg="yellow")
canvas.grid(row=0, column=0, sticky="news")

# Link a scrollbar to the canvas
vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Create a frame to contain the buttons

# Create a frame to contain the buttons, and make it scrollable
frame_buttons = tk.Frame(canvas, bg="blue")
window_id = canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

# Make frame_buttons width track the canvas width
def on_canvas_configure(event):
    canvas.itemconfig(window_id, width=event.width)
canvas.bind('<Configure>', on_canvas_configure)


# Add 9-by-5 buttons to the frame

rows = 9
columns = 5
c1 = Container(rows, columns, frame_buttons, canvas)
c1.generate_buttons()

# Update buttons frames idle tasks to let tkinter calculate buttons sizes
frame_buttons.update_idletasks()

# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
first5columns_width = sum([c1.buttons[0][j].winfo_width() for j in range(0, 5)])
first5rows_height = sum([c1.buttons[i][0].winfo_height() for i in range(0, 5)])
frame_canvas.config(width=first5columns_width + vsb.winfo_width(), height=first5rows_height)


# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))

# Launch the GUI
root.mainloop()