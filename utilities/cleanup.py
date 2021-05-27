###############################################################################
#   File: cleanup.py
#   Author(s): Paul Johnecheck
#   Date Created: 02 May, 2021
#
#   Purpose: This simple script just wipes the new_data and the locks directory.
#   Crashed or prematurely ended programs can leave data here that can mess with things.
#   This should only be ran while developing, this can and will cause data to not get put into the database.
#   DO NOT RUN THIS FILE IN THE REAL LAB IF YOU KNOW WHAT YOU'RE DOING!!!!!
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

import os
import sys
DROPBOX_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DROPBOX_DIR)

from sMDT import db

if __name__ == "__main__":
    test = input("This cleanup utility can cause problems if used incorrectly. If you don't know exactly why this program needs to be ran, dont run it.\nType exactly 'confirm' to continue. ")
    if test == 'confirm':
        db_man = db.db_manager()
        db_man.cleanup()
