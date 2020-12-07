from Gui import Gui
import tkinter as tk
from Detector import detect_and_save
from tkinter import messagebox
from tkinter.ttk import Progressbar
from os import startfile
from Settings import *


class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = Gui(self.root)
        self.stop = False

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
        # Get output directory path
        outputDir = self.gui.getDirectoryPath()
        # Get On The Fly decision (default is 0-->None) and parse it to boolean
        otfValue = self.gui.getOTFValue()
        if (otfValue == 1):
            otfValue = True
        else:
            otfValue = False

        # Check if input and output paths are selected
        if inputPath and outputDir:
            # Check input file format
            if inputPath.endswith(('.mp4', '.avi', '.mov', '.wmv', '.mpg', '.mpeg', '.flv')):
                # Hide main menu
                self.root.withdraw()
                # Show progress bar
                self.popup = tk.Toplevel()
                # Center gui on the screen
                ws = self.popup.winfo_screenwidth()
                hs = self.popup.winfo_screenheight()
                w = 400
                h = 100
                # calculate position x, y
                x = (ws / 2) - (w / 2)
                y = (hs / 2) - (h / 2)
                self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
                self.popup.title("Progress")
                self.popup.protocol("WM_DELETE_WINDOW", lambda: self.restart() if messagebox.askokcancel(
                    "Quit", "Do you want to quit?") else False)
                progress = tk.DoubleVar()
                label = tk.Label(self.popup, text="Detection in progress...", font=(FONT_FAMILY, HEADER_FONT_SIZE - 5, "bold"))
                label.place(relx=0.5, rely=0.4, anchor='center')
                progressBar = Progressbar(self.popup, variable=progress, maximum=100, orient="horizontal", length=200,
                                          mode="determinate")
                progressBar.place(relx=0.5, rely=0.6, anchor='center')

                # Start detection
                outputPath = ""
                for result, outputPath in detect_and_save(inputPath, outputDir, frameOffset, otfValue):
                    if self.stop:
                        break
                    progress.set(result)
                    self.popup.update()
                # Close progress bar
                self.popup.withdraw()
                # Save output path
                self.outputVideoPath = outputPath

                # Bring back main menu after detection is done 
                # Changes in START and PLAY buttons layout
                self.gui.startButton.place(relx=0.3, rely=0.9, anchor='center', width=100, height=35)
                self.gui.playButton.place(relx=0.7, rely=0.9, anchor='center', width=100, height=35)
                self.gui.finishLabel.place(relx=0.5, rely=0.8, anchor='center')
                self.root.deiconify()

            else:
                messagebox.showwarning("Error", "Invalid format")
        else:
            messagebox.showwarning("Error", "Choose input file and output directory")

    def playLastOutput(self, event):
        # Open last computed output videofile with OS default software
        startfile(self.outputVideoPath)

    def restart(self):
        self.popup.destroy()
        self.root.destroy()
        self.stop
        self = Controller()


if __name__ == '__main__':
    controller = Controller()
