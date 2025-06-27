import tkinter as tk

CELL_SIZE = 40
ERASER_SIZE = 20
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

class EraserApp:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
        self.canvas.pack()
        self.cells = []
        self.create_grid()

        self.eraser = self.canvas.create_rectangle(0, 0, ERASER_SIZE, ERASER_SIZE, fill='pink', outline='black')
        self.canvas.bind('<Motion>', self.move_eraser)

    def create_grid(self):
        for y in range(0, CANVAS_HEIGHT, CELL_SIZE):
            for x in range(0, CANVAS_WIDTH, CELL_SIZE):
                cell = self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill='blue', outline='black')
                self.cells.append(cell)

    def move_eraser(self, event):
        self.canvas.coords(self.eraser, event.x, event.y, event.x + ERASER_SIZE, event.y + ERASER_SIZE)
        self.erase(event.x, event.y)

    def erase(self, x, y):
        overlapping = self.canvas.find_overlapping(x, y, x + ERASER_SIZE, y + ERASER_SIZE)
        for obj in overlapping:
            if obj != self.eraser:
                self.canvas.itemconfig(obj, fill='white')

def main():
    root = tk.Tk()
    root.title("Eraser Canvas")
    app = EraserApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
