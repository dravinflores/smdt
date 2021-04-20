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

#Import Preparation block. 
#Currently only needed so the tests in the mains work with the current imports.
import os #This might cause problems on non-windows computers. #WorksOnMyMachine
import sys #This can eventually be removed once this code will only be executed with CWD outside the package itself.
path = os.path.realpath(__file__) #gets the path of the current file being executed
sys.path.append(path[:-len(os.path.basename(__file__))]) #adds the folder that file is in to the system path

from station import Station
from datetime import datetime
from test_data import Test_data


class TensionTest(Test_data):
    '''
    Class for objects representing individual tests from the Tension station.
    '''
    def __init__(self, tension=None, frequency=None, timedate=datetime.now()):
        super().__init__()
        self.tension = tension
        self.frequency = frequency
        self.timedate = timedate

    def fail():
        #TODO
        pass
    def __str__(self):
        return "Tension: {}\nFrequency: {}\nRecorded on {}\n".format(self.tension, self.frequency, self.timedate)


class Tension(Station):
    '''
    Class for objects representing individual tests from the Tension station.
    '''
    def __init__(self, users=[], tests=[]):
        super().__init__(users, tests)

    def __str__(self):
        pass


if __name__ == "__main__":
    tension = Tension()
    tension.set_test(TensionTest(15, 0.0005, timedate=datetime.now()))
    tension.set_test(TensionTest(3, 134.56, timedate=datetime.now()))
    print(tension.get_test())
    print(tension.get_test("first"))