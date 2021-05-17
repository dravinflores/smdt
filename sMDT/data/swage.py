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
current_folder = os.path.dirname(os.path.abspath(__file__))

# Adds the folder that file is in to the system path
sys.path.append(current_folder)

import textwrap
import station
from record import Record
from datetime import datetime


class SwageRecord(Record):
    """
    Class for objects representing individual records from the Swage station.
    """

    # These are the fail limits for any tube.
    max_raw_length = 2000   # cm
    min_raw_length = 0      # cm
    max_swage_length = 2000   # cm
    min_swage_length = 0      # cm

    # Does this format for a long list of parameters look cleaner?
    def __init__(self, raw_length=None, swage_length=None,
                 clean_code=None, error_code=None, date=datetime.now()):

        # Call the super class init to construct the object.
        super().__init__()
        self.raw_length = raw_length
        self.swage_length = swage_length
        self.clean_code = clean_code
        self.error_code = error_code
        self.date = date 

    def fail(self):
        if self.raw_length < SwageRecord.min_raw_length               \
                or self.raw_length > SwageRecord.max_raw_length       \
                or self.swage_length < SwageRecord.min_swage_length   \
                or self.swage_length > SwageRecord.max_swage_length:
            return True
        else:
            return False

    def __str__(self):
        # Using string concatenation here.
        a = f"Raw Length: {self.raw_length}\n"
        b = f"Swage Length: {self.swage_length}\n"
        c = f"Clean Code: {self.clean_code}\n"
        d = f"Error Code: {self.error_code}\n"
        e = f"Recorded on: {self.date}\n"

        return_str = a + b + c + d + e
        return return_str


class Swage(station.Station, ABC):
    '''
    The Swage station class, manages the relevant records for a particular tube.
    '''
    def __init__(self): 
        super().__init__()

    def __str__(self):
        a = "Swage Data:\n"
        b = ""

        # We want to print out each record.
        for record in self.m_records:
            b += record.__str__() + '\n\n'

        # We want to get rid of the last '\n' in the string.
        b = b[0:-1]

        # We want to have the return string indent each record, for viewing ease.
        return a + textwrap.indent(b, '\t')


if __name__ == "__main__":
    swage = Swage()
    swage.set_record(SwageRecord(raw_length=3.4, swage_length=3.2,clean_code=None, error_code=None))
    swage.set_record(SwageRecord(raw_length=5.2, swage_length=8, clean_code=None, error_code=None))
    swage.set_record(SwageRecord(raw_length=1.03, swage_length=5, clean_code=None, error_code=None))

    print("Created a Swage station object, stored 3 swage records with raw "
          "lengths 3.4, 5.2, 1.03 respectively")
    print("Printing swage.get_record() (default mode is last, should be 1.03)\n")
    # print(swage.get_record())
    print(swage)

    print("Printing swage.get_record('first')\n")
    print(swage.get_record("first"))

    print("Adding mode 'lengthiest', which returns the record with the "
          "grearecord raw_length.\nPrinting swage.get_record('lengthiest')\n")
    station.add_mode("lengthiest", lambda x: sorted(x.m_records, key=lambda y: y.raw_length)[-1])
    print(swage.get_record("lengthiest"))
