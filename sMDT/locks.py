###############################################################################
#   File: locks.py
#   Author(s): Paul Johnecheck
#   Date Created: 5 May, 2021
#
#   Purpose: Provides a system of custom mutex (mutual exclusion) locks for use
#   with accessing the database and other files.
#   These will be general purpose, in the off chance we need mutex for anything else
#       
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

# Import Preparation block.
# Currently only needed so the tests in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)
current_folder = os.path.dirname(os.path.abspath(__file__))

# Adds the folder that file is in to the system path
sys.path.append(current_folder)

import time

new_data_folder = os.path.join(current_folder, "new_data")

class Lock:
    def __init__(self, key=""):
        self.key = key
        self.lock_path = os.path.join(current_folder, "locks", key + ".lock")

    def lock(self):
        lock = open(self.lock_path, 'a')
        lock.write(self.key + " locked.")
        lock.close()

    def unlock(self):
        if os.path.exists(self.lock_path):
            os.remove(self.lock_path)

    def is_locked(self):
        return os.path.exists(self.lock_path)

    def wait(self):
        while self.is_locked():
            time.wait(0.5)
