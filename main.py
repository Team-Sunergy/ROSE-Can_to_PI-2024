import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk


# window
mainWin = tk.Tk()
mainWin.title("raspberry pi interface")
mainWin.geometry('800x480')

# place widget for speed window
speedActual = ttk.Label(mainWin, text="inf spd", font=("Helvetica", "65", "bold"), borderwidth=2, relief="raised")
speedActual.place(relx=0.5, rely=0.5, anchor='center')

# right window labels
socLabel = ttk.Label(mainWin, text=" SOC: ", font=("Helvetica", "30"), borderwidth=2, )
motorCurrentInLabel = ttk.Label(mainWin, text=" MOTOR CURRENT IN: ", font=("Helvetica", "15"), borderwidth=2, relief='raised')
motorCurrentOutLabel = ttk.Label(mainWin, text=" ZACH METER: ", font=("Helvetica", "15"),borderwidth=2, relief='raised')
deltaVoltageLabel = ttk.Label(mainWin, text=" ΔV:                       \n\n", font=("Helvetica", "15"), borderwidth=2, relief='raised')
HappinessStatusLabel = ttk.Label(mainWin, text=" HAPPINESS STATUS: HAPPY!!!", font=("Helvetica", "15"), borderwidth=2, relief='raised')

socLabel.place(x=0, y=0)
motorCurrentInLabel.place(x=0, y=400)
motorCurrentOutLabel.place(x=0, y=430)
deltaVoltageLabel.place(x=600, y=395)
HappinessStatusLabel.place(x=250, y=300)


mainWin.mainloop()