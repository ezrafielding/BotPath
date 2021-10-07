from math import sqrt

class Robot:
    def __init__(self, name, pos, goal, h, color="black"):
        #TODO Matrix to hold heuristic data
        #TODO add completion state?
        self.name = name
        self.pos = pos
        self.goal = goal
        self.color = color
        self.path = []
        self.setHMeasure(h)
        self.hValues = self.makeHMatrix()

    def setHMeasure(self, h):
        if h=="manhattan":
            self.hMeasure=self.manhattanH
        elif h=="diagonal":
            self.hMeasure=self.diagonalH
        elif h=="euclid":
            self.hMeasure=self.euclideanH
        else:
            self.hMeasure=None

    def manhattanH(self, pos):
        return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])

    def diagonalH(self, pos):
        dx = abs(pos[0] - self.goal[0])
        dy = abs(pos[1] - self.goal[1])
        return (dx+dy) + (sqrt(2)-2) * min(dx, dy)

    def euclideanH(self, pos):
        return sqrt((pos[0] - self.goal[0])**2 + (pos[1] - self.goal[1])**2)

    def makeHMatrix(self, gridDim, gridInfo):
        rows = []
        for i in range(gridDim[0]):
            rows.append([])
            for j in range(gridDim[1]):
                if gridInfo[i][j] == 0:
                    rows[i].append(-1)
                else:
                    rows[i].append(self.hMeasure((i,j)))
    #TODO Method to find path (should be able to run again)
    #TODO Method to move position
