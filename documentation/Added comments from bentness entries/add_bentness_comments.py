
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

darkcurrent_directory = "BentnessStation"

CSV_directory = os.path.join('BentnessStation', 'archive')

new_data_directory = os.path.join("sMDT", "new_data")

for directory in [darkcurrent_directory, CSV_directory, new_data_directory]:
    if not os.path.isdir(directory):
        os.mkdir(directory)

count = 0
f_comments = open("bentness_comments.txt","w")
for filename in os.listdir(CSV_directory):
    with open(os.path.join(CSV_directory, filename)) as CSV_file:
        try:
            sDate = datetime.datetime.strptime(filename, '%m.%d.%Y_%H_%M_%S.csv')
        except ValueError:
            print("Couldn't read this file " + filename)
            continue
        barcode = None
        for line in CSV_file.readlines():
            split = line.split(",")
            if len(split) != 5: continue
            
            barcode = split[0]
            try:
                date = datetime.datetime.strptime(split[2],'%m.%d.%Y_%H_%M_%S')
            except: continue
            user = split[3]
            comment = split[4]
            if comment == '' or comment == '\n': continue

            f_comments.write(barcode + '\n')
            tube = Tube()
            tube.set_ID(barcode)
            tube.new_comment(((comment, user, date, ErrorCodes(0))))

            pickled_filename = str(datetime.datetime.now().timestamp()) + \
                                str(random.randrange(100, 999)) + 'bentness_comment.tube'

            with open(os.path.join(new_data_directory, pickled_filename), "wb") as f:
                pickle.dump(tube, f)
                put_in_database = True
            count += 1
f_comments.close()

print(str(count) + " comments were added to the database")