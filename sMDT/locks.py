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

import os
import time


class Lock:
    sMDT_DIR = os.path.dirname(os.path.abspath(__file__))
    LOCK_DIR = os.path.join(sMDT_DIR, "locks")

    def __init__(self, key=""):
        '''
        Constructor, gets the locks key. Builds the lock's path out of the key
        '''
        self.key = key 
        self.locked_by_this = False
        self.lock_path = os.path.join(self.LOCK_DIR, key + ".lock")

    def lock(self):
        '''
        This Lock becomes locked. A file key.lock is written to the lock path
        '''
        if not os.path.isdir(self.LOCK_DIR):
            os.mkdir(self.LOCK_DIR)
        lock = open(self.lock_path, 'a')
        lock.write(self.key + " locked.")
        self.locked_by_this = True
        lock.close()

    def unlock(self):
        '''
        This Lock becomes unlocked. The file key.lock is deleted from the lock path
        '''
        self.locked_by_this = False
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
        if self.locked_by_this:
            self.unlock()

    @classmethod
    def cleanup(Lock):
        if not os.path.isdir(Lock.LOCK_DIR):
            os.mkdir(Lock.LOCK_DIR)
        for filename in os.listdir(Lock.LOCK_DIR):
            os.remove(os.path.join(Lock.LOCK_DIR, filename))