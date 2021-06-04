
import os
import sys
import pickle
import datetime
import random

from sMDT.tube import Tube
from sMDT.data.swage import Swage, SwageRecord
from sMDT.data.tension import Tension, TensionRecord
from sMDT.data.leak import Leak, LeakRecord
from sMDT.data.dark_current import DarkCurrent, DarkCurrentRecord


darkcurrent_directory = "DarkCurrentStation"

CSV_directory = os.path.join('DarkCurrent', '2730V Dark Current')
archive_directory = os.path.join("archive_old")

new_data_directory = os.path.join("sMDT", "new_data")
print("new data directory: " + new_data_directory)
print("Archive directory: " + archive_directory)
print("Csv file: " + CSV_directory)
for directory in [darkcurrent_directory, CSV_directory, archive_directory, new_data_directory]:
    if not os.path.isdir(directory):
        os.mkdir(directory)

for filename in os.listdir(CSV_directory):
    with open(os.path.join(CSV_directory, filename)) as CSV_file:
        try:
            sDate = datetime.datetime.strptime(filename, 'data_%d_%m_%Y_%H_%M_%S.csv')
        except ValueError:
            print("Couldn't read this file " + filename)
            continue
        print(filename)
        barcode = None
        for line in CSV_file.readlines():
            voltage = 2730


            if line[0:3] == "MSU":
                if len(line.split(",")) == 1: # This is a single tube test
                    barcode = line.replace("\n","")
                    continue
                else:                          # Reject group tests
                    break
            if barcode == None: # This skips the test duration for some tests
                continue
            if line == '':
                continue
            print(filename)                 
            darkcurrent = float(line.split(',')[0])

            tube = Tube()
            tube.set_ID(barcode)
            tube.dark_current.add_record(DarkCurrentRecord(dark_current=darkcurrent,
                                                            date=sDate,
                                                            voltage=voltage))

            pickled_filename = str(datetime.datetime.now().timestamp()) + \
                                str(random.randrange(100, 999)) + 'darkcurrentold.tube'

            # Lock and write tube instance to pickle file
            # file_lock = locks.Lock(pickled_filename)
            # file_lock.lock()
            with open(os.path.join(new_data_directory, pickled_filename), "wb") as f:
                pickle.dump(tube, f)
            # file_lock.unlock()