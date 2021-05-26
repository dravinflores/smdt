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

from .db import db_manager

if __name__ == "__main__":
    db_man = db_manager()
    db_man.cleanup()
