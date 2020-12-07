from Gui import Gui
from OldModel import Model
import tkinter as tk
from Tracker import detect_and_save

class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = Gui(self.root)

        self.gui.startButton.bind('<ButtonRelease-1>', self.startAlgorithm)

        # Start main loop of the gui
        self.root.mainloop()


    def startAlgorithm(self, event):
        # Get frame offset value (default is 1)
        frameOffset = self.gui.getFrameOffset()
        inputPath = self.gui.getFilePath()
        outputDir = self.gui.getDirectoryPath()

        # Start detection
        if(inputPath and outputDir):
            detect_and_save(inputPath,outputDir,frameOffset)
            # Hide start button
            self.gui.startButton.place_forget()

        


controller = Controller()
