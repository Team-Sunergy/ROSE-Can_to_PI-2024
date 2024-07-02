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

from tkinter import *
import customtkinter
import ttkbootstrap as tb
from PIL import Image
from ttkbootstrap import Style



# definition of main window
mainWin = customtkinter.CTk(fg_color='#E5E5E5')
mainWin.title("GUI for Driver Interface")
mainWin.geometry('800x480')
secondWin = customtkinter.CTkFrame(master=mainWin, width=800, height=440, corner_radius=10, fg_color='white')
secondWin.place(relx=0.0,rely=0.095)

versionLabel = Label(master=mainWin,
                                       text="version 0.2",
                                       font=('Gotham', 10),
                                       )
versionLabel.place(relx=0.99, rely=0.015, anchor='ne')


# Fonts
dashFont = customtkinter.CTkFont(family='Gotham', weight='bold', size=35)
socFont = customtkinter.CTkFont(family='Gotham', weight='bold', size=10)
errorFont = customtkinter.CTkFont(family='Gotham', weight='normal', size=8)
errorFont2 = customtkinter.CTkFont(family='Gotham', weight='normal', size=9)




# Speedometer
speedometerFrame = customtkinter.CTkFrame(secondWin,
                                          width=500,
                                          height=500,
                                          fg_color='transparent',
                                          )
speedometerFrame.place(relx=0.5, rely=0.48, anchor='center')

speedometer = tb.Meter(
    master=speedometerFrame,
    metersize=400,
    meterthickness=50,
    padding=0,
    amountused=25,
    metertype="semi",
    textfont="-size 100 -weight bold",
    stripethickness=4,
    subtext="",
    subtextfont="-size 0",
    bootstyle='dark',
    amounttotal=100,    
    interactive=True,
)
speedometer.place(relx=0.5, rely=0.48, anchor='center')
# fecd08 sunergy yellow
# define SOC frame (top left)
socFrame = customtkinter.CTkFrame(master=secondWin,
                                  width=200,
                                  height=100,
                                  corner_radius=5,
                                  fg_color='#E5E5E5',
                                  border_width=1,
                                  border_color='black',
                                  )
socLabel = customtkinter.CTkLabel(master=socFrame,
                                text='STATE OF CHARGE',
                                font=socFont,
                                text_color='black',
                                )
socVal = customtkinter.CTkLabel(master=socFrame,
                                text='95.5%',
                                font=dashFont,
                                text_color='black')
socVal.place(relx=0.5, rely=0.5, anchor='center')
socLabel.place(relx=0.5, rely=0.01, anchor='n')
# place on frame
socFrame.place(x=5,y=5,anchor='nw')


# define AMPS frame
ampsInFrame = customtkinter.CTkFrame(master=secondWin,
                                  width=200,
                                  height=100,
                                  corner_radius=5,
                                  fg_color='#E5E5E5',
                                  border_width=1,
                                  border_color='black',
                                  )
ampsInLabel = customtkinter.CTkLabel(master=ampsInFrame,
                                text='AMPERAGE IN',
                                font=socFont,
                                text_color='black',
                                )
ampsInValue = customtkinter.CTkLabel(master=ampsInFrame,
                                     text='3.2AMPS',
                                     font=dashFont,
                                     text_color='black'
                                     )
ampsInLabel.place(relx=0.5, rely=0.01, anchor='n')
ampsInValue.place(relx=0.5, rely=0.5, anchor='center')
ampsInFrame.place(x=5,y=428,anchor='sw')



ampsOutFrame = customtkinter.CTkFrame(master=secondWin,
                                  width=200,
                                  height=100,
                                  corner_radius=5,
                                  fg_color='#E5E5E5',
                                  border_width=1,
                                  border_color='black',
                                  )
ampsOutLabel = customtkinter.CTkLabel(master=ampsOutFrame,
                                text='AMPERAGE OUT',
                                font=socFont,
                                text_color='black',
                                )
ampsOutValue = customtkinter.CTkLabel(master=ampsOutFrame,
                                     text='1.9AMPS',
                                     font=dashFont,
                                     text_color='black'
                                     )
ampsOutValue.place(relx=0.5, rely=0.5, anchor='center')
ampsOutLabel.place(relx=0.5, rely=0.01, anchor='n')
ampsOutFrame.place(x=795,y=428,anchor='se')

ampsDiffFrame = customtkinter.CTkFrame(master=secondWin,
                                    width=300,
                                    height=75,
                                    corner_radius=5,
                                    fg_color='#E5E5E5',
                                    border_width=1,
                                    border_color='black',
                                    )
ampsDiffLabel = customtkinter.CTkLabel(master=ampsDiffFrame,
                                     text='AMP IN/AMP OUT',
                                     font=socFont,
                                     text_color='black',
                                    )
ampsDiffValue = customtkinter.CTkLabel(master=ampsDiffFrame,
                                     text='1.3A',
                                     font=customtkinter.CTkFont(family='Gotham', weight='bold', size=35),
                                     text_color='black'
                                     )
ampsDiffValue.place(relx=0.5, rely=0.53, anchor='center')
ampsDiffLabel.place(relx=0.5, rely=0.02,anchor='n')
ampsDiffFrame.place(x=400,y=428,anchor='s')


# BELOW ARE ALL THE ANNOYING ERROR FRAME DIAGNOSTICS
errorFrame = customtkinter.CTkFrame(master=secondWin,
                                  width=200,
                                  height=175,
                                  corner_radius=5,
                                  fg_color='#E5E5E5',
                                  border_width=1,
                                  border_color='black',)
errorFrameLabel = customtkinter.CTkLabel(master=errorFrame,
                                         text="MPPTS Status",
                                         font=errorFont2,
                                         text_color='black',
                                         )
mpptsErrorLabel = customtkinter.CTkLabel(master=errorFrame,
                                    text="mppt0 | mppt1",
                                    font=errorFont2,
                                    text_color='black')


mpptHWOverCurrentLabel = customtkinter.CTkLabel(master=errorFrame,
                                                 text="mpptHWOverCurrent:",
                                                 font=errorFont,
                                                 text_color='black',
                                                 anchor='w',)
mppt0HWOverCurrent = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)
mppt1HWOverCurrent = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)

mpptHWOverVoltageLabel = customtkinter.CTkLabel(master=errorFrame,
                                                 text="mpptHWOverVoltage:",
                                                 font=errorFont,
                                                 text_color='black',
                                                 anchor='w')
mppt0HWOverVoltage = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)
mppt1HWOverVoltage = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)

mppt12VUnderVoltageLabel = customtkinter.CTkLabel(master=errorFrame,
                                                   text="mppt12VUnderVoltage:",
                                                   font=errorFont,
                                                   text_color='black',
                                                   anchor='w')
mppt012VUnderVoltage = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)
mppt112VUnderVoltage = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)

mpptBatteryFullLabel = customtkinter.CTkLabel(master=errorFrame,
                                               text="mpptBatteryFull:",
                                               font=errorFont,
                                               text_color='black',
                                               anchor='w')
mppt0BatteryFull = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)
mppt1BatteryFull = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)

mpptBatteryLowLabel = customtkinter.CTkLabel(master=errorFrame,
                                              text="mpptBatteryLow:",
                                              font=errorFont,
                                              text_color='black',
                                              anchor='w')
mppt0BatteryLow = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)
mppt1BatteryLow = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)

mpptMosfetOverheatLabel = customtkinter.CTkLabel(master=errorFrame,
                                                  text="mpptMosfetOverheat:",
                                                  font=errorFont,
                                                  text_color='black',
                                                  anchor='w')
mppt0MosfetOverheat = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)
mppt1MosfetOverheat = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)

mpptLowArrayPowerLabel = customtkinter.CTkLabel(master=errorFrame,
                                         text="mpptLowArrayPower:",
                                         font=errorFont,
                                         text_color='black',
                                         anchor='w')
mppt0LowArrayPower = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)
mppt1LowArrayPower = customtkinter.CTkLabel(master= errorFrame, 
                                            text="OK",
                                            font=errorFont,
                                            text_color='green',
                                            anchor='w',)


# placing error labels
errorFrameLabel.place(relx=0.03, rely=0.006, anchor='nw')
mpptsErrorLabel.place(relx=0.6, rely=0.006, anchor='nw')

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


# Sunergy Logo
sunergyLogo = customtkinter.CTkImage(light_image=Image.open('Logo.png'), size=(104.16, 45.83))
logoLabel = customtkinter.CTkLabel(mainWin, text="", image=sunergyLogo)
# place on frame
logoLabel.place(x=400,y=0,anchor='n')


mainWin.mainloop()
