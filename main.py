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
faultFont = Font(family='Gotham', weight='bold', size=30)
speedFont = Font(family='Gotham', weight='bold', size=200)
errorFont = Font(family='Gotham', size=7)
errorFont2 = Font(family='Gotham', size=10)

speedometerNum = Label(secondWin, text="25", font=speedFont, bg="white")
speedometerNum.place(relx=0.5, rely=0.45, anchor='center')

# define SOC frame (top left)
socFrame = Frame(secondWin, bg='#E5E5E5', relief='raised', borderwidth=1)
socFrame.place(x=5, y=5, width=200, height=100)

socLabel = Label(socFrame, text='STATE OF CHARGE', font=socFont, background='#E5E5E5',)
socLabel.place(relx=0.5, rely=0.01, anchor='n')

socVal = Label(socFrame, text='95.5%', font=dashFont, background='#E5E5E5',)
socVal.place(relx=0.5, rely=0.5, anchor='center')

# define fault frame (middle left)
stateFrame = Frame(secondWin, bg='#E5E5E5', relief='raised', borderwidth=1)
stateFrame.place(relx=0.5, y=5, width=325, height=75, anchor='n')
indicatorLabel = Label(stateFrame, text='FAULT', font=faultFont, background='#E5E5E5', foreground='black')
indicatorLabel.place(relx=0.5, rely=0.47, anchor='center')


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

#define fault code frame
faultCodeFrame = Frame(master=secondWin, 
                       width=100,
                       height=100,
                       background='#E5E5E5',
                       borderwidth=1,
                       relief='raised',
                       )

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
mppts0ErrorLabel = Label(master=errorFrame,
                                    text="mppt0",
                                    font=errorFont2,
                                    background='#E5E5E5',
                                    foreground='black')
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
root.mainloop()
