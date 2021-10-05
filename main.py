import tkinter as tk
import grid

if __name__=="__main__":
    worldGrid = grid.Grid((6,6))
    mainWindow = tk.Tk()

    worldGrid.makeGrid(mainWindow)
    worldGrid.updateGrid()

    mainWindow.mainloop()