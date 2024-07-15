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
root.attributes('-fullscreen', False)
mainWin.pack(fill='both', expand=True)

secondWin = Frame(mainWin, bg='white')
secondWin.place(relx=0.0, rely=0.095, relwidth=1, relheight=0.905)

versionLabel = Label(mainWin, text="version 0.4", font=('Gotham', 10), background="#E5E5E5")
versionLabel.place(relx=0.99, rely=0.015, anchor='ne')

# Fonts
dashFont = Font(family='Gotham', weight='bold', size=30)
dashFontSmall = Font(family='Gotham', weight='bold', size=28)
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

# define fault frame (middle left)
stateFrame = Frame(secondWin, bg='#E5E5E5', relief='raised', borderwidth=1)
stateFrame.place(relx=0.5, y=5, width=325, height=75, anchor='n')
indicatorLabel = Label(stateFrame, text='FAULT', font=faultFont, background='#E5E5E5', foreground='black')
indicatorLabel.place(relx=0.075, rely=0.475, anchor='w')


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
                                     text='-1 AMPS',
                                     font=dashFont,
                                     foreground='black',
                                     background='#E5E5E5',
                                     )
ampsInLabel.place(relx=0.5, rely=0.01, anchor='n')
ampsInValue.place(relx=0.5, rely=0.5, anchor='center')
ampsInFrame.place(x=5,y=428,anchor='sw')

# define fault code frame
faultCodeFrame = Frame(master=stateFrame, 
                       width=100,
                       height=50,
                       background='#E5E5E5',
                       borderwidth=1,
                       relief='sunken',
                       )
faultCodeFrame.place(relx=0.93, rely=0.5, anchor='e')
faultCodeLabel = Label(master=faultCodeFrame,
                       text='FAULT CODE: ',
                       font=errorFont,
                       foreground='black',
                       background='#E5E5E5')
faultCodeLabel.place(relx=0.0, rely=0.0, anchor='nw')
faultCodeValue = Label(master=faultCodeFrame,
                       text='0x69',
                       font=faultFont2, 
                       background='#E5E5E5'
                       )
faultCodeValue.place(relx=.9, rely=0.62, anchor='e')



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
                                     text='-1 AMPS',
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
                                     text='-1AMPS',
                                     font=Font(family='Gotham', weight='bold', size=25),
                                     foreground='black',
                                     background='#E5E5E5',
                                     )
ampsDiffLabel = Label(master=ampsDiffFrame,
                                     text='NET AMPS',
                                     font=socFont,
                                     foreground='black',
                                     background='#E5E5E5',
                                    )
ampsDiffValue.place(relx=0.5, rely=0.53, anchor='center')
ampsDiffLabel.place(relx=0.5, rely=0.02,anchor='n')
ampsDiffFrame.place(x=400,y=428,anchor='s')

# discharge and charge limits
#line
chargCurrFrame = Frame(master=secondWin, width=200, height=210, background='#E5E5E5', borderwidth=1, relief='raised')
line = Canvas(master=chargCurrFrame, width=190, height=50,
              background='#E5E5E5', bd=0, highlightthickness=0)
line.place(relx=0.49, rely=0.5, anchor='center')
line.create_line(5, 25, 200, 25)

disCurrLimitLabel = Label(master=chargCurrFrame,
                          text="DIS. CURR LIM",
                          font=socFont,
                          foreground='black',
                          background='#E5E5E5')
chargCurrFrame.place(x=5, y=105)
disCurrLimitLabel.place(relx=0.5, rely=0.10, anchor='center')
disCurrLimitVal = Label(master=chargCurrFrame,
                        text="-1AMPS",
                        font=dashFont,
                        foreground='black',
                        background='#E5E5E5')
disCurrLimitVal.place(relx=0.5, rely=0.30, anchor='center')
charCurrLimitLabel = Label(master=chargCurrFrame,
                           text='CHAR. CURR LIM',
                           font=socFont,
                           foreground='black',
                           background='#E5E5E5')
charCurrLimitVal = Label(master=chargCurrFrame,
                         text="-1AMPS",
                         font=dashFont,
                         foreground='black',
                         background='#E5E5E5')
charCurrLimitVal.place(relx=0.5, rely=0.80, anchor='center')
charCurrLimitLabel.place(relx=0.5, rely=0.60, anchor='center')


# frame for button
avgMilesFrame = Frame(master=secondWin,
                      width=200, height=100,
                      background='#E5E5E5',
                      borderwidth=1, relief='raised')
avgMilesFrame.place(x=795, y=200, anchor='ne')
avgMilesStartButton = Button(master=avgMilesFrame, 
                                text="Click",
                                )
avgMilesStartButton.place(relx=0.5, rely=0.5)

def setTimeToZero():
    global secondsElapsed
    secondsElapsed = 0

# BELOW ARE ALL THE ANNOYING ERROR FRAME DIAGNOSTICS
errorFrame = Frame(master=secondWin,
                                  width=200,
                                  height=175,
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
mppt0OnLabel.place(relx=0.31, rely=0.03, anchor='n')

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

mppt0LowArrayPowerLabel.place(relx=0.02, rely=0.22, anchor='w')
mppt1LowArrayPowerLabel.place(relx=0.52, rely=0.22, anchor='w')

mppt0MosfetOverheatLabel.place(relx=0.02, rely=0.34, anchor='w')
mppt1MosfetOverheatLabel.place(relx=0.52, rely=0.34, anchor='w')

mppt0BatteryLowLabel.place(relx=0.02, rely=0.4532, anchor='w')
mppt1BatteryLowLabel.place(relx=0.52, rely=0.4532, anchor='w')

mppt0BatteryFullLabel.place(relx=0.02, rely=0.5648, anchor='w')
mppt1BatteryFullLabel.place(relx=0.52, rely=0.5648, anchor='w')

mppt012VUnderVoltageLabel.place(relx=0.02, rely=0.6864, anchor='w')
mppt112VUnderVoltageLabel.place(relx=0.52, rely=0.6864, anchor='w')

mppt0HWOverVoltageLabel.place(relx=0.02, rely=0.798, anchor='w')
mppt1HWOverVoltageLabel.place(relx=0.52, rely=0.798, anchor='w')

mppt0HWOverCurrentLabel.place(relx=0.02, rely=0.90, anchor='w')
mppt1HWOverCurrentLabel.place(relx=0.52, rely=0.90, anchor='w')

# place on frame
errorFrame.place(x=795,y=5,anchor='ne')


img = Image.open('Logo.png')
img = img.resize((84, 37))
sunergyLogo = ImageTk.PhotoImage(img)
logoLabel = Label(mainWin, image=sunergyLogo, background='#E5E5E5')
logoLabel.image = sunergyLogo  
logoLabel.place(x=400, y=0, anchor='n')


# seconds elapsed
secondsElapsed = 0.0
totalMiles = 0.0
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
    global secondsElapsed
    secondsElapsed += 0.1
    print(secondsElapsed)

    global totalMiles
    global currentMPH
    totalMiles = (currentMPH * secondsElapsed/3600) + totalMiles
    print(currentMPH)

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
        elif data['DataType'] == 'mppt1error':
            mppt1OnLabel.itemconfig(standby1, fill=getDisplayColor(data['Mode']))
            mppt1LowArrayPowerLabel.config(foreground=getMPPTErrors(data['LowArrayPower']))
            mppt1MosfetOverheatLabel.config(foreground=getMPPTErrors(data['MosfetOverheat']))
            mppt1BatteryLowLabel.config(foreground=getMPPTErrors(data['BatteryLow']))
            mppt1BatteryFullLabel.config(foreground=getMPPTErrors(data['BatteryFull']))
            mppt112VUnderVoltageLabel.config(foreground=getMPPTErrors(data['12VUnderVoltage']))
            mppt1HWOverCurrentLabel.config(foreground=getMPPTErrors(data['HWOverCurrent']))
            mppt1HWOverVoltageLabel.config(foreground=getMPPTErrors(data['HWOverVoltage']))
        elif data['DataType'] == 'STM':
            faultCodeLabel.config(text=getState(data['State']))
            faultCodeValue.config(text=data['FaultID'])
        elif data['DataType'] == 'bmsData':
            disCurrLimitVal.config(text=data['PackDCL'])
            charCurrLimitVal.config(text=data['PackCCL'])
        elif data['DataType'] != 'none': # might change
            # update speed with speed
            speedometerNum.config(text=data['Speed'])
            socVal.configure(text=f"{data['SOC']:.1f}")
            ampsInValue.configure(text=f"{data['OutputCurrent0'] + data['OutputCurrent1']:.1f}")
            ampsOutValue.configure(text=f"{data['PackCurrent'] - (data['OutputCurrent0'] + data['OutputCurrent1']):.1f}")
        else:
            pass 

        # update current MPH
        global currentMPH
        currentMPH = data['Speed']

        global secondsElapsed
        global totalMiles
        avgMPH = totalMiles/(secondsElapsed/3600)
        avgMilesStartButton.config(text=avgMPH)

def worker_thread(queue, bus):
    """A worker thread that generates canData and puts it on the queue."""
    print("Running worker thread.")
    while True:
        data = canCollection(bus)
        queue.put(data) # puts data in queue

def canCollection(bus):
    print("In the try")
    try:
        message = bus.recv()
        parsed_message = parse_can_message(message) # recieves parsed message
        data = parsed_message['data']
        # group up data into a table
        groupedData = group_can_data(parsed_message['arbitration_id'], data=data) # updates data with new data
        # used for seeing can frames
        
        # print(f"Timestamp: {parsed_message['timestamp']:.6f}")
        # print(f"ID: {parsed_message['arbitration_id']:x}")
        # print(f"DLC: {parsed_message['dlc']}")
        # print(f"Data: {parsed_message['data_str']}")
        # print("-" * 30)
        # print("SOC: " + str(groupedData['SOC']))

        
        # used for sending data, contains all different types of possible categories (mppts, bms, mc)
        # depending on what CAN frame ID is
        print(secondsElapsed)
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


