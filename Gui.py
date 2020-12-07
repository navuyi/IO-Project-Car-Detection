import tkinter as tk
from tkinter import filedialog
from Settings import *


class Gui:
    def __init__(self, master):
        self.inputDirectoryPath = None
        self.inputFilePath = None
        self.master = master
        master.title("WTV")
        master.resizable(False, False)
        master.geometry(str(WIDTH) + "x" + str(HEIGHT))

        # Create field for user's input video file
            # Label
        self.filePathLabel = tk.Label(master, text="Plik wejściowy", font=(FONT_FAMILY, HEADER_FONT_SIZE, "bold"))
        self.filePathLabel.place(relx=0.5, rely=0.1, anchor='center')
            # Input button
        self.filePathButton = tk.Button(master, text="Select file", command=self.selectFilePath, bg="lightblue")
        self.filePathButton.pack()
        self.filePathButton.place(relx=0.5, rely=0.18, anchor='center', width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
            # Path label
        self.pathLabel1 = tk.Label(master, text="", font=(FONT_FAMILY, FONT_SIZE), wraplength=WIDTH*0.9)
        self.pathLabel1.place(relx=0.5, rely=0.3, anchor='center')

        # Create field for user's result directory PATH
             # Label
        self.dirPathLabel = tk.Label(master, text="Katalog wyjściowy", font=(FONT_FAMILY, HEADER_FONT_SIZE, "bold"))
        self.dirPathLabel.place(relx=0.5, rely=0.4, anchor='center')
            # Input button
        self.dirPathButton = tk.Button(master, text="Select directory", command=self.selectDirectoryPath, bg="lightblue")
        self.dirPathButton.pack()
        self.dirPathButton.place(relx=0.5, rely=0.48, anchor='center' , width=BUTTON_WIDTH+20, height=BUTTON_HEIGHT)
            # Path label
        self.pathLabel2 = tk.Label(master, text="", font=(FONT_FAMILY, FONT_SIZE), wraplength=WIDTH*0.9)
        self.pathLabel2.place(relx=0.5, rely=0.60, anchor='center')


        # Create frame offset label
        self.frameOffsetLabel = tk.Label(master, text="Frame Offset", font=(FONT_FAMILY, HEADER_FONT_SIZE-5, "bold"))
        self.frameOffsetLabel.place(relx=0.3, rely=0.70, anchor='center')

        # Create frame offset selector
        self.frameOffset = tk.IntVar()
        self.frameOffset.set(1) # default value is 1 
        self.selector = tk.OptionMenu(master, self.frameOffset, 1, 2, 4, 6)
        self.selector.config(bg="lightblue", font=(FONT_FAMILY, 10, "bold"))
        self.selector.place(relx=0.3, rely=0.75, anchor='center', width=75, height=25)

        # Create On The Fly Label
        self.otfLabel = tk.Label(master, text="Show progress", font=(FONT_FAMILY, HEADER_FONT_SIZE-5, "bold"))
        self.otfLabel.place(relx=0.7, rely=0.70, anchor='center')

        # Create On The Fly checkbox
        self.otfValue = tk.IntVar()
        self.otfValue.set(0) # default value is 0 --> progress is not shown
        self.otfCheckbox = tk.Checkbutton(master, text=None, variable=self.otfValue)
        self.otfCheckbox.place(relx=0.7, rely=0.75, anchor='center', width=75, height=25)

        # Create START button
        self.startButton = tk.Button(master, text="DETECT", font=(FONT_FAMILY, HEADER_FONT_SIZE, "bold"), bg="steelblue")
        self.startButton.pack()
        self.startButton.place(relx=0.5, rely=0.9, anchor='center', width = 100, height=35)

        # Create PLAY button --> plays last computed detection video
        self.playButton = tk.Button(master, text="PLAY", font=(FONT_FAMILY, HEADER_FONT_SIZE, "bold"), bg="steelblue")
        self.playButton.pack()
        self.playButton.place(relx=0.7, rely=0.9, anchor='center', width = 100, height=35)
        self.playButton.place_forget()
        # Button will be set to visible after first detection cycle

    def selectFilePath(self):
        self.inputFilePath = tk.filedialog.askopenfilename(initialdir="./", title="Select a File", filetypes=(("any file", "*.*"), ("avi files", "*.avi"), ("mp4 files", "*.mp4")))
        self.pathLabel1['text'] = str(self.inputFilePath)

    def selectDirectoryPath(self):
        self.inputDirectoryPath = tk.filedialog.askdirectory(initialdir="./", title="Select directory")
        self.pathLabel2['text'] = str(self.inputDirectoryPath)

    def getDirectoryPath(self):
        return self.inputDirectoryPath

    def getFilePath(self):
        return self.inputFilePath

    def getFrameOffset(self):
        return self.frameOffset.get()

    def getOTFValue(self):
        return self.otfValue.get()
