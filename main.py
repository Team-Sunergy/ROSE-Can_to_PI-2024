import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import queue
import threading
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
rightWindow.columnconfigure(0, weight=1)
rightWindow.columnconfigure(1, weight=1)
rightWindow.columnconfigure(2, weight=1)
rightWindow.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
rightWindow.grid_propagate(False)

# place widgets
rightWindow.grid(row=0, column=1, sticky='nsew')
leftWindow.grid(row=0, column=0, sticky='nsew')

# place widget in left window
speedCarLabel = ttk.Label(leftWindow, text="SPEED", font=('Helvetica', '10'))
speedCarLabel.grid(row=4, column=1, sticky='s')
speedActual = ttk.Label(leftWindow, text="inf spd", font=("Helvetica", "65", "bold"), borderwidth=2, relief="raised")
speedActual.grid(row=5, column=1, sticky='n')

# right window labels
socLabel = ttk.Label(rightWindow, text=" SOC ", font=("Helvetica", "15"), borderwidth=2, relief='raised')
motorCurrentInLabel = ttk.Label(rightWindow, text=" MOTOR CURRENT IN: ", font=("Helvetica", "15"), borderwidth=2, relief='raised')
motorCurrentOutLabel = ttk.Label(rightWindow, text=" ZACH METER: ", font=("Helvetica", "15"),borderwidth=2, relief='raised')
deltaVoltageLabel = ttk.Label(rightWindow, text=" DELTA VOLTAGE: ", font=("Helvetica", "15"), borderwidth=2, relief='raised')
HappinessStatusLabel = ttk.Label(rightWindow, text=" HAPPINESS STATUS: HAPPY!!!", font=("Helvetica", "15"), borderwidth=2, relief='raised')

socLabel.grid(row=2, column=0, sticky='w')
motorCurrentInLabel.grid(row=3, column=0, sticky='w')
motorCurrentOutLabel.grid(row=4, column=0, sticky='w')
deltaVoltageLabel.grid(row=5, column=0, sticky='w')
HappinessStatusLabel.grid(row=6, column=0, sticky='w')


mainWin.mainloop()