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
    def __init__(self, mode='file'):
        if mode == 'file':
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


if __name__ == '__main__':
    print("Database stored in memory, demonstrating tube addition")
    tubes = db(mode='mem')

    tube1 = Tube()
    tube1.m_tube_id = "MSUID1"
    tube1.dark_current.set_record(DarkCurrentRecord(0.001))

    print("Adding first tube, printing last dark current record")
    tubes.add_tube(tube1)
    print(tubes.get_tube("MSUID1").dark_current.get_record())

    tube2 = Tube()
    tube2.m_tube_id = "MSUID1"
    tube2.dark_current.set_record(DarkCurrentRecord(0.002))

    print("Adding second tube, printing last dark current record")
    tubes.add_tube(tube2)
    print(tubes.get_tube("MSUID1").dark_current.get_record())

    del tubes

    print("Database stored in file using shelve")
    tubes2 = db(mode='file')
    tubes2.wipe()

    tube1 = Tube()
    tube1.m_tube_id = "MSUID1"
    tube1.dark_current.set_record(DarkCurrentRecord(0.001))

    print("Adding first tube, printing last dark current record")
    tubes2.add_tube(tube1)
    print(tubes2.get_tube("MSUID1").dark_current.get_record())

    tube2 = Tube()
    tube2.m_tube_id = "MSUID1"
    tube2.dark_current.set_record(DarkCurrentRecord(0.002))

    print("Adding second tube, printing last dark current record")
    tubes2.add_tube(tube2)
    print(tubes2.get_tube("MSUID1").dark_current.get_record())

    del tubes2

    print("Close file database and reopen, printing the dark current "
          "result that was stored")
    tubes3 = db(mode='file')
    print(tubes3.get_tube("MSUID1").dark_current.get_record())
