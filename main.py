from can_interface import setup_can_interface, shutdown_can_interface
from bus import initialize_bus
from message_parser import parse_can_message, group_can_data
import queue
import time
import threading
from tkinter import *
from tkinter import Tk, Frame, Label
from tkinter.font import Font
from PIL import Image, ImageTk
from tools import getDisplayColor, getMPPTErrors, getState
# definition of main window
root = Tk()
root.title("GUI for Driver Interface")
root.geometry('800x480')

mainWin = Frame(root, bg='#E5E5E5')
root.attributes('-fullscreen', True)
mainWin.pack(fill='both', expand=True)

secondWin = Frame(mainWin, bg='white')
secondWin.place(relx=0.0, rely=0.095, relwidth=1, relheight=0.905)

versionLabel = Label(mainWin, text="version 0.4", font=('Gotham', 10), background="#E5E5E5")
versionLabel.place(relx=0.99, rely=0.015, anchor='ne')

# Fonts
dashFont = Font(family='Gotham', weight='bold', size=30)
dashFontSmall = Font(family='Gotham', weight='bold', size=28)
dashFontSmall2 = Font(family='Gotham', weight='bold', size=20)
socFont = Font(family='Gotham', weight='bold', size=10)
faultFont = Font(family='Gotham', weight='bold', size=32)
faultFont2 = Font(family='Gotham', weight='bold', size=20)
speedFont = Font(family='Gotham', weight='bold', size=200)
errorFont = Font(family='Gotham', size=7)
errorFont2 = Font(family='Gotham', size=10)

speedometerNum = Label(secondWin, text="25", font=speedFont, bg="white")
speedometerNum.place(relx=0.5, rely=0.5, anchor='center')

# define SOC frame (top left)
socFrame = Frame(secondWin, bg='#E5E5E5', relief='raised', borderwidth=1)
socFrame.place(x=5, y=5, width=200, height=85)

socLabel = Label(socFrame, text='STATE OF CHARGE', font=socFont, background='#E5E5E5',)
socLabel.place(relx=0.5, rely=0.01, anchor='n')

socVal = Label(socFrame, text='-1%', font=dashFont, background='#E5E5E5',)
socVal.place(relx=0.5, rely=0.55, anchor='center')

# define NET Amps frame (top right)
netFrame = Frame(secondWin, bg='#E5E5E5', relief='raised', borderwidth=1)
netFrame.place(x=595, y=5, width=200, height=85)

netLabel = Label(netFrame, text='NET AMPERAGE', font=socFont, background='#E5E5E5',)
netLabel.place(relx=0.5, rely=0.01, anchor='n')

netVal = Label(netFrame, text='-1%', font=dashFont, background='#E5E5E5',)
netVal.place(relx=0.5, rely=0.55, anchor='center')

# define fault frame (middle left)
stateFrame = Frame(secondWin, bg='#E5E5E5', relief='raised', borderwidth=1)
stateFrame.place(relx=0.5, y=5, width=375, height=75, anchor='n')
mphIndicatorLabel = Label(stateFrame, text='AVGM:', font=dashFontSmall2, background='#E5E5E5', foreground='black')
mphIndicatorLabel.place(relx=0.075, rely=0.275, anchor='w')

netIndicatorLabel = Label(stateFrame, text='AVGAM:', font=dashFontSmall2, background='#E5E5E5', foreground='black')
netIndicatorLabel.place(relx=0.075, rely=0.675, anchor='w')



# define AMPS frame
ampsInFrame = Frame(master=secondWin,
                                  width=200,
                                  height=100,
                                  background='#E5E5E5',
                                  borderwidth=1,
                                  relief='raised',
                                  )
ampsInLabel = Label(master=ampsInFrame,
                                text='SOLAR AMPERAGE IN',
                                font=socFont,
                                foreground='black',
                                background='#E5E5E5',
                                )
ampsInValue = Label(master=ampsInFrame,
                                     text='-1 AMPS',
                                     font=dashFont,
                                     foreground='black',
                                     background='#E5E5E5',
                                     )
ampsInLabel.place(relx=0.5, rely=0.01, anchor='n')
ampsInValue.place(relx=0.5, rely=0.5, anchor='center')
ampsInFrame.place(x=5,y=428,anchor='sw')

def setTimeToZero():
    global secondsElapsed
    global totalMiles
    global currentNetAmps
    global totalNetAmps
    secondsElapsed = 0
    totalMiles = 0
    currentNetAmps = 0
    totalNetAmps = 0

avgMilesStartButton = Button(master=stateFrame, 
                                text="55mi",
                                font=dashFontSmall2,
                                command=setTimeToZero,
                                )

avgAmpsLabel = Label(master=stateFrame,
                         text="-12amp",
                         font=dashFontSmall2,
                         foreground='black',
                         background='#E5E5E5',
                         )



ampsOutFrame = Frame(master=secondWin,
                                  width=200,
                                  height=100,
                                  background='#E5E5E5',
                                  borderwidth=1,
                                  relief='raised',
                                  )
ampsOutLabel = Label(master=ampsOutFrame,
                                text='DATA COLLECTION',
                                font=socFont,
                                foreground='black',
                                background='#E5E5E5',
                                )
ampsOutValue = Label(master=ampsOutFrame,
                                     text='-1 AMPS',
                                     font=dashFontSmall,
                                     foreground='black',
                                     background='#E5E5E5',
                                     )
ampsOutValue.place(relx=0.5, rely=0.55, anchor='center')
ampsOutLabel.place(relx=0.5, rely=0.01, anchor='n')
ampsOutFrame.place(x=795,y=428,anchor='se')

# discharge and charge limits
#line

chargCurrFrame = Frame(master=secondWin, width=250, height=65, background='#E5E5E5', borderwidth=1, relief='raised')
disFrame = Frame(master=chargCurrFrame, 
                    width=250, height=32.5,
                    background='#E5E5E5',
                    borderwidth=1,
                    relief='raised')
chaFrame = Frame(master=chargCurrFrame,
                    width=250, height=32.5,
                    background='#E5E5E5',
                    borderwidth=1,
                    relief='raised',
                    )
disCurrLimitLabel = Label(master=disFrame,
                          text="DCL:",
                          font=socFont,
                          foreground='black',
                          background='#E5E5E5'
                          )
charCurrLimitLabel = Label(master=chaFrame,
                           text='CCL:',
                           font=socFont,
                           foreground='black',
                           background='#E5E5E5',
                           )
disVal = Label(master=disFrame,
               text="-1amp",
               font=socFont,
               foreground='black',
               background='#E5E5E5',
               )
charVal = Label(master=chaFrame,
               text="-1amp",
               font=socFont,
               foreground='black',
               background='#E5E5E5')

disCurrLimitLabel.place(relx=0.5, rely=0.5, anchor='center')
charCurrLimitLabel.place(relx=0.5, rely=0.5, anchor='center')
disFrame.place(relx=0.4, rely=0.0, anchor='n')
chaFrame.place(relx=0.4, rely=1.0, anchor='s')
disVal.place(relx=0.7, rely=0.5, anchor='center')
charVal.place(relx=0.7, rely=0.5, anchor='center')
chargCurrFrame.place(relx=0.5, y=428, anchor='s')



# # frame for button
# avgMilesFrame = Frame(master=secondWin,
#                       width=125, height=65,
#                       background='#E5E5E5',
#                       borderwidth=1, relief='raised')
# avgMilesFrame.place(x=275,y=428,anchor='s')



# avgMilesStartButton = Button(master=avgMilesFrame, 
#                                 text="55mi",
#                                 font=dashFontSmall,
#                                 command=setTimeToZero,
#                                 )
avgMilesStartButton.place(relx=0.7, rely=0.3, width=200, height=25, anchor='center')
avgAmpsLabel.place(relx=0.7, rely=0.7, width=200, height=25, anchor='center')



# BELOW ARE ALL THE ANNOYING ERROR FRAME DIAGNOSTICS
errorFrame = Frame(master=secondWin,
                                  width=200,
                                  height=207,
                                  background='#E5E5E5',
                                  borderwidth=1,
                                  relief='raised'
                                  )
mppts0ErrorLabel = Label(master=errorFrame,
                                    text="mppt0",
                                    font=errorFont2,
                                    background='#E5E5E5',
                                    foreground='black')


# on labels
mppt0OnLabel = Canvas(master=errorFrame, width=20, height=20, background='#E5E5E5', bd=0, highlightthickness=0,)
standby0 = mppt0OnLabel.create_oval(15, 15, 5, 5, fill='yellow')
mppt0OnLabel.place(relx=0.31, rely=0.03, anchor='n') #31

mppt1OnLabel = Canvas(master=errorFrame, width=20, height=20, background='#E5E5E5', bd=0, highlightthickness=0,)
standby1 = mppt1OnLabel.create_oval(15, 15, 5, 5, fill='yellow')
mppt1OnLabel.place(relx=0.8, rely=0.03, anchor='n')

mppts1ErrorLabel = Label(master=errorFrame,
                                    text="mppt1",
                                    font=errorFont2,
                                    background='#E5E5E5',
                                    foreground='black')
mppt0HWOverCurrentLabel = Label(master=errorFrame,
                                text="M0HWOverCurrent",
                                font=errorFont,
                                foreground='#d7d7d7',
                                background='#E5E5E5',
                                anchor='w',)
mppt1HWOverCurrentLabel = Label(master=errorFrame,
                                text="M1HWOverCurrent",
                                font=errorFont,
                                foreground='#d7d7d7',
                                background='#E5E5E5',
                                anchor='w',)
mppt0HWOverVoltageLabel = Label(master=errorFrame,
                                                 text="M0HWOverVoltage",
                                                 font=errorFont,
                                                 foreground='#d7d7d7',
                                                 background='#E5E5E5',
                                                 anchor='w')
mppt1HWOverVoltageLabel = Label(master=errorFrame,
                                                 text="M1HWOverVoltage",
                                                 font=errorFont,
                                                 foreground='#d7d7d7',
                                                 background='#E5E5E5',
                                                 anchor='w')
mppt012VUnderVoltageLabel = Label(master=errorFrame,
                                                   text="M0VUnderVoltage",
                                                   font=errorFont,
                                                   foreground='#d7d7d7',
                                                   background='#E5E5E5',
                                                   anchor='w')
mppt112VUnderVoltageLabel = Label(master=errorFrame,
                                                   text="M1VUnderVoltage",
                                                   font=errorFont,
                                                   foreground='#d7d7d7',
                                                   background='#E5E5E5',
                                                   anchor='w')
mppt0BatteryFullLabel = Label(master=errorFrame,
                                               text="M0BatteryFull",
                                               font=errorFont,
                                               foreground='#d7d7d7',
                                               background='#E5E5E5',
                                               anchor='w')
mppt1BatteryFullLabel = Label(master=errorFrame,
                                               text="M1BatteryFull",
                                               font=errorFont,
                                               foreground='#d7d7d7',
                                               background='#E5E5E5',
                                               anchor='w')
mppt0BatteryLowLabel = Label(master=errorFrame,
                                              text="M0BatteryLow",
                                              font=errorFont,
                                              foreground='#d7d7d7',
                                              background='#E5E5E5',
                                              anchor='w')
mppt1BatteryLowLabel = Label(master=errorFrame,
                                              text="M1BatteryLow",
                                              font=errorFont,
                                              foreground='#d7d7d7',
                                              background='#E5E5E5',
                                              anchor='w')
mppt0MosfetOverheatLabel = Label(master=errorFrame,
                                                  text="M0MosfetOverheat",
                                                  font=errorFont,
                                                  foreground='#d7d7d7',
                                                  background='#E5E5E5',
                                                  anchor='w')
mppt1MosfetOverheatLabel = Label(master=errorFrame,
                                                  text="M1MosfetOverheat",
                                                  font=errorFont,
                                                  foreground='#d7d7d7',
                                                  background='#E5E5E5',
                                                  anchor='w')
mppt0LowArrayPowerLabel = Label(master=errorFrame,
                                         text="M0LowArrayPower",
                                         font=errorFont,
                                         foreground='#d7d7d7',
                                         background='#E5E5E5',
                                         anchor='w')
mppt1LowArrayPowerLabel = Label(master=errorFrame,
                                         text="M1LowArrayPower",
                                         font=errorFont,
                                         foreground='#d7d7d7',
                                         background='#E5E5E5',
                                         anchor='w')

# placing error labels
mppts0ErrorLabel.place(relx=0.02, rely=0.03, anchor='nw')
mppts1ErrorLabel.place(relx=0.52, rely=0.03, anchor='nw')

mppt0LowArrayPowerLabel.place(relx=0.02, rely=0.20, anchor='w') #0.22
mppt1LowArrayPowerLabel.place(relx=0.52, rely=0.20, anchor='w')

mppt0MosfetOverheatLabel.place(relx=0.02, rely=0.32, anchor='w')
mppt1MosfetOverheatLabel.place(relx=0.52, rely=0.32, anchor='w')

mppt0BatteryLowLabel.place(relx=0.02, rely=0.4332, anchor='w')
mppt1BatteryLowLabel.place(relx=0.52, rely=0.4332, anchor='w')

mppt0BatteryFullLabel.place(relx=0.02, rely=0.5448, anchor='w')
mppt1BatteryFullLabel.place(relx=0.52, rely=0.5448, anchor='w')

mppt012VUnderVoltageLabel.place(relx=0.02, rely=0.6664, anchor='w')
mppt112VUnderVoltageLabel.place(relx=0.52, rely=0.6664, anchor='w')

mppt0HWOverVoltageLabel.place(relx=0.02, rely=0.778, anchor='w')
mppt1HWOverVoltageLabel.place(relx=0.52, rely=0.778, anchor='w')

mppt0HWOverCurrentLabel.place(relx=0.02, rely=0.88, anchor='w')
mppt1HWOverCurrentLabel.place(relx=0.52, rely=0.88, anchor='w')


# place on frame
errorFrame.place(x=5, y=105)  #x=795,y=5,anchor='ne') 



# BELOW ARE ALL THE ANNOYING ERROR FRAME DIAGNOSTICS part 2
flagFrame = Frame(master=secondWin,
                                  width=200,
                                  height=207,
                                  background='#E5E5E5',
                                  borderwidth=1,
                                  relief='raised'
                                  )

mppts0ErrorLabel = Label(master=flagFrame,
                                    text="mppt0",
                                    font=errorFont2,
                                    background='#E5E5E5',
                                    foreground='black')
mppt0OnLabel.place(relx=0.31, rely=0.03, anchor='n')

mppts1ErrorLabel = Label(master=flagFrame,
                                    text="mppt1",
                                    font=errorFont2,
                                    background='#E5E5E5',
                                    foreground='black')
mppt0InputCurrentMinLabel = Label(master=flagFrame,
                                text="M0InCurrentMin",
                                font=errorFont,
                                foreground='#d7d7d7',
                                background='#E5E5E5',
                                anchor='w',)
mppt1InputCurrentMinLabel = Label(master=flagFrame,
                                text="M1HInCurrentMin",
                                font=errorFont,
                                foreground='#d7d7d7',
                                background='#E5E5E5',
                                anchor='w',)
mppt0InputCurrentMaxLabel = Label(master=flagFrame,
                                                 text="M0InCurrentMax",
                                                 font=errorFont,
                                                 foreground='#d7d7d7',
                                                 background='#E5E5E5',
                                                 anchor='w')
mppt1InputCurrentMaxLabel = Label(master=flagFrame,
                                                 text="M1InCurrentMax",
                                                 font=errorFont,
                                                 foreground='#d7d7d7',
                                                 background='#E5E5E5',
                                                 anchor='w')
mppt0OutputVoltageMaxLabel = Label(master=flagFrame,
                                                   text="M0OutVoltageMax",
                                                   font=errorFont,
                                                   foreground='#d7d7d7',
                                                   background='#E5E5E5',
                                                   anchor='w')
mppt1OutputVoltageMaxLabel = Label(master=flagFrame,
                                                   text="M1OutVoltageMax",
                                                   font=errorFont,
                                                   foreground='#d7d7d7',
                                                   background='#E5E5E5',
                                                   anchor='w')
mppt0MosfetTemperatureMPPTLabel = Label(master=flagFrame,
                                               text="M0MosTempMPPT",
                                               font=errorFont,
                                               foreground='#d7d7d7',
                                               background='#E5E5E5',
                                               anchor='w')
mppt1MosfetTemperatureMPPTLabel = Label(master=flagFrame,
                                               text="M1MosTempMPPT",
                                               font=errorFont,
                                               foreground='#d7d7d7',
                                               background='#E5E5E5',
                                               anchor='w')
mppt0DutyCycleMin = Label(master=flagFrame,
                                              text="M0DutyCycleMin",
                                              font=errorFont,
                                              foreground='#d7d7d7',
                                              background='#E5E5E5',
                                              anchor='w')
mppt1DutyCycleMin = Label(master=flagFrame,
                                              text="M1DutyCycleMin",
                                              font=errorFont,
                                              foreground='#d7d7d7',
                                              background='#E5E5E5',
                                              anchor='w')
mppt0DutyCycleMax = Label(master=flagFrame,
                                                  text="M0DutyCycleMax",
                                                  font=errorFont,
                                                  foreground='#d7d7d7',
                                                  background='#E5E5E5',
                                                  anchor='w')
mppt1DutyCycleMax = Label(master=flagFrame,
                                                  text="M1DutyCycleMax",
                                                  font=errorFont,
                                                  foreground='#d7d7d7',
                                                  background='#E5E5E5',
                                                  anchor='w')
mppt0LocalMPPTLabel = Label(master=flagFrame,
                                         text="M0LocalMPPT",
                                         font=errorFont,
                                         foreground='#d7d7d7',
                                         background='#E5E5E5',
                                         anchor='w')
mppt1LocalMPPTLabel = Label(master=flagFrame,
                                         text="M1LocalMPPT",
                                         font=errorFont,
                                         foreground='#d7d7d7',
                                         background='#E5E5E5',
                                         anchor='w')
mppt0GlobalMPPTLabel = Label(master=flagFrame,
                                         text="M0GlobalMPPT",
                                         font=errorFont,
                                         foreground='#d7d7d7',
                                         background='#E5E5E5',
                                         anchor='w')
mppt1GlobalMPPTLabel = Label(master=flagFrame,
                                         text="M1GlobalMPPT",
                                         font=errorFont,
                                         foreground='#d7d7d7',
                                         background='#E5E5E5',
                                         anchor='w')


# placing limit labels
mppt0InputCurrentMinLabel.place(relx=0.02, rely=0.03, anchor='nw')
mppt1InputCurrentMinLabel.place(relx=0.52, rely=0.03, anchor='nw')

mppt0InputCurrentMaxLabel.place(relx=0.02, rely=0.20, anchor='w') #0.22
mppt1InputCurrentMaxLabel.place(relx=0.52, rely=0.20, anchor='w')

mppt0OutputVoltageMaxLabel.place(relx=0.02, rely=0.32, anchor='w')
mppt1OutputVoltageMaxLabel.place(relx=0.52, rely=0.32, anchor='w')

mppt0MosfetTemperatureMPPTLabel.place(relx=0.02, rely=0.4332, anchor='w')
mppt1MosfetTemperatureMPPTLabel.place(relx=0.52, rely=0.4332, anchor='w')

mppt0DutyCycleMin.place(relx=0.02, rely=0.5448, anchor='w')
mppt1DutyCycleMin.place(relx=0.52, rely=0.5448, anchor='w')

mppt0DutyCycleMax.place(relx=0.02, rely=0.6664, anchor='w')
mppt1DutyCycleMax.place(relx=0.52, rely=0.6664, anchor='w')

mppt0LocalMPPTLabel.place(relx=0.02, rely=0.778, anchor='w')
mppt1LocalMPPTLabel.place(relx=0.52, rely=0.778, anchor='w')

mppt0GlobalMPPTLabel.place(relx=0.02, rely=0.88, anchor='w')
mppt1GlobalMPPTLabel.place(relx=0.52, rely=0.88, anchor='w')


# place on frame
flagFrame.place(x=795,y=105, anchor='ne')

img = Image.open('Logo.png')
img = img.resize((84, 37))
sunergyLogo = ImageTk.PhotoImage(img)
logoLabel = Label(mainWin, image=sunergyLogo, background='#E5E5E5')
logoLabel.image = sunergyLogo  
logoLabel.place(x=400, y=0, anchor='n')




# seconds elapsed
secondsElapsed = 0.0
totalMiles = 0.0
totalNetAmps = 0.0
currentNetAmps = 0.0
currentMPH = 0

def startGui():
    """starts the gui loop given data"""
    print("Starting gui")
    root.mainloop()


def updateGuiData(dataQueue):
    """updates gui via a queue system"""
    data = None
    try:
        # non-blocking get from queue
        data = dataQueue.get_nowait()
    except queue.Empty:
        pass
    else:
        # data received, update labels
        update_label(data=data)

    # seconds elapsed
    global secondsElapsed # get seconds elapsed
    secondsElapsed += 0.1
    # for total miles
    global totalMiles # gets total miles
    global currentMPH
    # for avg net amps
    global totalNetAmps
    global currentNetAmps

    totalMiles = (currentMPH * 0.1/3600) + totalMiles # get total miles
    avgMPH = totalMiles/(secondsElapsed/3600) # get average mph
    avgMilesStartButton.config(text=f"{avgMPH:.1f}" + "mph") # sets button to avgMiles

    totalNetAmps = (currentNetAmps + totalNetAmps)
    avgAmps = totalNetAmps/(secondsElapsed * 10)
    print(currentNetAmps)
    avgAmpsLabel.config(text=f"{avgAmps:.1f}" + "amps")

   
     

    # schedule next update
    mainWin.after(100, updateGuiData, dataQueue)

        
def update_label(data: dict):
        """private for gui.py, takes data dict
        and updates label"""
        if data['DataType'] == 'mppt0error':
            mppt0OnLabel.itemconfig(standby0, fill=getDisplayColor(data['Mode']))
            mppt0LowArrayPowerLabel.config(foreground=getMPPTErrors(data['LowArrayPower']))
            mppt0MosfetOverheatLabel.config(foreground=getMPPTErrors(data['MosfetOverheat']))
            mppt0BatteryLowLabel.config(foreground=getMPPTErrors(data['BatteryLow']))
            mppt0BatteryFullLabel.config(foreground=getMPPTErrors(data['BatteryFull']))
            mppt012VUnderVoltageLabel.config(foreground=getMPPTErrors(data['12VUnderVoltage']))
            mppt0HWOverCurrentLabel.config(foreground=getMPPTErrors(data['HWOverCurrent']))
            mppt0HWOverVoltageLabel.config(foreground=getMPPTErrors(data['HWOverVoltage']))

            mppt0InputCurrentMinLabel.config(foreground=getMPPTErrors(data['InputCurrentMin']))
            mppt0InputCurrentMaxLabel.config(foreground=getMPPTErrors(data['InputCurrentMax']))
            mppt0OutputVoltageMaxLabel.config(foreground=getMPPTErrors(data['OutputVoltageMax']))
            mppt0MosfetTemperatureMPPTLabel.config(foreground=getMPPTErrors(data['MosfetTemperatureMPPT']))
            mppt0DutyCycleMin.config(foreground=getMPPTErrors(data['DutyCycleMin']))
            mppt0DutyCycleMax.config(foreground=getMPPTErrors(data['DutyCycleMax']))
            mppt0LocalMPPTLabel.config(foreground=getMPPTErrors(data['LocalMPPT']))
            mppt0GlobalMPPTLabel.config(foreground=getMPPTErrors(data['GlobalMPPT']))


        elif data['DataType'] == 'mppt1error':
            mppt1OnLabel.itemconfig(standby1, fill=getDisplayColor(data['Mode']))
            mppt1LowArrayPowerLabel.config(foreground=getMPPTErrors(data['LowArrayPower']))
            mppt1MosfetOverheatLabel.config(foreground=getMPPTErrors(data['MosfetOverheat']))
            mppt1BatteryLowLabel.config(foreground=getMPPTErrors(data['BatteryLow']))
            mppt1BatteryFullLabel.config(foreground=getMPPTErrors(data['BatteryFull']))
            mppt112VUnderVoltageLabel.config(foreground=getMPPTErrors(data['12VUnderVoltage']))
            mppt1HWOverCurrentLabel.config(foreground=getMPPTErrors(data['HWOverCurrent']))
            mppt1HWOverVoltageLabel.config(foreground=getMPPTErrors(data['HWOverVoltage']))

            mppt1InputCurrentMinLabel.config(foreground=getMPPTErrors(data['InputCurrentMin']))
            mppt1InputCurrentMaxLabel.config(foreground=getMPPTErrors(data['InputCurrentMax']))
            mppt1OutputVoltageMaxLabel.config(foreground=getMPPTErrors(data['OutputVoltageMax']))
            mppt1MosfetTemperatureMPPTLabel.config(foreground=getMPPTErrors(data['MosfetTemperatureMPPT']))
            mppt1DutyCycleMin.config(foreground=getMPPTErrors(data['DutyCycleMin']))
            mppt1DutyCycleMax.config(foreground=getMPPTErrors(data['DutyCycleMax']))
            mppt1LocalMPPTLabel.config(foreground=getMPPTErrors(data['LocalMPPT']))
            mppt1GlobalMPPTLabel.config(foreground=getMPPTErrors(data['GlobalMPPT']))

        elif data['DataType'] == 'bmsData':
            netVal.config(text=str(data['PackCurrent']))
            #print("pack current: " + str(data['PackCurrent']))
            disVal.config(text=data['PackDCL'])
            charVal.config(text=data['PackCCL'])
        elif data['DataType'] != 'none': # might change
            # update speed with speed
            speedometerNum.config(text=data['Speed'])
            socVal.configure(text=f"{data['SOC']:.1f}")
            ampsInValue.configure(text=f"{data['OutputCurrent0'] + data['OutputCurrent1']:.1f}")
            #print("mppt0" + str(data['OutputCurrent0']))
            #print("mppt1" + str(data['OutputCurrent1']))
            ampsOutValue.configure(text=f"{(data['OutputCurrent0'] + data['OutputCurrent1'] - data['PackCurrent']):.1f}")
        else:
            pass 

        # update current MPH
        global currentMPH
        currentMPH = data['Speed']
        global currentNetAmps
        currentNetAmps = data['PackCurrent']

def worker_thread(queue, bus):
    """A worker thread that generates canData and puts it on the queue."""
    print("Running worker thread.")
    while True:
        data = canCollection(bus)
        queue.put(data) # puts data in queue

def canCollection(bus):
    #print("In the try")
    try:
        message = bus.recv()
        parsed_message = parse_can_message(message) # recieves parsed message
        data = parsed_message['data']
        # group up data into a table
        groupedData = group_can_data(parsed_message['arbitration_id'], data=data) # updates data with new data
        # used for seeing can frames
        #print("MOSFET:" + str(groupedData['MosfetTemperature']))
        #print("CONTROLLER TEMP:" + str(groupedData['ControllerTemperature']))
        #print(groupedData['PackCurrent'])
        #print("mppt0 amps" + str(groupedData['InputCurrent0']))
        #print("mppt1 amps " + str(groupedData['InputCurrent1']))
        #print("CURRENT VOLTAGE:" + str(groupedData['OutputVoltage0']))
        # print(f"Timestamp: {parsed_message['timestamp']:.6f}")
        # print(f"ID: {parsed_message['arbitration_id']:x}")
        # print(f"DLC: {parsed_message['dlc']}")
        # print(f"Data: {parsed_message['data_str']}")
        # print("-" * 30)
        # print("SOC: " + str(groupedData['SOC']))

        
        # used for sending data, contains all different types of possible categories (mppts, bms, mc)
        # depending on what CAN frame ID is
        #print(secondsElapsed)
        return groupedData
    
    except KeyboardInterrupt:
        shutdown_can_interface()
        print("\n\rKeyboard interrupt")

# data queue for data
dataQueue = queue.Queue()

def main():
    """
    Main function to set up the CAN interface, initialize the bus, and continuously
    receive and parse CAN messages until interrupted by user.
    """
    setup_can_interface()
    secondsElapsed = 0.0
    print("The setup_can_interface done")
    bus = initialize_bus()
    print("Bus variable is set")
    # this is for motor controllers
    print("Sending request frame0 in main...")
    worker = threading.Thread(target=worker_thread, args=(dataQueue, bus))
    worker.start()
    root.after(100, updateGuiData, dataQueue)
    startGui()

if __name__ == "__main__":
    main()


