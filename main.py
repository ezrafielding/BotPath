import tkinter as tk
import grid
import robot
import json
import sys
import random
import time

def readSettings():
    try:
        with open(sys.argv[1]) as f:
            return json.load(f)
    except IndexError:
        print("Missing arg: Configuration File")
        exit()
    except FileNotFoundError:
        print("Configuration file not found!")
        exit()

def rndPos(world, ux, lx, uy, ly):
    check = False
    while not check:
        x = random.randint(lx,ux)
        y = random.randint(ly,uy)
        check = world.openSpace(x,y,includeGoals=False)
    return x,y

def spawnBots(world, robots):
    for bot in robots:
        if bot.get("position") == None:
            posx,posy = rndPos(world, world.dim[0]-1, 0, world.dim[1]-1, 0)
        else:
            posx = bot["position"]["x"]
            posy = bot["position"]["y"]
        if bot.get("goal") == None:
            sameCheck = True
            while sameCheck:
                goalx,goaly = rndPos(world, world.dim[0]-1, 0, world.dim[1]-1, 0)
                if (posx,posy) != (goalx,goaly):
                    sameCheck = False
        else:
            goalx = bot["goal"]["x"]
            goaly = bot["goal"]["y"]

        world.appendBot(robot.Robot(
            name=bot.get("name"),
            pos=(posx,posy),
            goal=(goalx,goaly),
            h=bot.get("heuristic"),
            color=bot.get("color"),
            grid=world
        ))

if __name__=="__main__":
    settings = readSettings()

    gridSize = settings["gridSize"]
    worldGrid = grid.Grid((gridSize["x"],gridSize["y"]), settings["blockSize"], obst=settings["obstacles"])
    spawnBots(worldGrid, settings["robots"])

    mainWindow = tk.Tk()
    worldGrid.makeGrid(mainWindow)
    worldGrid.updateGrid()
    mainWindow.update()
    while worldGrid.run(mainWindow):
        time.sleep(0.5)
    mainWindow.mainloop()