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

from data.swage import Swage
from data.tension import Tension
from data.leak import Leak
from data.dark_current import Dark_Current


class Tube():
    def __init__(self, tubeDict=dict()):
        self.m_tube_id = None
        self.m_comments = []
        self.swage = Swage()
        self.tension = Tension()
        self.leak = Leak()
        self.dark_current = Dark_Current()
        pass
    def dict(self) -> dict():
        return dict()
    def get_comments(self):
        return self.m_comments
    def new_comment(self, comment: str):
        self.m_comments.append(comment)
    def fail(self) -> bool:
        return True

if __name__ == '__main__':
    a = Tube()
    a.swage.test()