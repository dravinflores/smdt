###############################################################################
#   File: __init__.py
#   Author(s): Paul Johnecheck
#   Date Created: 11 April, 2021
#
#   Purpose: __init__file for the tube object package 
#
#   Known Issues:
#   Something is wrong with the imports, and I'm not sure what. Needs fixing
#
#   Workarounds:
#
###############################################################################


__all__ = ["dark_current", "leak", "swage","tension", "tube"]

import sys
sys.path.append('\sMDT\tube')
from swage import Swage
from tension import Tension
from leak import Leak
from dark_current import Dark_Current


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

if __name__ == 'main':
    a = Tube()
