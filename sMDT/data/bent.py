###############################################################################
#   File: swage.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 02 April, 2021
#
#   Purpose: This file houses the bentness class. This class stores the
#       data collected from the bentness measurement into an object.
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


class BentRecord(Record):
    """
    Class for objects representing individual records from the Bentness station.
    """

    # These are the fail limits for any tube.
    max_bentness = 0.9   # mm

    # Does this format for a long list of parameters look cleaner?
    def __init__(self, bentness=None, date=datetime.now(), user=None):

        # Call the super class init to construct the object.
        super().__init__(user)
        self.date = date 
        self.bentness = bentness

    def fail(self):
        if self.bentness is None:
            return False
        if self.bentness >= BentRecord.max_bentness:
            return True
        else:
            return False

    def __str__(self):
        # Using string concatenation here.
        a = f"Bentness: {self.bentness}\n"
        b = f"Recorded on: {self.date}\n"
        c = f"Recorded by: {self.user}\n\n"

        return_str = a + b + c
        return return_str


class Bent(Station, ABC):
    """
    The Bentness station class, manages the relevant records for a particular tube.
    """
    def __init__(self): 
        super().__init__()

    def __str__(self):
        a = "Bentness Data: " + (self.status().name or '') + "\n"
        b = ""

        # We want to print out each record.
        for record in sorted(
                self.m_records, key=lambda i: (i.date is None, i.date)
        ):
            b += record.__str__()

        b = b[:-1]

        # We want to have the return string indent each record, for viewing ease.
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

    def bentness(self):
        if not self.visited():
            return 0.0
        return self.get_record(mode='last').bentness
