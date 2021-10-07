from tkinter import Canvas

class Grid:

    def __init__(self, dim, scale, obst=[], bots=[]):
        self.dim = dim
        self.bots = bots
        self.botTotal = len(bots)
        self.botsComplete = 0
        self.obst = obst
        self.scale = scale
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

    def openSpace(self, x, y, includeGoals=True):
        if includeGoals:
            openCheck = self.gridInfo[x][y] == -1 or self.gridInfo[x][y]==2
        else:
            openCheck = self.gridInfo[x][y] == -1
        if openCheck:
            return True
        return False

    def makeGrid(self, window):
        self.canvas = Canvas(window, width=(self.dim[0]*self.scale), height=(self.dim[1]*self.scale))
        self.canvas.pack()

    def appendBot(self, bot):
        self.bots.append(bot)
        self.botTotal = len(self.bots)
        self.updateGridInfo(bot.pos[0], bot.pos[1], 1)
        self.updateGridInfo(bot.goal[0], bot.goal[1], 2)

    def getNeighbours(self, pos):
        neigbours = []
        for i in range(-1,2):
            for j in range(-1,2):
                lowerCheck = pos[0]+i>=0 and pos[1]+j>=0
                upperCheck = pos[0]+i<self.dim[0] and pos[1]+j<self.dim[1]
                if lowerCheck and upperCheck and self.openSpace(pos[0]+i, pos[1]+j):
                    neigbours.append((pos[0]+i, pos[1]+j))
        return neigbours

    def updateGrid(self, init=False):
        if init:
            for j in range(self.dim[1]):
                augJ = (j*self.scale)
                for i in range(self.dim[0]):
                    augI = (i*self.scale)
                    if self.gridInfo[i][j]==0:
                        self.canvas.create_rectangle(augI, augJ, augI+self.scale, augJ+self.scale, fill="black")
                    else:
                        self.canvas.create_rectangle(augI, augJ, augI+self.scale, augJ+self.scale)
        
            for bot in self.bots:
                goal = bot.goal
                x0 = (goal[0]*self.scale)
                x1 = (goal[0]*self.scale)+self.scale
                y0 = (goal[1]*self.scale)
                y1 = (goal[1]*self.scale)+self.scale
                self.canvas.create_line(x0,y0,x1,y1, width=2, fill=bot.color)
                self.canvas.create_line(x1,y0,x0,y1, width=2, fill=bot.color)
        
        self.canvas.delete("robots")
        for bot in self.bots:
            pos = bot.pos
            x0 = (pos[0]*self.scale)+0.2*self.scale
            x1 = (pos[0]*self.scale)+0.8*self.scale
            y0 = (pos[1]*self.scale)+0.2*self.scale
            y1 = (pos[1]*self.scale)+0.8*self.scale
            self.canvas.create_oval(x0,y0,x1,y1, fill=bot.color, tags="robots")

            traveled = bot.traveled
            traveled.append(bot.pos)
            for i,tpos in enumerate(traveled):
                x0 = (tpos[0]*self.scale)+self.scale/2
                y0 = (tpos[1]*self.scale)+self.scale/2
                if i==0:
                    x1,y1=x0,y0
                else:
                    x1 = (traveled[i-1][0]*self.scale)+self.scale/2
                    y1 = (traveled[i-1][1]*self.scale)+self.scale/2
                self.canvas.create_line(x0,y0,x1,y1, width=2, fill=bot.color, tags="robots")


    def run(self, window):
        if self.botsComplete < self.botTotal:
            self.botsComplete=0
            print("tick")
            for bot in self.bots:
                self.updateGridInfo(bot.pos[0], bot.pos[1], -1)
                bot.move()
                if bot.atGoal:
                    self.botsComplete += 1
                if self.openSpace(bot.pos[0], bot.pos[1]):
                    self.updateGridInfo(bot.pos[0], bot.pos[1], 1)
                else:
                    self.updateGridInfo(bot.pos[0], bot.pos[1], 3)
            self.updateGrid()
            window.update()
            return True
        else:
            return False