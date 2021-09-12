###############################################################################
#   File: delivered.py
#   Author(s): Reinhard Schwienhorst
#   Date Created: August 2021
#
#   Purpose: This file stores the information on whether a tube has been
#   delivered to UMich. It is based on bent.py
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################
from abc import ABC
from datetime import datetime

from .status import Status
from .record import Record


class Delivered(Record):
    """
    Class for objects representing individual records on tube delivery to UMich.
    """

    # Does this format for a long list of parameters look cleaner?
    def __init__(self, delivered=None, date=datetime.now(), user=None):

        # Call the super class init to construct the object.
        super().__init__(user)
        self.date = date 
        self.delivered = delivered

    def fail(self):
        if self.delivered is None:
            return True
        else:
            return False

    def __str__(self):
        # Using string concatenation here.
        a = f"Tube has been delivered to University of Michigan\n"
        b = f"Packaged for delivery on: {self.date}\n"
        c = f"Packaged by: {self.user}\n\n"
        if self.delivered is None:
            return_str = f"Tube has not been delivered yet.\n\n"
        else:
            return_str = a + b + c
        return return_str

