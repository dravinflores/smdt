###############################################################################
#   File: leak.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 06 April, 2021
#
#   Purpose: This file houses the leak test station class. This class stores the
#       data collected from the leak test station into an object.
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
import textwrap


class LeakTest(TestData):
    """
    Class for objects representing individual tests from the Leak station.
    """

    # Here are the project defined limits.
    threshold_leak = 5.0E-5

    def __init__(self, leak_rate=None, date=datetime.now(), data_file=None):
        self.leak_rate = leak_rate
        self.date = date
        self.data_file = data_file

    def __str__(self):
        a = f"Leak Rate: {self.leak_rate}\n"
        b = f"Recorded on: {self.date}\n"
        c = f"Data File: {self.data_file}"
        return a + b + c

    def fail(self):
        if self.leak_rate > LeakTest.threshold_leak:
            return True
        else:
            return False


class Leak(Station, ABC):
    '''
    The Leak station class, manages the relevant tests for a particular tube.
    '''
    def __init__(self):
        super().__init__()

    def __str__(self):
        a = "Leak Data:\n"
        b = ""

        # We want to print out each test.
        for test in self.m_tests:
            b += test.__str__() + '\n\n'

        # We want to get rid of the last '\n' in the string.
        b = b[0:-1]

        # We want to have the return string indent each test, for viewing ease.
        return a + textwrap.indent(b, '\t')


if __name__ == "__main__":
    leak = Leak()
    leak.set_test(LeakTest(0.0001, datetime.now()))
    leak.set_test(LeakTest(3, datetime.now()))
    # print(leak.get_test())
    # print(leak.get_test("first"))
    print(leak)
