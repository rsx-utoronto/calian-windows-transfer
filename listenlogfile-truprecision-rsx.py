"""
Filename: listenlogfile-truprecision-rsx.py

Listen to TruPrecision log file sent from Windows computer on local network over socket

Server-side (Ubuntu, ROS) script

Robotics for Space Exploration - University of Toronto

Author: Jason Li <jasonli.li@mail.utoronto.ca>
Date: 2024-11-16
"""





import socket





# Ensure that these are the same as the Windows-side Python script
HOST = "192.168.0.99"
PORT = 8080





# Socket listener -------------------------------


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    print("Ready for connection from Windows")
    
    while True:

        # Found connection
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")


            while True:

                # Received data
                data = conn.recv(1024)
                if data:

                    received_line = data.decode()
                    print(received_line)
                    # TODO: Publish received_line to ROS topic

                # Disconnect when data has stopped
                # Outer while loop will wait for connection again
                else:
                    break


# -----------------------------------------------
