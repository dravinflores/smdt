###############################################################################
#   File: swage.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 02 April, 2021
#
#   Purpose: This file houses the swager station class. This class stores the
#       data collected from the swager station into an object.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################
from station import Station


class Swage(Station):
    def __init__(self, users=[], tests=[]):
        super().__init__(users, tests)

    def __str__(self):
        pass