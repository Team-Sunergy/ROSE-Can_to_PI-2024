# C.A.N. Bus to Raspberry Pi Interface for Driver UI

Welcome to the C.A.N. Bus to Raspberry Pi interface project! This project aims to enable a Raspberry Pi to read C.A.N. messages and display data for the driver and passengers in a solar car.

## Project Overview

The goal of this project is to:

1. Interface the Raspberry Pi with the C.A.N. Bus system.
2. Read and process C.A.N. messages.
3. Display relevant data to the driver and passengers.

This project is a crucial part of the solar car's driver UI system, ensuring that important information is readily available.

## Features

- **C.A.N. Bus Integration**: Seamlessly connect the Raspberry Pi with the vehicle's C.A.N. Bus.
- **Real-time Data Display**: Provide up-to-date information to enhance the driving experience.
- **User-friendly Interface**: Ensure the displayed data is easy to read and understand.

## Getting Started

To get started with this project, follow the instructions below:

1. **Hardware Setup**: Connect the Raspberry Pi to the C.A.N. Bus using the appropriate hardware.
2. **Software Installation**: Install the necessary software and libraries on the Raspberry Pi.
3. **Configuration**: Configure the system to read and display C.A.N. messages.

## Contributors

Developed by:
- Nathan Care
- John Waugh
- Blaez Jibben
- Sean Choi

## Todo
 - find a way to filter out each msg(i.e look for specific ID numbers)
 - find each msg ID
 - display Speed, Soc, Power intake, Power outtake.
 - make some kind of gui (Make a acutral gui or just use flask(i.e html/css))
 - get a LoRa dongle
 - send data to the cloud
 - get a new screen
