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
import os
import sys
path = os.path.realpath(__file__)
sys.path.append(path[:-len(os.path.basename(__file__))])

from tube import Tube
from data.dark_current import *
import shelve




class db():
    def __init__(self):
        self.tubes = shelve.open("database.s")
    def addTube(self, tube: Tube()):
        if tube.getID() in self.tubes:
            temp = self.tubes[tube.getID()] + tube
            self.tubes[tube.getID()] = temp
        else:
            self.tubes[tube.getID()] = tube
    def getTube(self, id):
        return self.tubes[id]
    def __del__(self):
        self.tubes.close()
        


if __name__ == '__main__':
    tubes = db()
    tube1 = Tube()
    tube2 = Tube()
    tube1.m_tube_id = "MSUID1"
    tube2.m_tube_id = "MSUID1"
#    tube1.dark_current = DarkCurrent()
#    tube1.dark_current.set_test(DarkCurrentTest(0.001))
#    tube1.dark_current.set_test(5)
#    tube2.dark_current = DarkCurrent()
#    tube2.dark_current.set_test(DarkCurrentTest(0.002))
    tubes.addTube(tube1)
    print(tubes.getTube("MSUID1").dark_current.get_test())
#    tubes.addTube(tube2)
    print(tubes.getTube("MSUID1").dark_current.get_test())
    
