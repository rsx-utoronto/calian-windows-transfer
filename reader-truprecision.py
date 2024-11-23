"""
Filename: reader-truprecision.py

Reads TruPrecision serial data and sends to robot computer on local network over socket

Client-side (Windows, TruPrecision) script

Robotics for Space Exploration - University of Toronto

Author: Jason Li <jasonli.li@mail.utoronto.ca>
Date: 2024-11-16
"""





import socket
import serial
from serial.tools import list_ports





# Ensure that these are the same on the Ubuntu-side Python script.
# HOST should be the Ubuntu computer's local IP, and
# PORT should be an available port on the Ubuntu computer.
# This is to send the data to the Ubuntu computer.
HOST = "192.168.0.32"
PORT = 5409



# Baud rate on TruPrecision
BAUD_RATE = 230400





# Determine serial port -------------------------


selected_com_port = False
available_com_ports_names = ""

while not selected_com_port:

    # Get all COM ports
    available_com_ports = list_ports.comports()
    # Short device name
    available_com_ports_names = list(map(lambda device: device.name, available_com_ports))

    # Ask user to select COM port
    selected_com_port_name = input(f"Select COM port {available_com_ports_names}: ")

    if selected_com_port_name in available_com_ports_names:
        selected_com_port = True
    else:
        print("Invalid COM port.")

# COM port name is selected_com_port_name
print(f"\nDevice: {selected_com_port_name}\nBaud rate: {BAUD_RATE}")


# -----------------------------------------------





# Read and send to other computer ---------------


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect((HOST, PORT))

        print("Connected, sending data.")

        while True:

            with serial.Serial(selected_com_port_name, BAUD_RATE, timeout=1) as ser:
                line_byte = ser.readline()
                soc.sendall(line_byte)



# Failed to connect
except TimeoutError:
    print("Failed to connect to Ubuntu computer.")
    print("Ensure that both computers are connected to the same network, and run the Ubuntu-side script first.")


# -----------------------------------------------
