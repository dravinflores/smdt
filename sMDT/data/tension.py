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
# Currently only needed so the tests in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
# Adds the folder that file is in to the system path
sys.path.append(DATA_DIR)

from station import Station
from status import Status
from record import Record
import datetime
import textwrap


class TensionRecord(Record):
    """
    Class for objects representing individual records from the Tension station.
    """

    # Here are the project defined limits.
    max_tension = 350 + 15
    min_tension = 350 - 15

    def __init__(self, tension=None, frequency=None,
                 date=datetime.datetime.now(), user=None):
        super().__init__(user)
        self.tension = tension
        self.frequency = frequency
        self.date = date

    def fail(self):
        if self.tension < TensionRecord.min_tension \
                or self.tension > TensionRecord.max_tension:
            return True
        else:
            return False

    def __str__(self):
        a = f"Tension: {self.tension}\n"
        b = f"Frequency: {self.frequency}\n"
        c = f"Recorded on: {self.date}\n"
        return a + b + c



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

    def passed_first_tension(self):
        return any([not i.fail() for i in self.m_records])

    def passed_second_tension(self):
        found_first_tension = False
        first_tension_date = None
        two_weeks = datetime.timedelta(days=14)
        for record in sorted(self.m_records, key=lambda i: i.date):
            if not record.fail():
                if found_first_tension:
                    delta = record.date - first_tension_date
                    if delta > two_weeks:
                        return True
                else:
                    found_first_tension = True
                    first_tension_date = record.date
        return False


    def status(self):
        if not self.visited():
            return Status.INCOMPLETE
        if self.passed_second_tension():
            return Status.PASS
        else:
            for record in sorted(self.m_records, key=lambda i: i.date):
                if not record.fail():
                    two_weeks = datetime.timedelta(days=14)
                    delta = datetime.datetime.now() - record.date
                    if delta < two_weeks:
                        return Status.INCOMPLETE
                    else:
                        break
            return Status.FAIL

    def fail(self):
        return self.status() == Status.FAIL




if __name__ == "__main__":
    tension = Tension()
    tension.set_record(TensionRecord(15, 0.0005, datetime.datetime.now()))
    tension.set_record(TensionRecord(3, 134.56, datetime.datetime.now()))
    # print(tension.get_record())
    # print(tension.get_record("first"))
    print(tension)