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

#Import Preparation block. 
#Currently only needed so the tests in the mains work with the current imports.
import os #This might cause problems on non-windows computers. #WorksOnMyMachine
import sys #This can eventually be removed once this code will only be executed with CWD outside the package itself.
path = os.path.realpath(__file__) #gets the path of the current file being executed
sys.path.append(path[:-len(os.path.basename(__file__))]) #adds the folder that file is in to the system path



class Station:
    '''
    Abstract class representing a station that will record data on a tube
    '''
    def __init__(self, users=[], tests=[]):
        self.m_users = users
        self.m_tests = tests

        #I'll document it fully later but this code below 
        #is going to allow application custimizable modes in a really nice way. 

        self.modes = {
           "last"  :  lambda station: station.m_tests[-1],
           "first" :  lambda station: station.m_tests[0]}

    def add_mode(name, lam_expr):
        self.modes[name] = lam_expr

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()

    def fail(self):
        raise NotImplementedError

    def get_users(self):
        '''Returns the list of people who have recorded data for this tube at this station'''
        return self.m_users

    def add_user(self, user):
        '''Adds a user to the station's records'''
        self.m_users.append(user)

    def get_test(self, mode='last'):
        '''Given a selected mode, returns the respective test'''
        return self.modes[mode](self)

    def set_test(self, test):
        '''Adds a test to the station's records'''
        self.m_tests.append(test)


if __name__ == "__main__":
    station = Station(tests=[0,5])
    print(station.get_test())
    print(station.get_test("first"))
