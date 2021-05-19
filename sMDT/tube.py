###############################################################################
#   File: tube.py
#   Author(s): Paul Johnecheck, Dravin Flores
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

# Import Preparation block.
# Currently only needed so the tests in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)
current_folder = os.path.dirname(os.path.abspath(__file__))

# Adds the folder that file is in to the system path
sys.path.append(current_folder)

from data.swage import Swage
from data.tension import Tension
from data.leak import Leak
from data.dark_current import DarkCurrent


class Tube:
    def __init__(self):
        self.m_tube_id = None
        self.m_comments = []
        self.swage = Swage()
        self.tension = Tension()
        self.leak = Leak()
        self.dark_current = DarkCurrent()
        self.legacy_data = dict()

    def __add__(self, other):
        ret = Tube()
        ret.m_tube_id = self.m_tube_id
        ret.m_comments = self.m_comments + other.m_comments
        ret.swage = self.swage + other.swage
        ret.leak = self.leak + other.leak
        ret.dark_current = self.dark_current + other.dark_current
        ret.tension = self.tension + other.tension
        ret.legacy_data = self.legacy_data | other.legacy_data 
        return ret

    def __str__(self):
        n = self.getID() + '\n'
        a = self.swage.__str__()
        b = self.tension.__str__()
        c = self.leak.__str__()
        d = self.dark_current.__str__()

        ret_str = n + a + b + c + d
        ret_str = str(ret_str)

        return ret_str

    def getID(self):
        return self.m_tube_id

    def get_comments(self):
        return self.m_comments

    def new_comment(self, comment: str):
        self.m_comments.append(comment)

    def fail(self):
        return any([x.fail() for x in [self.swage,self.leak,self.tension,self.dark_current]])

    def dict(self) -> dict():
        return dict()


if __name__ == '__main__':
    a = Tube()
    print(a)
