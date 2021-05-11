###############################################################################
#   File: station.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 02 April, 2021
#
#   Purpose: This file houses the base class that all station classes will
#       inherit from.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

modes = {
    "last"  :  lambda station: station.m_records[-1],
    "first" :  lambda station: station.m_records[0]
}


def add_mode(name, lam_expr):
    modes[name] = lam_expr

# Import Preparation block.
# Currently only needed so the records in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)

# Adds the folder that file is in to the system path
sys.path.append(path[:-len(os.path.basename(__file__))])


class Station:
    """
    Abstract class representing a station that will record data on a tube
    """
    def __init__(self):
        # WARNING
        # Initially, this init function and the inheriting station's functions
        # looked something like
        # def __init__(self, users=[],records=[])
        #   self.m_users = users
        #   self.m_records = records
        # I don't know why, but this is apparently a terrible idea
        # that somehow makes the lists in every station object be the same
        # object and share their users and records. Again, no idea why, I
        # encountered the problem and traced it back here and found that
        # removing it fixed it
        self.m_users = []
        self.m_records = []

        # I'll document it fully later but this code below
        # is going to allow application customizable modes in a really nice way.

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        ret = type(self)()
        ret.m_users = self.m_users + other.m_users
        ret.m_records = self.m_records + other.m_records
        return ret
        # Return
        # type(self)(self.m_users + other.m_users, self.m_records + other.m_records)

    def fail(self, mode="last"):
        raise modes[mode](self).fail()

    def get_users(self):
        """Returns the list of people who have recorded data for this tube at
        this station"""
        return self.m_users

    def add_user(self, user):
        """Adds a user to the station's records"""
        self.m_users.append(user)

    def get_record(self, mode="last"):
        """Given a selected mode, returns the respective record"""
        return modes[mode](self)

    def set_record(self, record):
        """Adds a record to the station's records"""
        self.m_records.append(record)



