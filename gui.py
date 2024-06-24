import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

from mockDataTransfer import *

# window
mainWin = tk.Tk()
mainWin.title("raspberry pi interface")
mainWin.geometry('800x480')

# configures columns
mainWin.columnconfigure(0, weight=1)
mainWin.columnconfigure(1, weight=1)
mainWin.rowconfigure(0, weight=1)


# configure left window
leftWindow = tk.Frame(mainWin, borderwidth=5, relief='raised')
leftWindow.columnconfigure(0, weight=1)
leftWindow.columnconfigure(1, weight=10)
leftWindow.columnconfigure(2, weight=1)
leftWindow.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
leftWindow.grid_propagate(False) # makes it so grid doesnt expand based on labels inside

rightWindow = tk.Frame(mainWin, borderwidth=5, relief='raised')
rightWindow.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
rightWindow.grid_propagate(False)

# place widgets
rightWindow.grid(row=0, column=1, sticky='nsew')
leftWindow.grid(row=0, column=0, sticky='nsew')

# place widget in left window
speedCarLabel = ttk.Label(leftWindow, text="SPEED", font=('Helvetica', '10', 'bold italic'))
speedCarLabel.grid(row=4, column=1, sticky='s')
speedActual = ttk.Label(leftWindow, text="", font=("Helvetica", "65", "bold"), borderwidth=30, relief="raised")
speedActual.grid(row=5, column=1, sticky='n')

# right window labels
label1 = ttk.Label(rightWindow, text=" text1: ", borderwidth=5, relief='raised')
label2 = ttk.Label(rightWindow, text=" text2: ", borderwidth=5, relief='raised')
label3 = ttk.Label(rightWindow, text=" text3: ", borderwidth=5, relief='raised')
label4 = ttk.Label(rightWindow, text=" text4: ", borderwidth=5, relief='raised')
label5 = ttk.Label(rightWindow, text=" text5: ", borderwidth=5, relief='raised')

label1.grid(row=2)
label2.grid(row=3)
label3.grid(row=4)
label4.grid(row=5)
label5.grid(row=6)

def startGui(data: dict):
    "starts the gui loop given data"
    update_label(data)
    mainWin.mainloop()
    
def update_label(data: dict):
        if data is not None:
            # update speed with speed
            speedActual.config(text=str(data['Speed']))
            mainWin.after(100, update_label)