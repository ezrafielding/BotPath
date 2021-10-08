from math import sqrt, inf
from heapq import heapify, heappush, heappop

class Robot:
    def __init__(self, name, pos, goal, h, grid, color="black"):
        '''
        Constructor for robots
        '''
        self.name = name
        self.pos = pos
        self.goal = goal
        self.color = color
        self.path = []
        self.traveled = []
        self.setHMeasure(h)
        self.atGoal = False
        self.grid = grid
        self.A_star()
        self.waiting = False

    def setHMeasure(self, h):
        '''
        Sets the prfered heuristic function for the robot for later use
        '''
        if h=="manhattan":
            self.hMeasure=self.manhattanH
        elif h=="diagonal":
            self.hMeasure=self.diagonalH
        elif h=="euclid":
            self.hMeasure=self.euclideanH
        else:
            self.hMeasure=None

    def manhattanH(self, pos):
        '''
        Manhattan Distance Heuristic
        '''
        return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])

    def diagonalH(self, pos):
        '''
        Diagonal Distance Heuristic
        '''
        dx = abs(pos[0] - self.goal[0])
        dy = abs(pos[1] - self.goal[1])
        return (dx+dy) + (sqrt(2)-2) * min(dx, dy)

    def euclideanH(self, pos):
        '''
        Euclidian Distance Heuristic
        '''
        return self.euclid(pos, self.goal)

    def euclid(self, pos1, pos2):
        '''
        Calculates general Eucilidian distance
        '''
        return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def reconstructPath(self, cameFrom, current):
        '''
        Builds final path from 'cameFrom' map bassed of the current position
        '''
        totalPath = [current]
        while current in cameFrom.keys():
            current = cameFrom[current]
            # Prepending node to path
            totalPath.insert(0, current)
        return totalPath

    def A_star(self):
        '''
        A* algorithm implementation
        Finds best path by optimising f(n) = g(n) + h(n) for each node
        '''
        # Declaring initial maps and vairables
        cameFrom = {}
        gscore = {}
        gscore[self.pos] = 0
        fscore = {}
        fscore[self.pos] = self.hMeasure(self.pos)
        openSet = []
        # Converting openSet to min-heap so that finding the node with lowest fscore is O(1)
        heapify(openSet)
        heappush(openSet, (fscore[self.pos], self.pos))

        # Loop set to run until all discovered nodes are evaluated
        while len(openSet) != 0:
            # Fetching node with lowest f(n)
            current = heappop(openSet)[1]
            if current == self.goal:
                # Reconstructing path now that goal has been found
                self.path = self.reconstructPath(cameFrom, current)
                self.path.pop(0)
                return True
            # Iterating to evaluate neighbour of current node
            for neighbour in self.grid.getNeighbours(current):
                tempGScore = gscore.get(current, inf) + self.euclid(current, neighbour)
                # Checking if current nod eprovides a better path to neighbour compared to what has been found already
                if tempGScore < gscore.get(neighbour, inf):
                    cameFrom[neighbour] = current
                    gscore[neighbour] = tempGScore
                    fscore[neighbour] = gscore[neighbour] + self.hMeasure(neighbour)
                    # Adding neighbours to set of discovered nodes
                    if (fscore[neighbour], neighbour) not in openSet:
                        heappush(openSet, (fscore[neighbour], neighbour))
        return False    # Returns False if path not found
    
    def move(self):
        '''
        Provides movement logic for each robot
        '''
        # Checking if Goal has been reached first
        if self.pos == self.goal:
            self.atGoal = True
            return True
        # Checking if next position is open for movement to it
        if self.grid.openSpace(self.path[0][0],self.path[0][1]):
            # Tracking path traveled and updating new position
            self.traveled.append(self.pos)
            self.pos = self.path.pop(0)
            self.waiting = False
        # Check if the robot has been waiting
        elif self.waiting:
            # Generates new path if Robot was waiting for more than 1 time unit
            self.A_star()   # New path generated based on current world state
            self.waiting = False
        else:
            # Set if no move could be made because path is blocked
            self.waiting = True
        
