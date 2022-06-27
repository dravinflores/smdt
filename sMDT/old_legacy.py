###############################################################################
#   File: old_legacy.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 16 April, 2021
#
#   Purpose: Provides functions for legacy support. Currently, the database is stored as a list of dictionaries. This
#       file houses all of the necessary information to go from a list of
#       dictionaries to a list of tube objects, as well as go backwards and do the inverse operation.
#       
# Updates: 
# 2022-06-27 this used to be legacy.py. This is now only for MSU tubes.
#
###############################################################################


import os
import sys
import pickle
import datetime
import random

from .MSU_only_tube import MSU_only_Tube
from .data.swage import Swage, SwageRecord
from .data.tension import Tension, TensionRecord
from .data.leak import Leak, LeakRecord
from .data.dark_current import DarkCurrent, DarkCurrentRecord
from .data.bent import Bent, BentRecord

from .data.status import ErrorCodes


class station_pickler:
    '''
    This class is designed to facilitate the interface between the database manager and the data generated by the
    stations. This class will take whatever data is generated in the form of a csv file, and will read it into a sMDT
    tube object. It will then pickle the object into the standard specified for new data for the db manager.
    '''

    sMDT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, path, archive=True, logging=True):
        '''
        Constructor, builds the pickler object. Gets the path to the directory it should look for/create the relevant
        files in
        '''
        self.path = path
        self.archive = archive
        self.error_files = {'Swage': set(), 'Tension': set(), 'Leak': set(), 'DarkCurrent': set(), 'Bentness': set()}
        self.logging = logging

    def write_errors(self):
        fp = open("errors.txt", 'a')
        for station in self.error_files:
            if self.error_files[station]:
                fp.write(station + ':\n')
                for filename in self.error_files[station]:
                    fp.write('\t' + filename + '\n')
        fp.close()

    '''
    This is the swage pickler function that will pickle every 
    swage csv file that is in the specified directory swagerDirectory
    '''

    def pickle_swage(self):
        swage_directory = os.path.join(self.path, "SwagerStation")
        archive_directory = os.path.join(swage_directory, "archive")
        CSV_directory = os.path.join(swage_directory, "SwagerData")
        new_data_directory = os.path.join(self.sMDT_DIR, "new_data")

        for directory in [swage_directory, CSV_directory, archive_directory, new_data_directory]:
            if not os.path.isdir(directory):
                os.mkdir(directory)

        for filename in os.listdir(CSV_directory):
            with open(os.path.join(CSV_directory, filename)) as CSV_file:
                if self.archive:
                    archive_file = open(os.path.join(archive_directory, filename), 'a')
                for line in CSV_file.readlines():
                    if self.archive:
                        archive_file.write(line)
                    line = line.split(',')
                    # Here are the different csv types, there have been 3 versions
                    # The currently used version that includes endplug type 'Protvino' or 'Munich'
                    endplug_type = None
                    if len(line) not in [9, 8, 3]:
                        self.error_files['Swage'].add(filename)
                        continue
                    if len(line) == 9:
                        barcode = line[0].replace('\r', '').replace('\n', '')
                        raw_length = float(line[1]) if line[1] != "" else None
                        swage_length = float(line[2]) if line[2] != "" else None
                        sDate = datetime.datetime.strptime(line[3], '%m.%d.%Y_%H_%M_%S')
                        cCode = line[4]
                        eCode = line[5]
                        comment = line[6]
                        user = line[7].replace('\r', '').replace('\n', '')

                        endplug_type = line[8]

                    # An earlier version when endplug type wasn't recorded
                    elif len(line) == 8:
                        barcode = line[0].replace('\r', '').replace('\n', '')
                        raw_length = float(line[1]) if line[1] != "" else None
                        swage_length = float(line[2]) if line[2] != "" else None
                        sDate = datetime.datetime.strptime(line[3], '%m.%d.%Y_%H_%M_%S')
                        cCode = line[4]
                        eCode = line[5]
                        comment = line[6]
                        user = line[7].replace('\r', '').replace('\n', '')
                    # This was the very first iteration where there were only 3 things recorded
                    else:
                        barcode = line[0].replace('\r', '').replace('\n', '')
                        comment = line[1]
                        user = line[2].replace('\r', '').replace('\n', '')
                        raw_length = None
                        swage_length = None
                        eCode = None
                        cCode = None
                        # Swager date was stored in the filename in this version
                        try:
                            sDate = datetime.datetime.strptime(filename, '%d.%m.%Y_%H_%M_%S.csv')
                        except ValueError:
                            try:
                                sDate = datetime.datetime.strptime(filename, '%m.%d.%Y_%H_%M_%S.csv')
                            except ValueError:
                                sDate = None

                    tube = MSU_only_Tube()
                    tube.set_ID(barcode)
                    tube.set_ID(barcode)
                    try:
                        error_code = ErrorCodes(int(eCode[0]))
                    except ValueError:
                        error_code = ErrorCodes(0)
                    except TypeError:
                        error_code = ErrorCodes(0)
                    if comment or error_code != 0:
                        tube.new_comment((comment, user, sDate, error_code))
                    tube.swage.add_record(SwageRecord(raw_length=raw_length,
                                                      swage_length=swage_length,
                                                      clean_code=cCode,
                                                      date=sDate,
                                                      user=user))

                    if endplug_type:
                        tube.legacy_data['is_munich'] = endplug_type == "Munich"

                    pickled_filename = str(datetime.datetime.now().timestamp()) + str(
                        random.randrange(100, 999)) + 'swage.tube'

                    if self.logging:
                        print("Pickling swage data for tube", barcode)

                    # file_lock = locks.Lock(pickled_filename)
                    # file_lock.lock()
                    with open(os.path.join(new_data_directory, pickled_filename), "wb") as f:
                        pickle.dump(tube, f)
                    # file_lock.unlock()

            if self.archive:
                os.remove(os.path.join(CSV_directory, filename))

    '''
    This is the tension pickler function that will pickle every tension csv file 
    that is in the specified directory tensionDirectory
    '''

    def pickle_tension(self):
        tension_directory = os.path.join(self.path, "TensionStation")
        archive_directory = os.path.join(tension_directory, "archive")
        CSV_directory = os.path.join(tension_directory, "output")
        new_data_directory = os.path.join(self.sMDT_DIR, "new_data")

        for directory in [tension_directory, CSV_directory, archive_directory, new_data_directory]:
            if not os.path.isdir(directory):
                os.mkdir(directory)

        for filename in os.listdir(CSV_directory):
            with open(os.path.join(CSV_directory, filename)) as CSV_file:
                if self.archive:
                    archive_file = open(os.path.join(archive_directory, filename), 'a')
                for line in CSV_file.readlines():
                    if line in {',\n', ','} or line[0:11] == "Operator ID":
                        continue

                    if self.archive:
                        archive_file.write(line)

                    line = line.split(',')
                    # Check there are 8 columns, else report to terminal
                    if len(line) == 8:
                        user = line[0]
                        date = line[1]
                        barcode = line[2]
                        # not_used   = line[3]
                        # not_used   = line[4]
                        frequency = float(line[5])
                        tension = float(line[6])
                        # not_used   = line[7]
                    # Report to terminal unknown formats
                    else:
                        if self.logging:
                            print("File " + filename + " has a line with unknown format")
                        self.error_files['Tension'].add(filename)
                        continue

                    try:
                        sDate = datetime.datetime.strptime(filename, 'data_%d.%m.%Y_%H_%M_%S.out')
                    except ValueError:
                        try:
                            sDate = datetime.datetime.strptime(filename, 'data_%m.%d.%Y_%H_%M_%S.out')
                        except ValueError:
                            sDate = None

                    # Create tube instance
                    tube = MSU_only_Tube()
                    tube.set_ID(barcode)

                    if self.logging:
                        print("Pickling tension data for tube", barcode)

                    tube.tension.add_record(TensionRecord(tension=tension,
                                                          frequency=frequency,
                                                          date=sDate,
                                                          user=user))

                    pickled_filename = str(datetime.datetime.now().timestamp()) + str(
                        random.randrange(100, 999)) + 'tension.tube'

                    # Lock and write tube instance to pickle file
                    # file_lock = locks.Lock(pickled_filename)
                    # file_lock.lock()
                    with open(os.path.join(new_data_directory, pickled_filename), "wb") as f:
                        pickle.dump(tube, f)
                    # file_lock.unlock()

            if self.archive:
                os.remove(os.path.join(CSV_directory, filename))

    '''
    This is the leak rate pickler function that will pickle every leak rate csv file 
    that is in the specified directory leakDirectory
    '''

    def pickle_leak(self):
        leak_directory = os.path.join(self.path, "LeakStation")
        CSV_directory = os.path.join(self.path, 'LeakDetector')
        archive_directory = os.path.join(leak_directory, "archive")

        new_data_directory = os.path.join(self.sMDT_DIR, "new_data")

        for directory in [leak_directory, CSV_directory, archive_directory, new_data_directory]:
            if not os.path.isdir(directory):
                os.mkdir(directory)

        for filename in os.listdir(CSV_directory):
            with open(os.path.join(CSV_directory, filename)) as CSV_file:
                if self.archive:
                    archive_file = open(os.path.join(archive_directory, filename), 'a')
                for line in CSV_file.readlines():
                    if self.archive:
                        archive_file.write(line)
                    line = line.split('\t')
                    # Check there are 6 columns, else report to terminal
                    if len(line) == 6:
                        try:
                            leak = float(line[0])
                            pressure = line[1]  # Not used
                            pass_fail = line[2]  # Useless
                            date = line[3]
                            time1 = line[4]
                            user = line[5]
                        except ValueError:
                            self.error_files['Leak'].add(filename)
                            continue
                    # Report to terminal unknown formats
                    else:
                        if self.logging:
                            print("File " + filename + " has line with unknown format")
                        self.error_files['Leak'].add(filename)
                        continue

                    try:
                        sDate = datetime.datetime.strptime(date + time1, '%m/%d/%Y%I:%M %p')
                    except ValueError:
                        sDate = None

                    barcode = filename.split('_')[0]

                    # Create tube instance
                    tube = MSU_only_Tube()
                    tube.set_ID(barcode)
                    tube.leak.add_record(LeakRecord(leak_rate=leak,
                                                    date=sDate, user=user))

                    if self.logging:
                        print("Pickling leak data for tube", barcode)

                    pickled_filename = str(datetime.datetime.now().timestamp()) + str(
                        random.randrange(100, 999)) + 'leak.tube'

                    # Lock and write tube instance to pickle file
                    # file_lock = locks.Lock(pickled_filename)
                    # file_lock.lock()
                    with open(os.path.join(new_data_directory, pickled_filename), "wb") as f:
                        pickle.dump(tube, f)
                    # file_lock.unlock()

            if self.archive:
                os.remove(os.path.join(CSV_directory, filename))

    '''
    This is the dark current pickler function that will pickle every dark current csv file 
    that is in the specified directory darkcurrentDirectory
    '''

    def pickle_darkcurrent(self):

        darkcurrent_directory = os.path.join(self.path, "DarkCurrentStation")

        CSV_directory = os.path.join(self.path, 'DarkCurrent', '3015V Dark Current')
        archive_directory = os.path.join(darkcurrent_directory, "archive")

        new_data_directory = os.path.join(self.sMDT_DIR, "new_data")

        for directory in [darkcurrent_directory, CSV_directory, archive_directory, new_data_directory]:
            if not os.path.isdir(directory):
                os.mkdir(directory)

        for filename in os.listdir(CSV_directory):
            with open(os.path.join(CSV_directory, filename)) as CSV_file:

                tube = MSU_only_Tube()
                barcode = filename.split('.')[0]
                tube.set_ID(barcode)
                if self.archive:
                    archive_file = open(os.path.join(archive_directory, filename), 'a')

                for line in CSV_file.readlines():
                    voltage = None
                    user=""
                    if self.archive:
                        archive_file.write(line)
                    line = line.split(',')
                    # Check there are 2 columns
                    if len(line) == 2:
                        current = float(line[0])
                        date = line[1]
                    elif len(line) == 3:
                        current = float(line[0])
                        date = line[1]
                        voltage = float(line[2])
                    elif len(line) == 4:
                        current = float(line[0])
                        date = line[1]
                        voltage = float(line[2])
                        user = line[3].strip()
                    else:
                        # Report to terminal unknown formats
                        if self.logging:
                            print("File " + filename + " has unknown format")
                        self.error_files['DarkCurrent'].add(filename)
                        continue

                    try:
                        date = date.replace("\n","")
                        sDate = datetime.datetime.strptime(date, '%d_%m_%Y_%H_%M_%S')
                    except ValueError:
                        sDate = None

                    tube.dark_current.add_record(DarkCurrentRecord(dark_current=current,
                                                                   date=sDate,
                                                                   voltage=voltage,user=user))
                    if self.logging:
                        print("Pickling dark current data for tube", barcode)

                    pickled_filename = str(datetime.datetime.now().timestamp()) + str(
                        random.randrange(100, 999)) + 'darkcurrent.tube'

                # Lock and write tube instance to pickle file
                # file_lock = locks.Lock(pickled_filename)
                # file_lock.lock()
                with open(os.path.join(new_data_directory, pickled_filename), "wb") as f:
                    pickle.dump(tube, f)
                # file_lock.unlock()

            if self.archive:
                os.remove(os.path.join(CSV_directory, filename))


    def pickle_bentness(self):

        bentness_directory = os.path.join(self.path, "BentnessStation/")

        CSV_directory = os.path.join(bentness_directory, 'BentnessData')
        archive_directory = os.path.join(bentness_directory, "archive")

        new_data_directory = os.path.join(self.sMDT_DIR, "new_data")

        for directory in [bentness_directory, CSV_directory, archive_directory, new_data_directory]:
            if not os.path.isdir(directory):
                os.mkdir(directory)

        for filename in os.listdir(CSV_directory):
            with open(os.path.join(CSV_directory, filename)) as CSV_file:
                
                if self.archive:
                    archive_file = open(os.path.join(archive_directory, filename), 'a')

                for line in CSV_file.readlines():
                    tube = MSU_only_Tube()
                    if self.archive:
                        archive_file.write(line)
                    line = line.split(',')
                    # Check there are 4 or 5 columns (5th column is comment for some of them)
                    if len(line) == 4 or len(line) == 5:
                        barcode = line[0]
                        bentness = float(line[1])
                        date = line[2]
                        user = line[3]
                        #comment = line[4] # Not used right now
                    # Report to terminal unknown formats
                    else:
                        if self.logging:
                            print("File " + filename + " has unknown format")
                        self.error_files['Bentness'].add(filename)
                        continue

                    try:
                        date = date.replace("\n","")
                        sDate = datetime.datetime.strptime(date, '%m.%d.%Y_%H_%M_%S')
                    except ValueError:
                        sDate = None
                        if self.logging:
                            print("File " + filename + " has unknown format")
                        self.error_files['Bentness'].add(filename)                        
                        continue

                    tube.set_ID(barcode)
                    tube.bent.add_record(BentRecord(bentness=bentness, date=sDate, user=user))
                    if self.logging:
                        print("Pickling bentness data for tube", barcode)

                    pickled_filename = str(datetime.datetime.now().timestamp()) + \
                                       str(random.randrange(100, 999)) + 'bentness.tube'

                    # Lock and write tube instance to pickle file
                    # file_lock = locks.Lock(pickled_filename)
                    # file_lock.lock()
                    with open(os.path.join(new_data_directory, pickled_filename), "wb") as f:
                        pickle.dump(tube, f)
                    # file_lock.unlock()

            if self.archive:
                os.remove(os.path.join(CSV_directory, filename))



            # dict_keys = [
#    # Keys related to the swage station.
#    # Codes run from dict_keys[0] to dict_keys[8].
#    "swagerUser",                   # 0
#    "rawLength",                    # 1
#    "swageLength",                  # 2
#    "swagerComment",                # 3
#    "swagerDate",                   # 4
#    "swagerFile",                   # 5
#    "eCode",                        # 6
#    "cCode",                        # 7
#    "failsSwager",                  # 8

#    # Keys related to the tension station.
#    # Codes run from dict_keys[9] to dict_keys[22].
#    "tensionUser",                  # 9
#    "tensionDateTime",              # 10
#    "tensionLength",                # 11
#    "frequency",                    # 12
#    "tensions",                     # 13
#    "tensionFile",                  # 14
#    "firstTensions",                # 15
#    "firstTensionUsers",            # 16
#    "firstTensionDates",            # 17
#    "failsFirstTension",            # 18
#    "secondTensions",               # 19
#    "firstTension",                 # 20
#    "firstTensionDate",             # 21
#    "firstFrequency",               # 22

#    # Keys related to the leak station.
#    # Codes run from dict_keys[23] to dict_keys[28].
#    "leakRate",                     # 23
#    "leakStatus",                   # 24
#    "leakFile",                     # 25
#    "leakDateTime",                 # 26
#    "leakUser",                     # 27
#    "failsLeak",                    # 28

#    # Keys related to the dark current station.
#    # Codes run from dict_keys[29] to dict_keys[32].
#    "currentTestDates",             # 29
#    "currentFile",                  # 30
#    "darkCurrents",                 # 31
#    "failsCurrent",                 # 32

#    # Boolean which flags whether a tube is good or not.
#    # This is dict_keys[33].
#    "good",                         # 33
# ]

# def open_database():
#    # We are creating a pathlib path, which is set to the current working
#    # directory.
#    smdt_folder = Path()
#    db_file = smdt_folder / 'database.p'

#    if not db_file.exists():
#        ret = None
#    else:
#        ret = pickle.load(db_file.open('rb'))

#    return ret


# def get_attribute_alt(get_from):
#    try:
#        assign_to = get_from
#    except KeyError:
#        assign_to = []

#    return assign_to


# def get_attribute(data_dict, key):
#    try:
#        assign_to = data_dict[key]
#    except KeyError:
#        assign_to = []

#    return assign_to


# def string_to_datetime(date_str, fmt):
#    try:
#        ret = datetime.strptime(date_str, fmt)
#    except ValueError:
#        ret = None

#    return ret


## The difference here is that I want to try a new method.
# def dict_to_tube_object():
#    dict_db = open_database()

#    if dict_db is None:
#        return None

#    # Time to construct the tube object. We are constructing this tube object
#    # outside of the tube class for the time being. This is more for testing
#    # purposes. Eventually, this code will be integrated into the tube class.
#    list_of_tubes = []

#    swage_date_fmt = '%m.%d.%Y_%H_%M_%S'
#    tension_date_fmt = '%d.%m.%Y %H.%M.%S'
#    leak_date_fmt = '%d.%m.%Y %H.%M.%S'
#    dark_current_date_fmt = '%d_%m_%Y_%H_%M_%S'

#    # Now we need to start to peel back the layers of the database.
#    for (tube_id, data_dict) in dict_db.items():
#        # We need this to check whether the data recorded has the particular
#        # values that we need.
#        recorded_dict_keys = data_dict.keys()

#        swager_user           = get_attribute(data_dict, "swagerUser")
#        raw_length            = get_attribute(data_dict, "rawLength")
#        swage_length          = get_attribute(data_dict, "swageLength")
#        swager_comment        = get_attribute(data_dict, "swagerComment")
#        swager_date           = get_attribute(data_dict, "swagerDate")
#        swager_file           = get_attribute(data_dict, "swagerFile")
#        e_code                = get_attribute(data_dict, "eCode")
#        c_code                = get_attribute(data_dict, "cCode")
#        fails_swager          = get_attribute(data_dict, "failsSwager")

#        tension_user          = get_attribute(data_dict, "tensionUser")
#        tension_date          = get_attribute(data_dict, "tensionDateTime")
#        tension_length        = get_attribute(data_dict, "tensionLength")
#        frequency             = get_attribute(data_dict, "frequency")
#        tensions              = get_attribute(data_dict, "tensions")
#        tension_file          = get_attribute(data_dict, "tensionFile")
#        first_tensions        = get_attribute(data_dict, "firstTensions")
#        first_tension_users   = get_attribute(data_dict, "firstTensionUsers")
#        first_tension_dates   = get_attribute(data_dict, "firstTensionDates")
#        fails_first_tension   = get_attribute(data_dict, "failsFirstTension")
#        second_tensions       = get_attribute(data_dict, "secondTensions")
#        first_tension         = get_attribute(data_dict, "firstTension")
#        first_tension_date    = get_attribute(data_dict, "firstTensionDate")
#        first_frequency       = get_attribute(data_dict, "firstFrequency")

#        leak_rate             = get_attribute(data_dict, "leakRate")
#        leak_status           = get_attribute(data_dict, "leakStatus")
#        leak_file             = get_attribute(data_dict, "leakFile")
#        leak_date             = get_attribute(data_dict, "leakDateTime")
#        leak_user             = get_attribute(data_dict, "leakUser")
#        fails_leak            = get_attribute(data_dict, "failsLeak")

#        current_test_dates    = get_attribute(data_dict, "currentTestDates")
#        current_file          = get_attribute(data_dict, "currentFile")
#        currents              = get_attribute(data_dict, "darkCurrents")
#        fails_current         = get_attribute(data_dict, "failsCurrent")

#        bool_flag             = get_attribute(data_dict, "good")

#        # Now to construct the tube, the test data, and populate everything.
#        tube_construct = tube.MSU_only_Tube()
#        tube_construct.m_tube_id = tube_id

#        # We will add in the comments. The swage station is the only place
#        # where comments can be recorded.
#        tube_construct.new_comment(swager_comment)

#        ########################################################################
#        #   A great test to run here is to check the size of the lists, and
#        #   assert that they are the same length. Like the number of tension
#        #   dates should match the number of tension files.
#        ########################################################################

#        # Here we are just getting the number of users.
#        number_of_swage_tests = len(swager_user)
#        number_of_tension_tests = len(tensions)
#        number_of_leak_tests = len(leak_file)
#        number_of_dark_current_tests = len(currents)

#        # Now we will populate the tests by first constructing these lists, and
#        # then constructing the station objects and inserting these lists in.
#        list_of_swage_tests = []
#        list_of_tension_tests = []
#        list_of_leak_tests = []
#        list_of_dark_current_tests = []

#        for n in range(0, number_of_swage_tests):
#            # First we construct the date object.
#            date_obj = string_to_datetime(swager_date[n], swage_date_fmt)

#            test = SwageRecord(
#                raw_length = raw_length[n],
#                swage_length = swage_length[n],
#                clean_code = c_code[n],
#                error_code = e_code[n],
#                date = date_obj
#            )
#            list_of_swage_tests.append(test)

#        for n in range(0, number_of_tension_tests):
#            date_obj = string_to_datetime(tension_date[n], tension_date_fmt)

#            test = TensionTest(
#                tension = tensions[n],
#                frequency = frequency[n],
#                date = date_obj,
#                data_file = tension_file[n]
#            )
#            list_of_tension_tests.append(test)

#        for n in range(0, number_of_leak_tests):
#            try:
#                date_obj = string_to_datetime(leak_date[n], leak_date_fmt)
#            except IndexError:
#                date_obj = None

#            test = LeakTest(
#                leak_rate = leak_rate[n],
#                date = date_obj,
#                data_file = leak_file[n]
#            )
#            list_of_leak_tests.append(test)

#        for n in range(0, number_of_dark_current_tests):
#            # It appears that the data file names have a '\n' character added
#            # to the end. This just serves to fix that issue.
#            date_fixed = current_test_dates[n][0:-1]
#            date_obj = string_to_datetime(date_fixed, dark_current_date_fmt)

#            test = DarkCurrentTest(
#                dark_current = currents[n],
#                date = date_obj,
#                data_file = current_file
#            )
#            list_of_dark_current_tests.append(test)

#        # Here are all of our station objects.
#        s = Swage()
#        t = Tension()
#        l = Leak()
#        d = DarkCurrent()

#        s.m_users = swager_user
#        s.m_tests = list_of_swage_tests

#        t.m_users = tension_user
#        t.m_tests = list_of_tension_tests

#        l.m_users = leak_user
#        l.m_tests = list_of_leak_tests

#        # d.m_users = data_dict[dict_keys[]]
#        d.m_tests = list_of_dark_current_tests

#        tube_construct.swage = s
#        tube_construct.tension = t
#        tube_construct.leak = l
#        tube_construct.dark_current = d

#        list_of_tubes.append(tube_construct)

#    return list_of_tubes


# if __name__ == "__main__":
#    list_of_tubes = dict_to_tube_object()

#    list_of_tubes.sort(key = lambda t: t.getID())

#    for tube in list_of_tubes:
#        print(tube)
#        print("#"*80)
