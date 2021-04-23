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

from data.swage import Swage
from data.tension import Tension
from data.leak import Leak
from data.dark_current import DarkCurrent

# Import Preparation block.
# Currently only needed so the tests in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)

# Adds the folder that file is in to the system path
sys.path.append(path[:-len(os.path.basename(__file__))])


class Tube:
    def __init__(self, tubeDict={}):
        self.m_tube_id = None
        self.m_comments = []
        self.swage = Swage()
        self.tension = Tension()
        self.leak = Leak()
        self.dark_current = DarkCurrent()

    def dict(self) -> dict():
        return dict()

    def get_comments(self):
        return self.m_comments

    def new_comment(self, comment: str):
        self.m_comments.append(comment)

    def fail(self):
        if self.swage.fail()                    \
                or self.tension.fail()          \
                or self.leak.fail()             \
                or self.dark_current.fail():
            return True
        else:
            return False


if __name__ == '__main__':
    a = Tube()
    a.swage.fail()
