from math import sqrt, inf
from heapq import heapify, heappush, heappop

class Robot:
    def __init__(self, name, pos, goal, h, grid, color="black"):
        self.name = name
        self.pos = pos
        self.goal = goal
        self.color = color
        self.path = []
        self.setHMeasure(h)
        self.atGoal = False
        self.grid = grid

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
        return self.euclid(pos, self.goal)

    def euclid(pos1, pos2):
        return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    #TODO Method to find path (should be able to run again)
    def reconstructPath(self, cameFrom, current):
        totalPath = [current]
        while current in cameFrom.keys():
            current = cameFrom[current]
            totalPath.insert(0, current)
        return totalPath

    def A_star(self):
        cameFrom = {}
        gscore = {}
        gscore[self.pos] = 0
        fscore = {}
        fscore[self.pos] = self.hMeasure(self.pos)
        openSet = []
        heapify(openSet)
        heappush(openSet, (fscore[self.pos], self.pos))

        while len(openSet) != 0:
            current = heappop(openSet)[1]
            if current == self.goal:
                self.path = self.reconstructPath(cameFrom, current)
                return True
            for neighbour in self.grid.getNeighbours(current):
                tempGScore = gscore.get(current, inf) + self.euclid(current, neighbour)
                if tempGScore < gscore.get(neighbour, inf):
                    cameFrom[neighbour] = current
                    gscore[neighbour] = tempGScore
                    fscore[neighbour] = gscore[neighbour] + self.hMeasure(neighbour)
                    if (fscore[neighbour], neighbour) not in openSet:
                        heappush(openSet, (fscore[neighbour], neighbour))
        return False
            
    #TODO Method to move position
