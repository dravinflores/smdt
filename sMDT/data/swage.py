###############################################################################
#   File: swage.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 02 April, 2021
#
#   Purpose: This file houses the swager station class. This class stores the
#       data collected from the swager station into an object.
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
from test_data import Test_data


class SwageTest(Test_data):
    '''
    Class for objects representing individual tests from the Swage station.
    '''
    def __init__(self, raw_length=None, swage_length=None, clean_code=None, error_code=None):
        super().__init__()
        self.raw_length = raw_length
        self.swage_length = swage_length
        self.clean_code = clean_code
        self.error_code = error_code

    def fail():
        #TODO
        pass
    def __str__(self):
        return "Raw Length: {}\nSwage Length: {}\n{}\n{}".format(self.raw_length, self.swage_length, self.clean_code, self.error_code)


class Swage(Station):
    '''
    The Swage station class, manages the relevant tests for a particular tube.
    '''
    def __init__(self, users=[], tests=[]): 
            super().__init__(users, tests)


if __name__ == "__main__":
    swage = Swage()
    swage.set_test(SwageTest(raw_length=3.4, swage_length=3.2, clean_code=None, error_code=None))
    swage.set_test(SwageTest(raw_length=5.2, swage_length=8., clean_code=None, error_code=None))
    print(swage.get_test())
    print(swage.get_test("first"))