from Gui import Gui
from OldModel import Model
import tkinter as tk
from Tracker import detect_and_save
from tkinter import messagebox
from Settings import WIDTH, HEIGHT

class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = Gui(self.root)

        self.gui.startButton.bind('<ButtonRelease-1>', self.startAlgorithm)

        # Center gui on the screen
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        w = WIDTH
        h = HEIGHT
        
        # calculate position x, y
        x = (ws/2) - (w/2)    
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Start main loop of the gui
        self.root.mainloop()


    def startAlgorithm(self, event):
        # Get frame offset value (default is 1)
        frameOffset = self.gui.getFrameOffset()
        inputPath = self.gui.getFilePath()
        outputDir = self.gui.getDirectoryPath()

        # Check if input and output paths are selected
        if(inputPath and outputDir):
            # Check input file format
            if(inputPath.endswith(('.mp4', '.avi', '.mov', '.wmv','.mpg', '.mpeg', '.flv'))):
                # Start detection
                detect_and_save(inputPath,outputDir,frameOffset)
                # Hide start button AND SHOW PROGRESS BAR OR SOMETHING XD
                self.gui.startButton.place_forget()
            else:
                messagebox.showwarning("Uwaga", "Wybierz poprawny format pliku wejściowego")
                
        else:
            messagebox.showwarning("Uwaga", "Wybierz plik wejściowy oraz katalog wyjściowy")
        


controller = Controller()
