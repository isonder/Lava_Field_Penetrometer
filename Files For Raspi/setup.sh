#!/usr/bin/env bash

# Make rc.local executable to enable all commands listed in there to run after
# automatically boot.
sudo chmod +x /etc/rc.local

# Install required packages
sudo apt-get update
sudo apt install python3-rpi.gpio

# If things install without problems, register penetrometer in rc.local
# Get the current working directory
CWD=$(pwd)
# Path to the code that needs to run at startup
PENFILE="${CWD}/Penetrometer_execution_code.py"
