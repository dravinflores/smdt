###############################################################################
#   File: dict_to_tube_object.py
#   Author(s): Dravin Flores
#   Date Created: 16 April, 2021
#
#   Purpose: Currently, the database is stored as a list of dictionaries. This
#       file houses all of the necessary information to go from a list of
#       dictionaries to a list of tube objects.
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

# Adds the folder that file is in to the system path
sys.path.append(path[:-len(os.path.basename(__file__))])

import tube
import pickle
from pathlib import Path
from datetime import datetime

from data.swage import Swage, SwageTest
from data.tension import Tension, TensionTest
from data.leak import Leak, LeakTest
from data.dark_current import DarkCurrent, DarkCurrentTest

dict_keys = [
    # Keys related to the swage station.
    # Codes run from dict_keys[0] to dict_keys[8].
    "swagerUser",                   # 0
    "rawLength",                    # 1
    "swageLength",                  # 2
    "swagerComment",                # 3
    "swagerDate",                   # 4
    "swagerFile",                   # 5
    "eCode",                        # 6
    "cCode",                        # 7
    "failsSwager",                  # 8

    # Keys related to the tension station.
    # Codes run from dict_keys[9] to dict_keys[22].
    "tensionUser",                  # 9
    "tensionDateTime",              # 10
    "tensionLength",                # 11
    "frequency",                    # 12
    "tensions",                     # 13
    "tensionFile",                  # 14
    "firstTensions",                # 15
    "firstTensionUsers",            # 16
    "firstTensionDates",            # 17
    "failsFirstTension",            # 18
    "secondTensions",               # 19
    "firstTension",                 # 20
    "firstTensionDate",             # 21
    "firstFrequency",               # 22

    # Keys related to the leak station.
    # Codes run from dict_keys[23] to dict_keys[28].
    "leakRate",                     # 23
    "leakStatus",                   # 24
    "leakFile",                     # 25
    "leakDateTime",                 # 26
    "leakUser",                     # 27
    "failsLeak",                    # 28

    # Keys related to the dark current station.
    # Codes run from dict_keys[29] to dict_keys[32].
    "currentTestDates",             # 29
    "currentFile",                  # 30
    "darkCurrents",                 # 31
    "failsCurrent",                 # 32

    # Boolean which flags whether a tube is good or not.
    # This is dict_keys[33].
    "good",                         # 33
]

def open_database():
    # We are creating a pathlib path, which is set to the current working
    # directory.
    smdt_folder = Path()
    db_file = smdt_folder / 'database.p'

    if not db_file.exists():
        ret = None
    else:
        ret = pickle.load(db_file.open('rb'))

    return ret


def get_attribute_alt(get_from):
    try:
        assign_to = get_from
    except KeyError:
        assign_to = []

    return assign_to


def get_attribute(data_dict, key):
    try:
        assign_to = data_dict[key]
    except KeyError:
        assign_to = []

    return assign_to


def string_to_datetime(date_str, fmt):
    try:
        ret = datetime.strptime(date_str, fmt)
    except ValueError:
        ret = None

    return ret


# The difference here is that I want to try a new method.
def dict_to_tube_object():
    dict_db = open_database()

    if dict_db is None:
        return None

    # Time to construct the tube object. We are constructing this tube object
    # outside of the tube class for the time being. This is more for testing
    # purposes. Eventually, this code will be integrated into the tube class.
    list_of_tubes = []

    swage_date_fmt = '%m.%d.%Y_%H_%M_%S'
    tension_date_fmt = '%d.%m.%Y %H.%M.%S'
    leak_date_fmt = '%d.%m.%Y %H.%M.%S'
    dark_current_date_fmt = '%d_%m_%Y_%H_%M_%S'

    # Now we need to start to peel back the layers of the database.
    for (tube_id, data_dict) in dict_db.items():
        # We need this to check whether the data recorded has the particular
        # values that we need.
        recorded_dict_keys = data_dict.keys()

        swager_user           = get_attribute(data_dict, "swagerUser")
        raw_length            = get_attribute(data_dict, "rawLength")
        swage_length          = get_attribute(data_dict, "swageLength")
        swager_comment        = get_attribute(data_dict, "swagerComment")
        swager_date           = get_attribute(data_dict, "swagerDate")
        swager_file           = get_attribute(data_dict, "swagerFile")
        e_code                = get_attribute(data_dict, "eCode")
        c_code                = get_attribute(data_dict, "cCode")
        fails_swager          = get_attribute(data_dict, "failsSwager")

        tension_user          = get_attribute(data_dict, "tensionUser")
        tension_date          = get_attribute(data_dict, "tensionDateTime")
        tension_length        = get_attribute(data_dict, "tensionLength")
        frequency             = get_attribute(data_dict, "frequency")
        tensions              = get_attribute(data_dict, "tensions")
        tension_file          = get_attribute(data_dict, "tensionFile")
        first_tensions        = get_attribute(data_dict, "firstTensions")
        first_tension_users   = get_attribute(data_dict, "firstTensionUsers")
        first_tension_dates   = get_attribute(data_dict, "firstTensionDates")
        fails_first_tension   = get_attribute(data_dict, "failsFirstTension")
        second_tensions       = get_attribute(data_dict, "secondTensions")
        first_tension         = get_attribute(data_dict, "firstTension")
        first_tension_date    = get_attribute(data_dict, "firstTensionDate")
        first_frequency       = get_attribute(data_dict, "firstFrequency")

        leak_rate             = get_attribute(data_dict, "leakRate")
        leak_status           = get_attribute(data_dict, "leakStatus")
        leak_file             = get_attribute(data_dict, "leakFile")
        leak_date             = get_attribute(data_dict, "leakDateTime")
        leak_user             = get_attribute(data_dict, "leakUser")
        fails_leak            = get_attribute(data_dict, "failsLeak")

        current_test_dates    = get_attribute(data_dict, "currentTestDates")
        current_file          = get_attribute(data_dict, "currentFile")
        currents              = get_attribute(data_dict, "darkCurrents")
        fails_current         = get_attribute(data_dict, "failsCurrent")

        bool_flag             = get_attribute(data_dict, "good")

        # Now to construct the tube, the test data, and populate everything.
        tube_construct = tube.Tube()
        tube_construct.m_tube_id = tube_id

        # We will add in the comments. The swage station is the only place
        # where comments can be recorded.
        tube_construct.new_comment(swager_comment)

        ########################################################################
        #   A great test to run here is to check the size of the lists, and
        #   assert that they are the same length. Like the number of tension
        #   dates should match the number of tension files.
        ########################################################################

        # Here we are just getting the number of users.
        number_of_swage_tests = len(swager_user)
        number_of_tension_tests = len(tensions)
        number_of_leak_tests = len(leak_file)
        number_of_dark_current_tests = len(currents)

        # Now we will populate the tests by first constructing these lists, and
        # then constructing the station objects and inserting these lists in.
        list_of_swage_tests = []
        list_of_tension_tests = []
        list_of_leak_tests = []
        list_of_dark_current_tests = []

        for n in range(0, number_of_swage_tests):
            # First we construct the date object.
            date_obj = string_to_datetime(swager_date[n], swage_date_fmt)

            test = SwageTest(
                raw_length = raw_length[n],
                swage_length = swage_length[n],
                clean_code = c_code[n],
                error_code = e_code[n],
                date = date_obj
            )
            list_of_swage_tests.append(test)

        for n in range(0, number_of_tension_tests):
            date_obj = string_to_datetime(tension_date[n], tension_date_fmt)

            test = TensionTest(
                tension = tensions[n],
                frequency = frequency[n],
                date = date_obj,
                data_file = tension_file[n]
            )
            list_of_tension_tests.append(test)

        for n in range(0, number_of_leak_tests):
            try:
                date_obj = string_to_datetime(leak_date[n], leak_date_fmt)
            except IndexError:
                date_obj = None

            test = LeakTest(
                leak_rate = leak_rate[n],
                date = date_obj,
                data_file = leak_file[n]
            )
            list_of_leak_tests.append(test)

        for n in range(0, number_of_dark_current_tests):
            # It appears that the data file names have a '\n' character added
            # to the end. This just serves to fix that issue.
            date_fixed = current_test_dates[n][0:-1]
            date_obj = string_to_datetime(date_fixed, dark_current_date_fmt)

            test = DarkCurrentTest(
                dark_current = currents[n],
                date = date_obj,
                data_file = current_file
            )
            list_of_dark_current_tests.append(test)

        # Here are all of our station objects.
        s = Swage()
        t = Tension()
        l = Leak()
        d = DarkCurrent()

        s.m_users = swager_user
        s.m_tests = list_of_swage_tests

        t.m_users = tension_user
        t.m_tests = list_of_tension_tests

        l.m_users = leak_user
        l.m_tests = list_of_leak_tests

        # d.m_users = data_dict[dict_keys[]]
        d.m_tests = list_of_dark_current_tests

        tube_construct.swage = s
        tube_construct.tension = t
        tube_construct.leak = l
        tube_construct.dark_current = d

        list_of_tubes.append(tube_construct)

    return list_of_tubes


if __name__ == "__main__":
    list_of_tubes = dict_to_tube_object()

    list_of_tubes.sort(key = lambda t: t.getID())

    for tube in list_of_tubes:
        print(tube)
        print("#"*80)
