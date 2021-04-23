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
from abc import ABC



# Import Preparation block.
# Currently only needed so the tests in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)

# Adds the folder that file is in to the system path
sys.path.append(path[:-len(os.path.basename(__file__))])

from station import Station
from test_data import TestData
from datetime import datetime


class TensionTest(TestData):
    """
    Class for objects representing individual tests from the Tension station.
    """

    # Here are the project defined limits.
    max_tension = 350 + 15
    min_tension = 350 - 15

    def __init__(self, tension=None, frequency=None, date=datetime.now()):
        super().__init__()
        self.tension = tension
        self.frequency = frequency
        self.date = date

    def fail(self):
        if self.tension < TensionTest.min_tension \
                or self.tension > TensionTest.max_tension:
            return True
        else:
            return False

    def __str__(self):
        a = f"Tension: {self.tension}\n"
        b = f"Frequency: {self.frequency}\n"
        c = f"Recorded on {self.date}\n"
        return a + b + c


class Tension(Station, ABC):
    '''
    Class for objects representing individual tests from the Tension station.
    '''
    def __init__(self):
        super().__init__()

    def __str__(self):
        pass


if __name__ == "__main__":
    tension = Tension()
    tension.set_test(TensionTest(15, 0.0005, datetime.now()))
    tension.set_test(TensionTest(3, 134.56, datetime.now()))
    print(tension.get_test())
    print(tension.get_test("first"))