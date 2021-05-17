###############################################################################
#   File: leak.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 06 April, 2021
#
#   Purpose: This file houses the leak record station class. This class stores the
#       data collected from the leak record station into an object.
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
current_folder = os.path.dirname(os.path.abspath(__file__))

# Adds the folder that file is in to the system path
sys.path.append(current_folder)

from station import Station
from record import Record
from datetime import datetime
import textwrap


class LeakRecord(Record):
    """
    Class for objects representing individual records from the Leak station.
    """

    # Here are the project defined limits.
    threshold_leak = 5.0E-5

    def __init__(self, leak_rate=None, date=datetime.now()):
        self.leak_rate = leak_rate
        self.date = date

    def __str__(self):
        a = f"Leak Rate: {self.leak_rate}\n"
        b = f"Recorded on: {self.date}\n"
        return a + b

    def fail(self):
        if self.leak_rate > LeakRecord.threshold_leak:
            return True
        else:
            return False


class Leak(Station, ABC):
    '''
    The Leak station class, manages the relevant records for a particular tube.
    '''
    def __init__(self):
        super().__init__()

    def __str__(self):
        a = "Leak Data:\n"
        b = ""

        # We want to print out each record.
        for record in self.m_records:
            b += record.__str__() + '\n\n'

        # We want to get rid of the last '\n' in the string.
        b = b[0:-1]

        # We want to have the return string indent each record, for viewing ease.
        return a + textwrap.indent(b, '\t')


if __name__ == "__main__":
    leak = Leak()
    leak.set_record(LeakRecord(0.0001, datetime.now()))
    leak.set_record(LeakRecord(3, datetime.now()))
    # print(leak.get_record())
    # print(leak.get_record("first"))
    print(leak)
