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
from datetime import datetime
import textwrap

from .station import Station
from .record import Record
from .status import Status



class DarkCurrentRecord(Record):
    """
    Class for objects representing individual records from the Dark Current station.
    """

    # Here are the project defined limits.
    max_individual_current = 1E-9   # 1 nA
    max_collective_current = 8E-9   # 8 nA

    def __init__(self, dark_current=None, date=datetime.now(), user=None):
        super().__init__(user)
        self.dark_current = dark_current
        self.date = date

    def __str__(self):
        a = f"Dark Current: {self.dark_current}\n"
        b = f"Recorded on: {self.date}\n"
        c = f"Recorded by: {self.user}\n\n"
        return a + b + c

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
        a = "Dark Current Data:  " + self.status().name + "\n"
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

