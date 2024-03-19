import argparse
from pathlib import Path
import os
import sys

user_id = os.getuid()
if user_id != 0:
    raise SystemError("This scipt requires root privileges")

parser = argparse.ArgumentParser()
parser.add_argument(
    "pencode", help="File to register to run at startup.", required=True)
