###############################################################################
#   File: db.py
#   Author(s): Paul Johnecheck
#   Date Created: 11 April, 2021
#
#   Purpose: This is the class representing the database.
#    It will act as the main interface for reading and writing to the database. 
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################


# Import Preparation block.
# Currently only needed so the records in the mains work with the current imports.
import os
import sys

# Adds the folder that file is in to the system path
sMDT_DIR = os.path.dirname(os.path.abspath(__file__))
containing_dir = os.path.dirname(sMDT_DIR)
sys.path.append(sMDT_DIR)


from tube import Tube
from data.swage import SwageRecord
from data.tension import TensionRecord
from data.leak import LeakRecord
from data.dark_current import DarkCurrentRecord
from legacy import station_pickler
import locks
import shelve
import pickle
import time
import datetime
import random
import re

class db:

    def __init__(self, db_path=os.path.join(containing_dir, "database.s")):
        '''
        Constructor, builds the database object. Gets the path to the database
        '''
        self.path = db_path
        
    def size(self):
        '''
        Return the integer size of the database. May wait for the database to be unlocked
        '''
        db_lock = locks.Lock("database")
        db_lock.wait()
        tubes = shelve.open(self.path)
        ret_size = len(tubes)
        tubes.close()
        return ret_size
        
       
    def add_tube(self, tube: Tube()):
        '''
        Adds tube to the database. It does so by pickling the tube,
        and adding it to the new_data file for the database manager to add to the database with update()
        '''
        
        dt = datetime.datetime.now()
        timestamp = dt.timestamp()

        filename = str(timestamp) + str(random.randrange(0,999)) + ".tube"


        new_data_path = os.path.join(sMDT_DIR, "new_data")
        
        if not os.path.isdir(new_data_path):
            os.mkdir(new_data_path)

        file_lock = locks.Lock(filename)
        file_lock.lock()
        with open(os.path.join(new_data_path, filename),"wb") as f:
            pickle.dump(tube, f)
        file_lock.unlock()

    def get_tube(self, id):
        '''
        Returns the tube specified by id. May wait for the database to be unlocked.
        '''
        db_lock = locks.Lock("database")
        db_lock.wait()
        tubes = shelve.open(self.path)
        try:
            ret_tube = tubes[id]
        except KeyError:
            tubes.close()
            raise KeyError
        tubes.close()
        return ret_tube

   



class db_manager():
    def __init__(self, db_path=os.path.join(os.path.dirname(sMDT_DIR), "database.s"), archive=False):
        '''
        Constructor, builds the database manager object. Gets the path to the database
        '''
        self.path = db_path
        self.archive = archive

    def wipe(self, confirm=False):
        '''
        Wipes the database. confirm must be "confirm" to proceed. 
        Excercise extreme caution with this, but it is necessary for many test cases.
        '''
        if confirm == 'confirm':
            db_lock = locks.Lock("database")
            db_lock.lock()

            tubes = shelve.open(self.path, flag='n')

            tubes.close()

            db_lock.unlock()

    def update(self):
        '''
        Updates the database by looking for .p files in the new_data directory.
        They should be pickled tubes, and they will be added to the database
        Needs to be ran after a db object calls add_tube(), otherwise the database will not contain the data in time for get_tube()
        '''

        dropbox_folder = os.path.dirname(sMDT_DIR)


        pickler = station_pickler(dropbox_folder, archive=self.archive)
        pickler.pickle_swage()
        pickler.pickle_tension()
        pickler.pickle_leak()
        pickler.pickle_darkcurrent()
        pickler.write_errors()



        #Lock the database
        db_lock = locks.Lock("database")
        db_lock.lock()


        new_data_path = os.path.join(sMDT_DIR, "new_data")

        with shelve.open(self.path) as tubes:

            count = 0
            for filename in os.listdir(new_data_path): 
                if filename.endswith(".tube"):
                    file_lock = locks.Lock(filename)
                    file_lock.wait()
                    new_data_file = open(os.path.join(new_data_path, filename), 'rb')   #open the file
                    tube = pickle.load(new_data_file)                                   #load the tube from pickle
                    new_data_file.close()                                               #close the file

                    print("Loading tube", tube.getID(), "into database.")

                    if tube.getID() in tubes:                                           #add the tubes to the database
                        temp = tubes[tube.getID()] + tube                           
                        tubes[tube.getID()] = temp                          
                    else:
                        tubes[tube.getID()] = tube
                    os.remove(os.path.join(new_data_path, filename))                 #delete the file that we added the tube from
                    count += 1
            t = time.localtime()
            print("Added", count, "tubes at", time.strftime("%H:%M:%S",t))

        #unlock the database
        db_lock.unlock()
