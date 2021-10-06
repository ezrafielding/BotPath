class Robot:
    def __init__(self, name, pos, goal, color="black"):
        self.name = name
        self.pos = pos
        self.goal = goal
        self.color = color
        self.path = []
