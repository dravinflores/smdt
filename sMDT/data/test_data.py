###############################################################################
#   File: test_data.py
#   Author(s): Paul Johnecheck
#   Date Created: 19 April, 2021
#
#   Purpose: This is the parent class of the various station's tests.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

import os
import sys
path = os.path.realpath(__file__)
sys.path.append(path[:-len(os.path.basename(__file__))])

class Test_data():
    def __init__(self):
        pass
    def fail():
        raise NotImplementedError
    def __str__():
        raise NotImplementedError
