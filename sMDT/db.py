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



class db():
    def __init__(self):
        self.tubes = []
    def addTube(tube: Tube()):
        self.tubes.append(tube)

if __name__ == 'main':
    tubes = db()
    tubes.addTube(Tube())