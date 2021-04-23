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
           "last"  :  lambda station: station.m_tests[-1],
           "first" :  lambda station: station.m_tests[0]}
def add_mode(name, lam_expr):
        modes[name] = lam_expr

# Import Preparation block.
# Currently only needed so the tests in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)

# Adds the folder that file is in to the system path
sys.path.append(path[:-len(os.path.basename(__file__))])


class Station:
    '''
    Abstract class representing a station that will record data on a tube
    '''
    def __init__(self):
        #WARNING
        #Initially, this init function and the inheriting station's functions looked something like
        #def __init__(self, users=[],tests=[])
        #   self.m_users = users
        #   self.m_tests = tests
        #I dont know why, but this is apparently a terrible idea 
        #that somehow makes the lists in every station ojbect be the same object and share their users and tests.
        #Again, no idea why, I encountered the problem and traced it back here and found that removing it fixed it
        self.m_users = []
        self.m_tests = []

        #I'll document it fully later but this code below 
        #is going to allow application custimizable modes in a really nice way. 

        


    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        ret = type(self)()
        ret.m_users = self.m_users + other.m_users
        ret.m_tests = self.m_tests + other.m_tests
        return ret
      #  return type(self)(self.m_users + other.m_users, self.m_tests + other.m_tests)

    def fail(self, mode="last"):
        raise modes[mode](self).fail()

    def get_users(self):
        """Returns the list of people who have recorded data for this tube at
        this station"""
        return self.m_users

    def add_user(self, user):
        """Adds a user to the station's records"""
        self.m_users.append(user)

    def get_test(self, mode="last"):
        '''Given a selected mode, returns the respective test'''
        return modes[mode](self)

    def set_test(self, test):
        """Adds a test to the station's records"""
        self.m_tests.append(test)

    def fail(self, mode='last'):
        return modes[mode](self).fail()



if __name__ == "__main__":
    from dark_current import DarkCurrentTest
    from datetime import datetime
    station = Station()
    station.set_test(5)
    station.m_tests.append(5)
    station2 = Station()
    station2.m_tests.append(10)
    station2.set_test(3)
    print(station.m_tests)
    print(station.get_test("first"))
    print(station2.m_tests)
    print(station2.get_test("first"))