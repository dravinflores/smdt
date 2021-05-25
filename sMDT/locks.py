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
sMDT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCK_DIR = os.path.join(sMDT_DIR, "locks")

# Adds the folder that file is in to the system path
sys.path.append(sMDT_DIR)

import time


class Lock:
    

    def __init__(self, key=""):
        '''
        Constructor, gets the locks key. Builds the lock's path out of the key
        '''
        self.key = key 
        
        self.lock_path = os.path.join(LOCK_DIR, key + ".lock")

    def lock(self):
        '''
        This Lock becomes locked. A file key.lock is written to the lock path
        '''
        if not os.path.isdir(LOCK_DIR):
            os.mkdir(LOCK_DIR)
        lock = open(self.lock_path, 'a')
        lock.write(self.key + " locked.")
        lock.close()

    def unlock(self):
        '''
        This Lock becomes unlocked. The file key.lock is deleted from the lock path
        '''
        if os.path.exists(self.lock_path):
            os.remove(self.lock_path)

    def is_locked(self):
        '''
        Returns true if the lock is locked, false otherwise
        '''
        return os.path.exists(self.lock_path)

    def wait(self):
        '''
        Causes the program that calls this function to wait until the lock is unlocked.
        '''
        while self.is_locked():
            time.sleep(0.5)

    def __del__(self):
        self.unlock()

    @staticmethod
    def cleanup():
        if not os.path.isdir(LOCK_DIR):
            os.mkdir(LOCK_DIR)
        for filename in os.listdir(LOCK_DIR): 
            os.remove(os.path.join(LOCK_DIR, filename))