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

# Import Preparation block.
# Currently only needed so the tests in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)
current_folder = os.path.dirname(os.path.abspath(__file__))

# Adds the folder that file is in to the system path
sys.path.append(current_folder)


class Record:
    def __init__(self):
        pass

    def fail(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
