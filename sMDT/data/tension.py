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


class TensionRecord(Record):
    """
    Class for objects representing individual records from the Tension station.
    """

    # Here are the project defined limits.
    max_tension = 350 + 15
    min_tension = 350 - 15

    def __init__(self, tension=None, frequency=None,
                 date=datetime.now(), data_file=None):
        super().__init__()
        self.tension = tension
        self.frequency = frequency
        self.date = date
        self.data_file = data_file

    def fail(self):
        if self.tension < Tensionrecord.min_tension \
                or self.tension > Tensionrecord.max_tension:
            return True
        else:
            return False

    def __str__(self):
        a = f"Tension: {self.tension}\n"
        b = f"Frequency: {self.frequency}\n"
        c = f"Recorded on: {self.date}\n"
        d = f"Data File: {self.data_file}"
        return a + b + c + d


class Tension(Station, ABC):
    '''
    Class for objects representing individual records from the Tension station.
    '''
    def __init__(self):
        super().__init__()

    def __str__(self):
        a = "Tension Data:\n"
        b = ""

        # We want to print out each record.
        for record in self.m_records:
            b += record.__str__() + '\n\n'

        # We want to get rid of the last '\n' in the string.
        b = b[0:-1]

        # We want to have the return string indent each record, for viewing ease.
        return a + textwrap.indent(b, '\t')


if __name__ == "__main__":
    tension = Tension()
    tension.set_record(TensionRecord(15, 0.0005, datetime.now()))
    tension.set_record(TensionRecord(3, 134.56, datetime.now()))
    # print(tension.get_record())
    # print(tension.get_record("first"))
    print(tension)