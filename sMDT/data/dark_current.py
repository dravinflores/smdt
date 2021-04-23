###############################################################################
#   File: dark-current.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 06 April, 2021
#
#   Purpose: This file houses the dark current test station class. This class
#       stores the data collected from the dark current test station into
#       an object.
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

class DarkCurrentTest(Test_data):
    '''
    Class for objects representing individual tests from the Dark Current station.
    '''
    def __init__(self, dark_current=None, timedate=datetime.now()):
        super().__init__()
        self.dark_current = dark_current
        self.timedate = timedate

    def fail():
        #TODO
        pass
    def __str__(self):
        return "Dark Current: {}\nRecorded on {}\n".format(self.dark_current, self.timedate)


class DarkCurrent(Station):
    '''
    Class for objects representing individual tests from the Dark Current station.
    '''
    def __init__(self):
        super().__init__()

    def __str__(self):
        pass


if __name__ == "__main__":
    dark_current1 = DarkCurrent()
    dark_current1.test = "test"
    dark_current1.set_test(DarkCurrentTest(15,  timedate=datetime.now()))
    dark_current2 = DarkCurrent()
    dark_current2.test = "test2"
    dark_current2.set_test(DarkCurrentTest(3,  timedate=datetime.now()))
    print(dark_current1.get_test())
    print(dark_current1.m_tests)
    print(dark_current2.get_test())
    print(dark_current2.m_tests)