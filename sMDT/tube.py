###############################################################################
#   File: db.py
#   Author(s): Paul Johnecheck 
#   Date Created: 16 April, 2021
#
#   Purpose: This is the class representing a tube.
#    an application will create these and store them in the database
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

#Import Preparation block. 
#Currently only needed so the tests in the mains work with the current imports.
import os #This might cause problems on non-windows computers. #WorksOnMyMachine
import sys #This can eventually be removed once this code will only be executed with CWD outside the package itself.
path = os.path.realpath(__file__) #gets the path of the current file being executed
sys.path.append(path[:-len(os.path.basename(__file__))]) #adds the folder that file is in to the system path

from data.swage import Swage, SwageTest
from data.tension import Tension, TensionTest
from data.leak import Leak, LeakTest
from data.dark_current import DarkCurrent, DarkCurrentTest


class Tube():
    def __init__(self, tubeDict=dict()):
        self.m_tube_id = None
        self.m_comments = []
        self.swage = Swage()
        self.tension = Tension()
        self.leak = Leak()
        self.dark_current = DarkCurrent()
        pass
    def dict(self) -> dict():
        return dict()
    def getID(self):
        return self.m_tube_id
    def get_comments(self):
        return self.m_comments
    def new_comment(self, comment: str):
        self.m_comments.append(comment)
    def fail(self) -> bool:
        return True
    def __add__(self, other):
        ret = Tube()
        ret.m_tube_id = self.m_tube_id
        ret.m_comments = self.m_comments + other.m_comments
        ret.swage = self.swage + other.swage
        ret.tension = self.tension + other.tension
        ret.leak = self.leak + other.leak
        ret.dark_current = self.dark_current + other.dark_current
        return ret

if __name__ == '__main__':
    a = Tube()
