from tkinter import Canvas

class Grid:

    def __init__(self, dim, obst=[], bots=[]):
        self.dim = dim
        self.bots = bots
        self.obst = obst
        self.initGridInfo()

    def initGridInfo(self):
        self.gridInfo = []
        for i in range(self.dim[0]):
            self.gridInfo.append([])
            for j in range(self.dim[1]):
                self.gridInfo[i].append(-1)
        
        for pos in self.obst:
            self.gridInfo[pos["x"]][pos["y"]] = 0

    def openSpace(self, x, y):
        if self.gridInfo[x][y] == -1:
            return True
        return False

    def makeGrid(self, window):
        self.canvas = Canvas(window, width=(self.dim[0]*100), height=(self.dim[1]*100))
        self.canvas.pack()

    def updateGrid(self, squareSize=100):
        self.canvas.delete("all")
        for j in range(self.dim[1]):
            augJ = j*squareSize
            for i in range(self.dim[0]):
                augI = i*squareSize
                if self.gridInfo[i][j]==0:
                    self.canvas.create_rectangle(augI, augJ, augI+squareSize, augJ+squareSize, fill="black")
                else:
                    self.canvas.create_rectangle(augI, augJ, augI+squareSize, augJ+squareSize)
        
        for bot in self.bots:
            pos = bot.pos
            x0 = (pos[0]*100)+20
            x1 = (pos[0]*100)+80
            y0 = (pos[1]*100)+20
            y1 = (pos[1]*100)+80
            self.canvas.create_oval(x0,y0,x1,y1, fill=bot.color)