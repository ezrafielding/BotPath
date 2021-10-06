class Robot:
    def __init__(self, name, pos, goal, color="black"):
        #TODO Matrix to hold heuristic data
        #TODO add completion state?
        self.name = name
        self.pos = pos
        self.goal = goal
        self.color = color
        self.path = []

    #TODO Functions to calculate 3 different types of heuristics (See geeksforgeeks A* page)
    #TODO Method to find path (should be able to run again)
    #TODO Method to move position
