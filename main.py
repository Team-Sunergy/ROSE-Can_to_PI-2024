from can_interface import setup_can_interface, shutdown_can_interface
from bus import initialize_bus
from message_parser import parse_can_message, group_can_data
from tools import getBits, send_request_frame0_periodically, getSpeed
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import queue
import threading
from mockDataTransfer import *
from tkinter import *
import customtkinter
import ttkbootstrap as tb
from PIL import Image


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
                                       text="version 0.1",
                                       font=('Gotham', 10),
                                       )
versionLabel.place(relx=0.99, rely=0.015, anchor='ne')


# Fonts
dashFont = customtkinter.CTkFont(family='Gotham', weight='bold', size=35)
socFont = customtkinter.CTkFont(family='Gotham', weight='bold', size=10)


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


# define error frame
errorFrame = customtkinter.CTkFrame(master=secondWin,
                                  width=200,
                                  height=300,
                                  corner_radius=5,
                                  fg_color='#E5E5E5',
                                  border_width=1,
                                  border_color='black',)
errorFrameLabel = customtkinter.CTkLabel(master=errorFrame,
                                         text="ACTIVE ERRORS",
                                         font=socFont,
                                         text_color='black',
                                         )
errorFrameVal = customtkinter.CTkLabel(master=errorFrame,
                                text='none',
                                font=dashFont,
                                text_color='black',
                                )
errorFrameLabel.place(relx=0.5, rely=0.01, anchor='n')
errorFrameVal.place(relx=0.5, rely=0.5, anchor='center')
# place on frame
errorFrame.place(x=795,y=5,anchor='ne')


# Sunergy Logo
sunergyLogo = customtkinter.CTkImage(light_image=Image.open('Logo.png'), size=(104.16, 45.83))
logoLabel = customtkinter.CTkLabel(mainWin, text="", image=sunergyLogo)
# place on frame
logoLabel.place(x=400,y=0,anchor='n')


def startGui():
    """starts the gui loop given data"""
    print("Starting gui")
    mainWin.mainloop()

def updateGuiData(dataQueue):
    """updates gui via a queue system"""
    try:
        # non-blocking get from queue
        data = dataQueue.get_nowait()
    except queue.Empty:
        # no new data
        pass
    else:
        # data received, update labels
        update_label(data=data)

    # schedule next update
    mainWin.after(100, updateGuiData, dataQueue)

        
def update_label(data: dict):
        """private for gui.py, takes data dict
        and updates label"""
        print("updating label")
        if data['DataType'] != 'none':
            # update speed with speed
            speedometer.config(amountused=str(data['Speed']))
            socVal.config(str(data['SOC']))
            ampsInValue.config(Text=str(data['InputCurrent0'] + data['InputCurrent1']))
            ampsOutValue.config(Text=str(data['OutputCurrent0'] + data['OutputCurrent1']))
            ampsDiffValue.config(Text=str(
                (data['InputCurrent0'] + data['InputCurrent1']) - (data['OutputCurrent0'] + data['OutputCurrent1'])))
        else:
             speedometer.config(text="0")
             socVal.config(Text="not loaded")
             ampsInValue.config("not loaded")
             ampsOutValue.config("not loaded")
             ampsDiffValue.config("not loaded")

def worker_thread(queue, bus):
    """A worker thread that generates canData and puts it on the queue."""
    print("Running worker thread.")
    while True:
        data = canCollection(bus)
        queue.put(data) # puts data in queue
        time.sleep(0.1)  # controls the rate of data generation.

def canCollection(bus):
    print("In the try")
    try:
        message = bus.recv()
        parsed_message = parse_can_message(message) # recieves parsed message
        data = parsed_message['data']
        # group up data into a table
        groupedData = group_can_data(parsed_message['arbitration_id'], data=data)
        # used for seeing can frames
        
        if groupedData["DataType"] == 'mppt1error' or data['DataType'] == 'mppt0error':
            print(data["DataType"])
            print("LowArrayPower: " + str(data['LowArrayPower']))
            print("MosfetOverheat: " + str(data['MosfetOverheat']))
            print("BatteryLow: "+ str(data['BatteryLow']))
            print("BatteryFull: " + str(data['BatteryFull']))
            print("12VUnderVoltage: " + str(data['12VUnderVoltage']))
            print("HWOvercurrent: " + str(data['HWOvercurrent']))
            print("HWOvervoltage: " + str(data['HWOvervoltage']))

        print(f"Timestamp: {parsed_message['timestamp']:.6f}")
        print(f"ID: {parsed_message['arbitration_id']:x}")
        print(f"DLC: {parsed_message['dlc']}")
        print(f"Data: {parsed_message['data_str']}")
        print("-" * 30)

        
        # used for sending data, contains all different types of possible categories (mppts, bms, mc)
        # depending on what CAN frame ID is
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
    print("The setup_can_interface done")
    bus = initialize_bus()
    print("Bus variable is set")
    # this is for motor controllers
    send_request_frame0_periodically(bus=bus)
    print("Sending request frame0 in main...")
    worker = threading.Thread(target=worker_thread, args=(dataQueue, bus))
    worker.start()
    mainWin.after(100, updateGuiData, dataQueue)
    startGui()

if __name__ == "__main__":
    main()


