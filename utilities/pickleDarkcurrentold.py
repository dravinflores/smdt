
import os
import sys
import pickle
import datetime
import random

from sMDT import db
from sMDT.tube import Tube
from sMDT.data.swage import Swage, SwageRecord
from sMDT.data.tension import Tension, TensionRecord
from sMDT.data.leak import Leak, LeakRecord
from sMDT.data.dark_current import DarkCurrent, DarkCurrentRecord
from sMDT.data.status import ErrorCodes

darkcurrent_directory = "DarkCurrentStation"

CSV_directory = os.path.join('DarkCurrent', '2730V Dark Current')
archive_directory = os.path.join("DarkCurrentStation","archive_old")
new_data_directory = os.path.join("sMDT", "new_data")

datab = db.db()
tubes_in_database = datab.get_IDs()

for directory in [darkcurrent_directory, CSV_directory, archive_directory, new_data_directory]:
    if not os.path.isdir(directory):
        os.mkdir(directory)
added_tubes = []
count = 0
# Step 1: loop over the data that is good, and pickle all of them. Leave the files that don't
#         get pickled. A second pass will happen in step 2.
for filename in os.listdir(CSV_directory):
    put_in_database = False
    with open(os.path.join(CSV_directory, filename)) as CSV_file:
        try:
            sDate = datetime.datetime.strptime(filename, 'data_%d_%m_%Y_%H_%M_%S.csv')
        except ValueError:
            #print("Couldn't read this file " + filename)
            continue
        barcode = None
        for line in CSV_file.readlines():
            voltage = 2730
            if line[0:3] == "MSU":
                if len(line.split(",")) == 1: # This is a single tube test
                    barcode = line.replace("\n","")
                    continue
                elif len(line.split(",")) == 8: # These are multi-tube tests, ignore for now
                    break

            if barcode == None:
                continue  # This skips the test duration for some tests

            if line == '':
                continue  # Some files have this at the end of the file
            
            try:
                darkcurrent = float(line.split(',')[0])
            except ValueError:
                continue
            if darkcurrent == 0:
                continue   # we need to exclude records that might have had the power trip
            added_tubes.append(barcode)
            if barcode not in tubes_in_database: continue
            tube = Tube()
            tube.set_ID(barcode)
            tube.dark_current.add_record(DarkCurrentRecord(dark_current=darkcurrent,
                                                            date=sDate,
                                                            voltage=voltage))

            pickled_filename = str(datetime.datetime.now().timestamp()) + \
                                str(random.randrange(100, 999)) + 'darkcurrentold.tube'

            with open(os.path.join(new_data_directory, pickled_filename), "wb") as f:
                pickle.dump(tube, f)
                put_in_database = True
                count += 1

    if put_in_database:
        os.replace(os.path.join(CSV_directory, filename), os.path.join(archive_directory, filename))
print(str(count) + " tubes were restored through single good tests")
print("END OF GOOD SINGLE TEST DATA")
count = 0
# Step 2: Now we will go over the multi-tube tests and if there are tubes without a dark current,
#         we will do our best and take the average of the multi-tube test current.

# I want to prioritize the most recent data, so I sort the filenames according to date
# and then add the data accordingly
def byDate(filename):
    try:
        date = datetime.datetime.strptime(filename, 'data_%d_%m_%Y_%H_%M_%S.csv')
        return date
    except:
        return datetime.datetime(year=datetime.MAXYEAR,month=1,day=1)
f_multi = open("multi-test tubes.txt","w")


filenames = os.listdir(CSV_directory)
filenames.sort(key=byDate, reverse=True)
for filename in filenames:
    put_in_database = False
    with open(os.path.join(CSV_directory, filename)) as CSV_file:
        try:
            sDate = datetime.datetime.strptime(filename, 'data_%d_%m_%Y_%H_%M_%S.csv')
        except ValueError:
            #print("Couldn't read this file " + filename)
            continue
        barcodes = None
        voltage = 2730
        lines = CSV_file.readlines()

        try:
            if len(lines[0].split(",")) == 8:
                barcodes = lines[0].split(",")
            elif len(lines[1].split(",")) == 8:
                barcodes = lines[1].split(",")
            else:
                #print("Could't read this file: " + filename)
                break   # Can't read file
        except:
            #print("Couldn't read this file: " + filename)
            break # Can't read file
        barcodes[-1] = barcodes[-1].replace("\n","")
        lines.reverse()
        for line in lines: # Read the last numbers
            if line == '':
                continue  # Some files have this at the end of the file
            try:
                darkcurrent = float(line.split(',')[0])
            except ValueError:
                #print("Couldn't read this file: " + filename)
                break
            darkcurrent = darkcurrent/8   # Average over all 8 tubes
            if darkcurrent == 0: # Some entries have no current. We don't trust these because the power
                continue         # supply could have tripped at that point.

            for barcode in barcodes:
                # If the database doesn't have a dark current value for this tube, add it.
                try:
                    if not datab.get_tube(barcode).dark_current.visited() and barcode not in added_tubes:
                        f_multi.write(barcode + "\n")
                        added_tubes.append(barcode)
                        tube = Tube()
                        tube.set_ID(barcode)
                        tube.dark_current.add_record(DarkCurrentRecord(dark_current=darkcurrent,
                                                                        date=sDate,
                                                                        voltage=voltage))
                        tube.new_comment(("This tube's dark current tests were the average of " + str(barcodes), "Jason", datetime.datetime.now(), ErrorCodes(0)))
                        pickled_filename = str(datetime.datetime.now().timestamp()) + \
                                            str(random.randrange(100, 999)) + 'darkcurrentold.tube'

                        with open(os.path.join(new_data_directory, pickled_filename), "wb") as f:
                            pickle.dump(tube, f)
                            put_in_database = True
                        count +=1
                except KeyError:
                    break  # If a tube doesn't exist in the database, then don't add the dark current
            # At this point, a dark current measurement was taken and stored with tubes that didn't
            # have a dark current measurement
            break

    if put_in_database:
        os.replace(os.path.join(CSV_directory, filename), os.path.join(archive_directory, filename))
f_multi.close()
print(str(count) + " tubes were restored from mutli-tube tests")
print("END OF MULTI-TUBE TESTS")
count = 0
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
# Now we turn our attention to the 'bad' data. Here channels may have been turned off and so
# any dark current measurement that is exactly 0 is unreliable. We will loop through and only
# put in nonzero dark currents.
f_bad = open("tubes_recovered_from_bad.txt","w")
CSV_directory = os.path.join('DarkCurrent', 'Bad Data')
archive_directory = os.path.join("DarkCurrentStation","archive_old_bad")
for directory in [darkcurrent_directory, CSV_directory, archive_directory, new_data_directory]:
    if not os.path.isdir(directory):
        os.mkdir(directory)

# Step 1: loop over the data that is good, and pickle all of them. Leave the files that don't
#         get pickled. A second pass will happen in step 2.
for filename in os.listdir(CSV_directory):
    put_in_database = False
    with open(os.path.join(CSV_directory, filename)) as CSV_file:
        try:
            sDate = datetime.datetime.strptime(filename[13:-4], '%d_%m_%Y_%H_%M_%S')
        except ValueError:
            #print("Couldn't read this file " + filename)
            continue
        barcode = None
        for line in CSV_file.readlines():
            voltage = 3015   # This data actually used the correct voltage
            if line[0:3] == "MSU":
                if len(line.split(",")) == 1: # This is a single tube test
                    barcode = line.replace("\n","")
                    continue
                elif len(line.split(",")) == 8: # These are multi-tube tests, ignore for now
                    break

            if barcode == None:
                continue  # This skips the test duration for some tests

            if line == '':
                continue  # Some files have this at the end of the file
     
            darkcurrent = float(line.split(',')[0])
            if darkcurrent == 0:
                continue       # Reject dark current measurements that are 0nA
            f_bad.write(barcode + "\n")
            tube = Tube()
            tube.set_ID(barcode)
            tube.dark_current.add_record(DarkCurrentRecord(dark_current=darkcurrent,
                                                            date=sDate,
                                                            voltage=voltage))
            tube.new_comment(("This tube was in bad data but was recovered", "Jason", datetime.datetime.now(), ErrorCodes(0)))
            pickled_filename = str(datetime.datetime.now().timestamp()) + \
                                str(random.randrange(100, 999)) + 'darkcurrentold.tube'

            with open(os.path.join(new_data_directory, pickled_filename), "wb") as f:
                pickle.dump(tube, f)
                put_in_database = True
            count += 1

    if put_in_database:
        os.replace(os.path.join(CSV_directory, filename), os.path.join(archive_directory, filename))
print(str(count) + " tubes were recovered from the bad tube directory.")
print("END OF BAD TUBE SINGLE TESTS")
f.close()