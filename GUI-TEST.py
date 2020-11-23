from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

from Settings import *
window = Tk()
window.title("WTV")
window.resizable(False, False)
window.geometry(str(WIDTH) + "x" + str(HEIGHT))

def selectEntryFile():
    entryFilename = filedialog.askopenfilename(initialdir = "/", title="Select a File", filetypes = (("any file", "*.*"), ("avi files", "*.avi"), ("mp4 files", "*.mp4")))
    filePathLabel['text'] = str(entryFilename)

def selectResultDirectory():
    resultDir = filedialog.askdirectory(initialdir = "/", title="Select result directory")
    dirPathLabel['text'] = str(resultDir)

# Entry file label and path
    # Label
entryFileLabel = Label(window, text="Plik wejściowy", font=("Consolas", 14, "bold"))
entryFileLabel.place(relx = 0.5, rely=0.1 , anchor='center')
    # Get Path
entryFileButton = Button(window, text="Select file", command=selectEntryFile)
entryFileButton.pack()
entryFileButton.place(relx = 0.5, rely = 0.17, anchor = 'center')
    # Result label
filePathLabel = Label(window, text="", font=("Consolas", 10))
filePathLabel.place(relx = 0.5, rely = 0.24, anchor='center', width=WIDTH*0.9)

# Result files directory(in this directory 2 files will be created: .txt log file and video file with extension same  as the entry file)
    # Label
resultDirectory = Label(window, text="Katalog wynikowy", font=("Consolas", 14, "bold"))
resultDirectory.place(relx = 0.5, rely=0.4 , anchor='center')
    # Get Path
resultDirButton = Button(window, text="Select file", command=selectResultDirectory)
resultDirButton.pack()
resultDirButton.place(relx = 0.5, rely = 0.47, anchor = 'center')
    # Result label
dirPathLabel = Label(window, text="", font=("Consolas", 10))
dirPathLabel.place(relx = 0.5, rely = 0.54, anchor='center')


# Start program button
startButton = Button(window, text="START")
#startButton.pack()
startButton.place(relx = 0.5, rely = 0.9, anchor='center')

window.mainloop()






