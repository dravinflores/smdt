###############################################################################
#   File: leak.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 06 April, 2021
#
#   Purpose: This file houses the leak test station class. This class stores the
#       data collected from the leak test station into an object.
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



class LeakTest(Test_data):
    '''
    Class for objects representing individual tests from the Leak station.
    '''
    def __init__(self, leak_rate=None, timedate=datetime.now()):
        self.leak_rate = leak_rate
        self.timedate = timedate

    def fail(self):
        #TODO
        pass

    def __str__(self):
        return "Leak Rate: {}\nRecorded at {}\n".format(self.leak_rate, self.timedate)



class Leak(Station):
    '''
    The Leak station class, manages the relevant tests for a particular tube.
    '''
    def __init__(self, users=[], tests=[]):
        super().__init__(users, tests)

    def __str__(self):
        pass



if __name__ == "__main__":
    leak = Leak()
    leak.set_test(LeakTest(leak_rate=0.0001, timedate=datetime.now()))
    leak.set_test(LeakTest(leak_rate=3, timedate=datetime.now()))
    print(leak.get_test())
    print(leak.get_test("first"))