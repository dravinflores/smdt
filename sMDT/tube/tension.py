###############################################################################
#   File: tension.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 06 April, 2021
#
#   Purpose: This file houses the tension station class. This class stores the
#       data collected from the tension station into an object.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################
from station import Station


class Tension(Station):
    def __init__(self, users=[], tests=[]):
        super().__init__(users, tests)

    def __str__(self):
        pass
