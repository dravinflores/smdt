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
from datetime import datetime
import textwrap

from .station import Station
from .status import Status
from .record import Record



class LeakRecord(Record):
    """
    Class for objects representing individual records from the Leak station.
    """

    # Here are the project defined limits.
    threshold_leak = 5.0E-5

    def __init__(self, leak_rate=None, date=datetime.now(), user=None):
        super().__init__(user)
        self.leak_rate = leak_rate
        self.date = date

    def __str__(self):
        a = f"Leak Rate: {self.leak_rate}\n"
        b = f"Recorded on: {self.date}\n"
        c = f"Recorded by: {self.user}\n\n"
        return a + b + c

    def fail(self):
        return self.leak_rate > LeakRecord.threshold_leak


class Leak(Station, ABC):
    '''
    The Leak station class, manages the relevant records for a particular tube.
    '''
    def __init__(self):
        super().__init__()

    def __str__(self):
        a = "Leak Data: " + self.status().name + "\n"
        b = ""

        # We want to print out each record.
        for record in sorted(self.m_records, key=lambda i: i.date):
            b += record.__str__()

        b = b[:-1]

        # We want to have the return string indent each record, for viewing ease.
        return a + textwrap.indent(b, '\t') + '\n'

    def fail(self):
        try:
            return self.get_record(mode='last').fail()
        except IndexError:
            return False

    def status(self):
        if not self.visited():
            return Status.INCOMPLETE
        elif self.fail():
            return Status.FAIL
        else:
            return Status.PASS

