###############################################################################
#   File: record.py
#   Author(s): Paul Johnecheck
#   Date Created: 19 April, 2021
#
#   Purpose: This is the parent class of the various station's records.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################


class Record:
    def __init__(self, user=None):
        self.user = user

    def fail(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
