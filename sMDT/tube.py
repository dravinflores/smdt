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

import os
import sys
path = os.path.realpath(__file__)
sys.path.append(path[:-len(os.path.basename(__file__))])

from data.swage import Swage
from data.tension import Tension
from data.leak import Leak
from data.dark_current import Dark_Current


class Tube():
    def __init__(self, tubeDict=dict()):
        self.m_tube_id = None
        self.m_comments = []
        self.swage = Swage()
        self.swage.test()
        print("test")
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