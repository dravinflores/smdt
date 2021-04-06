###############################################################################
#   File: tension.py
#   Author(s): Dravin Flores
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
    # Here are the values that determine whether a tension test is within the
    # specification.
    normal = 350
    max = normal + 15
    min = normal - 15

    def __init__(self):
        pass

    def __str__(self):
        pass
