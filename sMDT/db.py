    ###############################################################################
#   File: db.py
#   Author(s): Paul Johnecheck
#   Date Created: 11 April, 2021
#
#   Purpose: This is the class representing the database.
#    It will act as the main interface for reading and writing to the database. 
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################


# Import Preparation block.
# Currently only needed so the records in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)

# Adds the folder that file is in to the system path
sys.path.append(path[:-len(os.path.basename(__file__))])

from tube import Tube
from data.dark_current import DarkCurrent, DarkCurrentRecord
from data.station import *
import shelve


class db:
    def __init__(self, mode='file', path=None):
        if mode == 'file':
            if path:
                self.tubes = shelve.open(path)
            else:
                self.tubes = shelve.open("database.s")
            self.shelve = True
        elif mode == 'mem':
            self.tubes = dict()
            self.shelve = False
        else:
            raise NotImplementedError

    def add_tube(self, tube: Tube()):
        if tube.getID() in self.tubes:
            temp = self.tubes[tube.getID()] + tube
            self.tubes[tube.getID()] = temp
        else:
            self.tubes[tube.getID()] = tube

    def get_tube(self, id):
        return self.tubes[id]

    def wipe(self):
        for key in self.tubes:
            del self.tubes[key]

    def __del__(self):
        if self.shelve:
            self.tubes.close()


