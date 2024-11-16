"""
Filename: readlogfile-truprecision-rsx.py

Reads TruPrecision log file and sends to robot computer on local network over socket

Client-side (Windows, TruPrecision) script

Robotics for Space Exploration - University of Toronto

Author: Jason Li <jasonli.li@mail.utoronto.ca>
Date: 2024-11-16
"""





import datetime
import os
import socket
import json





# Ensure that these are the same as the Ubuntu-side Python script
HOST = "192.168.0.99"
PORT = 8080





# Open log file ---------------------------------


path = "C:\\ProgramData\\Tallysman\\TruPrecision\\Logs\\Rover"

# File name format:
# Serial_20241016.txt
# year month day

current_date = datetime.date.today()
current_date_formatted = str(current_date.year) + str(current_date.month) + str(current_date.day)
filename = "Serial_" + current_date_formatted + ".txt"
filepath = os.path.join(path, filename)

print(f"Reading file: {filepath}")


# -----------------------------------------------





# Determine lines read already ------------------


lines_already_read = 0

# JSON file stores lines read of all log files
logfilelinesread_path = "logfilelinesread.json"

try:
    # Get lines read from JSON file, if available
    with open(logfilelinesread_path, "r") as f:

        lines_already_read_all_files = json.load(f)

        if filepath in lines_already_read_all_files:
            # this log file already read
            lines_already_read = lines_already_read_all_files[filepath]

except FileNotFoundError:
    # Create JSON file if not exist
    with open(logfilelinesread_path, "w") as f:
        json.dump({filepath: lines_already_read}, f)


# -----------------------------------------------





# Read and send to other computer ---------------


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:

            # Open log file
            try:
                with open(filepath) as f:
                    # ignore lines already read
                    lines_read = f.read().splitlines()[lines_already_read:]

            # If log file doesn't exist
            except FileNotFoundError:
                # if file doesn't exist create file and close it
                open(filepath, "w").close()
                continue # ignore rest of loop, continue to next iteration



            # Send lines to computer
            for i in range(len(lines_read)):
                current_line = lines_read[i]
                s.sendall(current_line.encode())


            # Update lines read
            lines_already_read += len(lines_read)

            with open(logfilelinesread_path, "r") as f:
                logfiledata = json.load(f)
            with open(logfilelinesread_path, "w") as f:
                logfiledata[filepath] = lines_already_read
                json.dump(logfiledata, f)



# Failed to connect
except TimeoutError:
    print("Failed to connect to Ubuntu computer.")
    print("Ensure that both computers are connected to the same network, and run the Ubuntu-side script first.")


# -----------------------------------------------
