from tkinter import Canvas

class Grid:
    def __init__(self, dim, bots=[]):
        self.dim = dim
        self.bots = bots

    def makeGrid(self, window):
        self.canvas = Canvas(window, width=self.dim[0]*100, height=self.dim[1]*100)
        self.canvas.pack()

    def updateGrid(self):
        for i in range(self.dim[0]):
            lineLength = 100
            x = i*lineLength+lineLength/2
            self.canvas.create_line(x,lineLength/2, x, self.dim[0]*lineLength-lineLength/2, fill='gray', dash=(2,2))