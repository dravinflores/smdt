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
from datetime import datetime
import textwrap

from .station import Station
from .status import Status
from .record import Record


class SwageRecord(Record):
    """
    Class for objects representing individual records from the Swage station.
    """

    # These are the fail limits for any tube.
    max_raw_length      = 1000  # cm
    min_raw_length      = -1000 # cm
    max_swage_length    = 1000  # cm
    min_swage_length    = -1000 # cm

    # Does this format for a long list of parameters look cleaner?
    def __init__(self, raw_length=None, swage_length=None,
                 clean_code=None, date=datetime.now(), user=None):

        # Call the super class init to construct the object.
        super().__init__(user)
        self.raw_length = raw_length
        self.swage_length = swage_length
        self.clean_code = clean_code
        self.date = date 

    def fail(self):
        if self.raw_length is None or self.swage_length is None:
            return True
        elif self.raw_length < SwageRecord.min_raw_length \
                or self.raw_length > SwageRecord.max_raw_length \
                or self.swage_length < SwageRecord.min_swage_length \
                or self.swage_length > SwageRecord.max_swage_length:
            return True
        else:
            return False
        
    def __str__(self):
        # Using string concatenation here.
        a = f"Raw Length: {self.raw_length}\n"
        b = f"Swage Length: {self.swage_length}\n"
        c = f"Clean Code: {self.clean_code}\n"
        e = f"Recorded on: {self.date}\n"
        f = f"Recorded by: {self.user}\n\n"

        return_str = a + b + c + e + f
        return return_str



class Swage(Station, ABC):
    """
    The Swage station class, manages the relevant records for a particular tube.
    """
    def __init__(self): 
        super().__init__()

    def __str__(self):
        a = "Swage Data: " + self.status().name + "\n"
        b = ""

        # We want to print out each record.
        for record in sorted(self.m_records, key=lambda i: i.date):
            b += record.__str__()

        b = b[:-1]

        # We want to have the return string indent each record, for 
        # viewing ease.
        return a + textwrap.indent(b, '\t') + '\n'
    
    def fail(self):
        if not self.visited():
            return False
        return self.get_record(mode='last').fail()

    def status(self):
        if not self.visited():
            return Status.INCOMPLETE
        elif self.fail():
            return Status.FAIL
        else:
            return Status.PASS
