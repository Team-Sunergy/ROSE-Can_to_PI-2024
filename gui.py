import tkinter as tk
from tkinter import ttk

# window
mainWin = tk.Tk()
mainWin.title("raspberry pi interface")
mainWin.geometry('500x500')

# configures columns
mainWin.columnconfigure(0, weight=1)
mainWin.columnconfigure(1, weight=1)
mainWin.rowconfigure(0, weight=1)


# configure left window
leftWindow = ttk.Frame(mainWin, borderwidth=10, relief='solid')
leftWindow.columnconfigure(0, weight=1)
leftWindow.columnconfigure(1, weight=10)
leftWindow.columnconfigure(2, weight=1)
leftWindow.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
leftWindow.grid_propagate(False) # makes it so grid doesnt expand based on labels inside

rightWindow = ttk.Frame(mainWin, borderwidth=10, relief='solid')
rightWindow.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
rightWindow.grid_propagate(False)

# place widgets
rightWindow.grid(row=0, column=1, sticky='nsew')
leftWindow.grid(row=0, column=0, sticky='nsew')

# place widget in left window
speedCarLabel = ttk.Label(leftWindow, text="SPEED OF CAR")
speedCarLabel.grid(row=4, column=1, sticky='s')
speedActual = ttk.Label(leftWindow, text="35mph", font=("Arial", 45))
speedActual.grid(row=5, column=1, sticky='n')

# right window labels
label1 = ttk.Label(rightWindow, text="text1: ")
label2 = ttk.Label(rightWindow, text="text2: ")
label3 = ttk.Label(rightWindow, text="text3: ")
label4 = ttk.Label(rightWindow, text="text4: ")
label5 = ttk.Label(rightWindow, text="text5: ")

label1.grid(row=2)
label2.grid(row=3)
label3.grid(row=4)
label4.grid(row=5)
label5.grid(row=6)













mainWin.mainloop()