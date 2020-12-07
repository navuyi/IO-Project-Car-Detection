from Gui import Gui
from OldModel import Model
import tkinter as tk
from Tracker import detect_and_save
from tkinter import messagebox
from Settings import WIDTH, HEIGHT
import time
from os import startfile

class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = Gui(self.root)

        self.gui.startButton.bind('<ButtonRelease-1>', self.startAlgorithm)
        self.gui.playButton.bind('<ButtonRelease-1>', self.playLastOutput)
        self.outputVideoPath = None

        # Center gui on the screen
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        w = WIDTH
        h = HEIGHT

        # calculate position x, y
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Start main loop of the gui
        self.root.mainloop()

    def startAlgorithm(self, event):
        # Get frame offset value (default is 1)
        frameOffset = self.gui.getFrameOffset()
        # Get input video path
        inputPath = self.gui.getFilePath()
        inputPath = "./src/video_input/GrupaC1_cut2.mp4"
        # Get output directory path
        outputDir = self.gui.getDirectoryPath()
        outputDir = "./results"
        # Get On The Fly decision (default is 0-->None) and parse it to boolean
        otfValue = self.gui.getOTFValue()
        if(otfValue==1):
            otfValue = True
        else:
            otfValue = False

        # Check if input and output paths are selected
        if inputPath and outputDir:
            # Check input file format
            if(inputPath.endswith(('.mp4', '.avi', '.mov', '.wmv','.mpg', '.mpeg', '.flv'))):
                # Hide main menu
                self.root.withdraw()
                # Start detection
                self.outputVideoPath = detect_and_save(inputPath,outputDir,frameOffset, otfValue)
                # Bring back main menu after detection is done 
                    # Changes in START and PLAY buttons layout
                self.gui.startButton.place(relx=0.3, rely=0.9, anchor='center', width = 100, height=35)
                self.gui.playButton.place(relx=0.7, rely=0.9, anchor='center', width = 100, height=35) 
                self.root.deiconify()
            else:
                messagebox.showwarning("Uwaga", "Wybierz poprawny format pliku wejściowego")
        else:
            messagebox.showwarning("Uwaga", "Wybierz plik wejściowy oraz katalog wyjściowy")
        
    def playLastOutput(self, event):
        # Open last computed output videofile with OS default software
        startfile(self.outputVideoPath)



controller = Controller()
