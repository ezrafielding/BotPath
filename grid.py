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
            self.updateGridInfo(pos["x"],pos["y"], 0)

    def updateGridInfo(self, x, y, state):
        self.gridInfo[x][y] = state

    def openSpace(self, x, y):
        if self.gridInfo[x][y] == -1:
            return True
        return False

    def makeGrid(self, window):
        self.canvas = Canvas(window, width=(self.dim[0]*100), height=(self.dim[1]*100))
        self.canvas.pack()

    def appendBot(self, bot):
        self.bots.append(bot)
        self.updateGridInfo(bot.pos[0], bot.pos[1], 1)
        self.updateGridInfo(bot.goal[0], bot.goal[1], 2)

    def updateGrid(self, squareSize=100):
        self.canvas.delete("robots")
        for j in range(self.dim[1]):
            augJ = (j*squareSize)
            for i in range(self.dim[0]):
                augI = (i*squareSize)
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
            self.canvas.create_oval(x0,y0,x1,y1, fill=bot.color, tags="robots")

            goal = bot.goal
            x0 = (goal[0]*100)
            x1 = (goal[0]*100)+100
            y0 = (goal[1]*100)
            y1 = (goal[1]*100)+100
            self.canvas.create_line(x0,y0,x1,y1, width=2, fill=bot.color)
            self.canvas.create_line(x1,y0,x0,y1, width=2, fill=bot.color)