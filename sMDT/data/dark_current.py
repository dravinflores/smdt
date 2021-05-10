###############################################################################
#   File: dark-current.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 06 April, 2021
#
#   Purpose: This file houses the dark current test station class. This class
#       stores the data collected from the dark current test station into
#       an object.
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


class DarkCurrentTest(TestData):
    """
    Class for objects representing individual tests from the Dark Current station.
    """

    # Here are the project defined limits.
    max_individual_current = 1E-9   # 1 nA
    max_collective_current = 8E-9   # 8 nA

    def __init__(self, dark_current=None, date=datetime.now(), data_file=None):
        super().__init__()
        self.dark_current = dark_current
        self.date = date
        self.data_file = data_file

    def __str__(self):
        a = f"Dark Current: {self.dark_current}\n"
        b = f"Recorded on: {self.date}\n"
        c = f"Data File: {self.data_file}"
        return a + b + c

    def fail(self):
        if self.dark_current > DarkCurrentTest.max_individual_current:
            return True
        else:
            return False


class DarkCurrent(Station, ABC):
    """
    Class for objects representing individual tests from the Dark Current station.
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        a = "Dark Current Data:\n"
        b = ""

        # We want to print out each test.
        for test in self.m_tests:
            b += test.__str__() + '\n\n'

        # We want to get rid of the last '\n' in the string.
        b = b[0:-1]

        # We want to have the return string indent each test, for viewing ease.
        return a + textwrap.indent(b, '\t')


if __name__ == "__main__":
    dark_current = DarkCurrent()
    dark_current.set_test(DarkCurrentTest(15,  date=datetime.now()))
    dark_current.set_test(DarkCurrentTest(3,  date=datetime.now()))
    # print(dark_current.get_test())
    # print(dark_current.get_test("first"))
    print(dark_current)
