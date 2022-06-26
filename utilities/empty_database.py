###############################################################################
#   File: empty_database.py
#   Author(s): Reinhard Schwienhorst
#   Date Created: June, 2022
#
#   Purpose: This simple script just wipes the database files.
#   DO NOT RUN THIS FILE IN THE REAL LAB IF YOU KNOW WHAT YOU'RE DOING!!!!!
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

import os
import sys
import shelve
import pickle

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sMDT.tube import Tube
from sMDT import db, db_legacy

if __name__ == "__main__":
    test = input("This cleanup utility can cause problems if used incorrectly. If you don't know exactly why this program needs to be ran, dont run it.\nType exactly 'confirm' to continue. ")
    if test == 'confirm':
        db_file = 'empty_database.s'

        dict = shelve.open(db_file)
        dict.clear()
        dict.close()
