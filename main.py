import tkinter as tk
import grid
import json
import sys

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

if __name__=="__main__":
    settings = readSettings()

    gridSize = settings["gridSize"]
    worldGrid = grid.Grid((gridSize["x"],gridSize["y"]), obst=settings["obstacles"])

    mainWindow = tk.Tk()
    worldGrid.makeGrid(mainWindow)
    worldGrid.updateGrid()

    mainWindow.mainloop()