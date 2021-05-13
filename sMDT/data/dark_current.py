###############################################################################
#   File: dark-current.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 06 April, 2021
#
#   Purpose: This file houses the dark current record station class. This class
#       stores the data collected from the dark current record station into
#       an object.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################
from abc import ABC



# Import Preparation block.
# Currently only needed so the records in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)

# Adds the folder that file is in to the system path
sys.path.append(path[:-len(os.path.basename(__file__))])

from station import Station
from record import Record
from datetime import datetime
import textwrap


class DarkCurrentRecord(Record):
    """
    Class for objects representing individual records from the Dark Current station.
    """

    # Here are the project defined limits.
    max_individual_current = 1E-9   # 1 nA
    max_collective_current = 8E-9   # 8 nA

    def __init__(self, dark_current=None, date=datetime.now()):
        super().__init__()
        self.dark_current = dark_current
        self.date = date

    def __str__(self):
        a = f"Dark Current: {self.dark_current}\n"
        b = f"Recorded on: {self.date}\n"
        return a + b

    def fail(self):
        if self.dark_current > DarkCurrentRecord.max_individual_current:
            return True
        else:
            return False


class DarkCurrent(Station, ABC):
    """
    Class for objects representing individual records from the Dark Current station.
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        a = "Dark Current Data:\n"
        b = ""

        # We want to print out each record.
        for record in self.m_records:
            b += record.__str__() + '\n\n'

        # We want to get rid of the last '\n' in the string.
        b = b[0:-1]

        # We want to have the return string indent each record, for viewing ease.
        return a + textwrap.indent(b, '\t')


if __name__ == "__main__":
    dark_current = DarkCurrent()
    dark_current.set_record(DarkCurrentRecord(15,  date=datetime.now()))
    dark_current.set_record(DarkCurrentRecord(3,  date=datetime.now()))
    # print(dark_current.get_record())
    # print(dark_current.get_record("first"))
    print(dark_current)
