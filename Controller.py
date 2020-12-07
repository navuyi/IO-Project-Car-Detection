from Gui import Gui
from OldModel import Model
import tkinter as tk


class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = Gui(self.root)

        self.gui.startButton.bind('<ButtonRelease-1>', self.startAlgorithm)

        # Start main loop of the gui
        self.root.mainloop()


    def startAlgorithm(self, event):
        # Get frame skip value (default is 1)
        frameSkip = self.gui.getFrameSkip()
        print(frameSkip)
        
        # Create instance of model - calculations
        model = Model(self.gui.getFilePath(), self.gui.getDirectoryPath())

        # Hide start button
        self.gui.startButton.place_forget()

        # Start calculations
        model.detect()


controller = Controller()
