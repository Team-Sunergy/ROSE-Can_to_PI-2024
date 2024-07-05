# import tkinter as tk
# import tkinter.font as tkFont
# from tkinter import ttk, Canvas
# import speedometer

# # window
# mainWin = tk.Tk()
# mainWin.title("raspberry pi interface")
# mainWin.geometry('800x480')

# # place widget for speed window
# speedActual = ttk.Label(mainWin, text="inf spd", font=("Helvetica", "65", "bold"), borderwidth=2, relief="raised")
# speedActual.place(relx=0.5, rely=0.5, anchor='center')

# # #speedometer
# # speedometerMeter=Canvas(mainWin,height=500,width=500)
# # speedometerMeter.place(relx=0.5, rely=0.5, anchor='center')
# # speedometerMeter.create_oval(0,0,500,500,tag="oval", fill='white')
# # A=speedometer.Speedometer(speedometerMeter,"oval",Range=(-500,1000))
# # A.moveto(-500,"oval")
# # A.changerange(Range=(0,20),rfont=("Verdana",9))

# # right window labels
# socLabel = ttk.Label(mainWin, text=" SOC: ", font=("Helvetica", "30"), borderwidth=2, )
# motorCurrentInLabel = ttk.Label(mainWin, text=" MOTOR CURRENT IN: ", font=("Helvetica", "15"), borderwidth=2, relief='raised')
# motorCurrentOutLabel = ttk.Label(mainWin, text=" ZACH METER: ", font=("Helvetica", "15"),borderwidth=2, relief='raised')
# deltaVoltageLabel = ttk.Label(mainWin, text=" ΔV:                       \n\n", font=("Helvetica", "15"), borderwidth=2, relief='raised')
# HappinessStatusLabel = ttk.Label(mainWin, text=" HAPPINESS STATUS: HAPPY!!!", font=("Helvetica", "15"), borderwidth=2, relief='raised')

# socLabel.place(x=0, y=0)
# motorCurrentInLabel.place(x=0, y=400)
# motorCurrentOutLabel.place(x=0, y=430)
# deltaVoltageLabel.place(x=600, y=395)
# HappinessStatusLabel.place(x=250, y=300)


# mainWin.mainloop()

from tkinter import Tk, Frame, Label
from tkinter.font import Font
from PIL import Image, ImageTk

# definition of main window
root = Tk()
root.title("GUI for Driver Interface")
root.geometry('800x480')

mainWin = Frame(root, bg='#E5E5E5')
mainWin.pack(fill='both', expand=True)

secondWin = Frame(mainWin, bg='white')
secondWin.place(relx=0.0, rely=0.095, relwidth=1, relheight=0.905)

versionLabel = Label(mainWin, text="version 0.2", font=('Gotham', 10), background="#E5E5E5")
versionLabel.place(relx=0.99, rely=0.015, anchor='ne')

# Fonts
dashFont = Font(family='Gotham', weight='bold', size=30)
socFont = Font(family='Gotham', weight='bold', size=10)
speedFont = Font(family='Gotham', weight='bold', size=200)
errorFont = Font(family='Gotham', size=7)
errorFont2 = Font(family='Gotham', size=8)

speedometerNum = Label(secondWin, text="25", font=speedFont, bg="white")
speedometerNum.place(relx=0.5, rely=0.45, anchor='center')

# define SOC frame (top left)
socFrame = Frame(secondWin, bg='#E5E5E5', relief='raised', borderwidth=1)
socFrame.place(x=5, y=5, width=200, height=100)

socLabel = Label(socFrame, text='STATE OF CHARGE', font=socFont, background='#E5E5E5',)
socLabel.place(relx=0.5, rely=0.01, anchor='n')

socVal = Label(socFrame, text='95.5%', font=dashFont, background='#E5E5E5',)
socVal.place(relx=0.5, rely=0.5, anchor='center')

# define AMPS frame
ampsInFrame = Frame(master=secondWin,
                                  width=200,
                                  height=100,
                                  background='#E5E5E5',
                                  borderwidth=1,
                                  relief='raised',
                                  )
ampsInLabel = Label(master=ampsInFrame,
                                text='AMPERAGE IN',
                                font=socFont,
                                foreground='black',
                                background='#E5E5E5',
                                )
ampsInValue = Label(master=ampsInFrame,
                                     text='3.2AMPS',
                                     font=dashFont,
                                     foreground='black',
                                     background='#E5E5E5',
                                     )
ampsInLabel.place(relx=0.5, rely=0.01, anchor='n')
ampsInValue.place(relx=0.5, rely=0.5, anchor='center')
ampsInFrame.place(x=5,y=428,anchor='sw')



ampsOutFrame = Frame(master=secondWin,
                                  width=200,
                                  height=100,
                                  background='#E5E5E5',
                                  borderwidth=1,
                                  relief='raised',
                                   )
ampsOutLabel = Label(master=ampsOutFrame,
                                text='AMPERAGE OUT',
                                font=socFont,
                                foreground='black',
                                background='#E5E5E5',
                                )
ampsOutValue = Label(master=ampsOutFrame,
                                     text='1.9AMPS',
                                     font=dashFont,
                                     foreground='black',
                                     background='#E5E5E5',
                                     )
ampsOutValue.place(relx=0.5, rely=0.5, anchor='center')
ampsOutLabel.place(relx=0.5, rely=0.01, anchor='n')
ampsOutFrame.place(x=795,y=428,anchor='se')

ampsDiffFrame = Frame(master=secondWin,
                                    width=300,
                                    height=75,
                                    background='#E5E5E5',
                                    borderwidth=1,
                                    relief='raised',
                                    )
ampsDiffValue = Label(master=ampsDiffFrame,
                                     text='1.3A',
                                     font=Font(family='Gotham', weight='bold', size=25),
                                     foreground='black',
                                     background='#E5E5E5',
                                     )
ampsDiffLabel = Label(master=ampsDiffFrame,
                                     text='AMP IN/AMP OUT',
                                     font=socFont,
                                     foreground='black',
                                     background='#E5E5E5',
                                    )
ampsDiffValue.place(relx=0.5, rely=0.53, anchor='center')
ampsDiffLabel.place(relx=0.5, rely=0.02,anchor='n')
ampsDiffFrame.place(x=400,y=428,anchor='s')


# BELOW ARE ALL THE ANNOYING ERROR FRAME DIAGNOSTICS
errorFrame = Frame(master=secondWin,
                                  width=200,
                                  height=175,
                                  background='#E5E5E5',
                                  borderwidth=1,
                                  relief='raised'
                                  )
errorFrameLabel = Label(master=errorFrame,
                                         text="MPPTS Status",
                                         font=errorFont2,
                                         foreground='black',
                                         background='#E5E5E5',
                                         )
mpptsErrorLabel = Label(master=errorFrame,
                                    text="mppt0 mppt1",
                                    font=errorFont2,
                                    background='#E5E5E5',
                                    foreground='black')


mpptHWOverCurrentLabel = Label(master=errorFrame,
                                                 text="mpptHWOverCurrent:",
                                                 font=errorFont,
                                                 foreground='black',
                                                 background='#E5E5E5',
                                                 anchor='w',)
mppt0HWOverCurrent = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt1HWOverCurrent = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)

mpptHWOverVoltageLabel = Label(master=errorFrame,
                                                 text="mpptHWOverVoltage:",
                                                 font=errorFont,
                                                 foreground='black',
                                                 background='#E5E5E5',
                                                 anchor='w')
mppt0HWOverVoltage = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt1HWOverVoltage = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)

mppt12VUnderVoltageLabel = Label(master=errorFrame,
                                                   text="mppt12VUnderVoltage:",
                                                   font=errorFont,
                                                   foreground='black',
                                                   background='#E5E5E5',
                                                   anchor='w')
mppt012VUnderVoltage = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt112VUnderVoltage = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)

mpptBatteryFullLabel = Label(master=errorFrame,
                                               text="mpptBatteryFull:",
                                               font=errorFont,
                                               foreground='black',
                                               background='#E5E5E5',
                                               anchor='w')
mppt0BatteryFull = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt1BatteryFull = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)

mpptBatteryLowLabel = Label(master=errorFrame,
                                              text="mpptBatteryLow:",
                                              font=errorFont,
                                              foreground='black',
                                              background='#E5E5E5',
                                              anchor='w')
mppt0BatteryLow = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt1BatteryLow = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)

mpptMosfetOverheatLabel = Label(master=errorFrame,
                                                  text="mpptMosfetOverheat:",
                                                  font=errorFont,
                                                  foreground='black',
                                                  background='#E5E5E5',
                                                  anchor='w')
mppt0MosfetOverheat = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt1MosfetOverheat = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)

mpptLowArrayPowerLabel = Label(master=errorFrame,
                                         text="mpptLowArrayPower:",
                                         font=errorFont,
                                         foreground='black',
                                         background='#E5E5E5',
                                         anchor='w')
mppt0LowArrayPower = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)
mppt1LowArrayPower = Label(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            foreground='green',
                                            background='#E5E5E5',
                                            anchor='w',)


# placing error labels
errorFrameLabel.place(relx=0.03, rely=0.006, anchor='nw')
mpptsErrorLabel.place(relx=0.59, rely=0.006, anchor='nw')

mpptLowArrayPowerLabel.place(relx=0.03, rely=0.22, anchor='w')
mppt0LowArrayPower.place(relx=0.6, rely=0.22, anchor='w')
mppt1LowArrayPower.place(relx=0.8, rely=0.22, anchor='w')

mpptMosfetOverheatLabel.place(relx=0.03, rely=0.34, anchor='w')
mppt0MosfetOverheat.place(relx=0.6, rely=0.34, anchor='w')
mppt1MosfetOverheat.place(relx=0.8, rely=0.34, anchor='w')

mpptBatteryLowLabel.place(relx=0.03, rely=0.4532, anchor='w')
mppt0BatteryLow.place(relx=0.6, rely=0.4532, anchor='w')
mppt1BatteryLow.place(relx=0.8, rely=0.4532, anchor='w')

mpptBatteryFullLabel.place(relx=0.03, rely=0.5648, anchor='w')
mppt0BatteryFull.place(relx=0.6, rely=0.5648, anchor='w')
mppt1BatteryFull.place(relx=0.8, rely=0.5648, anchor='w')

mppt12VUnderVoltageLabel.place(relx=0.03, rely=0.6864, anchor='w')
mppt012VUnderVoltage.place(relx=0.6, rely=0.6864, anchor='w')
mppt112VUnderVoltage.place(relx=0.8, rely=0.6864, anchor='w')

mpptHWOverVoltageLabel.place(relx=0.03, rely=0.798, anchor='w')
mppt0HWOverVoltage.place(relx=0.6, rely=0.798, anchor='w')
mppt1HWOverVoltage.place(relx=0.8, rely=0.798, anchor='w')

mpptHWOverCurrentLabel.place(relx=0.03, rely=0.90, anchor='w')
mppt0HWOverCurrent.place(relx=0.6, rely= 0.90, anchor='w')
mppt1HWOverCurrent.place(relx=0.8, rely=0.90, anchor='w')



# place on frame
errorFrame.place(x=795,y=5,anchor='ne')


img = Image.open('Logo.png')
img = img.resize((84, 37))
sunergyLogo = ImageTk.PhotoImage(img)
logoLabel = Label(mainWin, image=sunergyLogo, background='#E5E5E5')
logoLabel.image = sunergyLogo  
logoLabel.place(x=400, y=0, anchor='n')
root.mainloop()
