###############################################################################
#   File: swage.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 02 April, 2021
#
#   Purpose: This file houses the swage station class. This class stores the
#       data collected from the swage station into an object.
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

import station
from test_data import TestData


class SwageTest(TestData):
    """
    Class for objects representing individual tests from the Swage station.
    """

    # These are the fail limits for any tube.
    max_raw_length = 2000   # cm
    min_raw_length = 0      # cm
    max_swage_length = 2000   # cm
    min_swage_length = 0      # cm

    # Does this format for a long list of parameters look cleaner?
    def __init__(self, raw_length=None, swage_length=None,
                 clean_code=None, error_code=None):

        # Call the super class init to construct the object.
        super().__init__()
        self.raw_length = raw_length
        self.swage_length = swage_length
        self.clean_code = clean_code
        self.error_code = error_code

    def fail(self):
        if self.raw_length < SwageTest.min_raw_length               \
                or self.raw_length > SwageTest.max_raw_length       \
                or self.swage_length < SwageTest.min_swage_length   \
                or self.swage_length > SwageTest.max_swage_length:
            return True
        else:
            return False

    def __str__(self):
        # Using string concatenation here.
        a = f"Raw Length: {self.raw_length}\n"
        b = f"Swage Length: {self.swage_length}\n"
        c = f"Clean Code: {self.clean_code}\n"
        d = f"Error Code: {self.error_code}\n"
        return_str = a + b + c + d
        return return_str


class Swage(station.Station, ABC):
    '''
    The Swage station class, manages the relevant tests for a particular tube.
    '''
    def __init__(self): 
            super().__init__()


if __name__ == "__main__":
    swage = Swage()
    swage.set_test(SwageTest(raw_length=3.4, swage_length=3.2, clean_code=None, error_code=None))
    swage.set_test(SwageTest(raw_length=5.2, swage_length=8., clean_code=None, error_code=None))
    swage.set_test(SwageTest(raw_length=1.03, swage_length=5, clean_code=None, error_code=None))

    print("Created a Swage station object, stored 3 swage tests with raw lengths 3.4, 5.2, 1.03 respectively")
    print("Printing swage.get_test() (default mode is last, should be 1.03)\n")
    print(swage.get_test())

    print("Printing swage.get_test('first')\n")
    print(swage.get_test("first"))

    print("Adding mode 'lengthiest', which returns the test with the greatest raw_length.\nPrinting swage.get_test('lengthiest')\n")
    station.add_mode("lengthiest", lambda x: sorted(x.m_tests, key=lambda y: y.raw_length)[-1])
    print(swage.get_test("lengthiest"))
    