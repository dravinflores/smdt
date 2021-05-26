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
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Adds the folder that file is in to the system path
sys.path.append(DATA_DIR)

import textwrap
import station
from record import Record
from datetime import datetime


class SwageRecord(Record):
    """
    Class for objects representing individual records from the Swage station.
    """

    # These are the fail limits for any tube.
    max_raw_length = 1000   # cm
    min_raw_length = -1000      # cm
    max_swage_length = 1000   # cm
    min_swage_length = -1000      # cm

    # Does this format for a long list of parameters look cleaner?
    def __init__(self, raw_length=None, swage_length=None,
                 clean_code=None, error_code=None, date=datetime.now(), user=None):

        # Call the super class init to construct the object.
        super().__init__(user)
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
        f = f"Recorded by: {self.user}\n"

        return_str = a + b + c + d + e + f
        return return_str


class Swage(station.Station, ABC):
    """
    The Swage station class, manages the relevant records for a particular tube.
    """
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
    
    def fail(self):
        return self.get_record(mode='last').fail()
