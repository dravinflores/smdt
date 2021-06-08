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

import shelve
import pickle
import time
import datetime
import random
import os
import sys

from .tube import Tube
from .data.swage import SwageRecord
from .data.tension import TensionRecord
from .data.leak import LeakRecord
from .data.dark_current import DarkCurrentRecord
from .legacy import station_pickler
from . import locks


class db:
    sMDT_DIR = os.path.dirname(os.path.abspath(__file__))
    containing_dir = os.path.dirname(sMDT_DIR)

    def __init__(self, db_path=os.path.join(containing_dir, "database.s")):
        """
        Constructor, builds the database object. Gets the path to the database
        """
        self.path = db_path

    def size(self):
        """
        Return the integer size of the database. May wait for the database to be unlocked
        """
        db_lock = locks.Lock("database")
        db_lock.wait()
        tubes = shelve.open(self.path)
        ret_size = len(tubes)
        tubes.close()
        return ret_size

    def add_tube(self, tube: Tube()):
        """
        Adds tube to the database. It does so by pickling the tube,
        and adding it to the new_data file for the database manager to add to the database with update()
        """

        dt = datetime.datetime.now()
        timestamp = dt.timestamp()

        filename = str(timestamp) + str(random.randrange(0, 999)) + ".tube"

        new_data_path = os.path.join(self.sMDT_DIR, "new_data")

        if not os.path.isdir(new_data_path):
            os.mkdir(new_data_path)

        file_lock = locks.Lock(filename)
        file_lock.lock()
        with open(os.path.join(new_data_path, filename), "wb") as f:
            pickle.dump(tube, f)
        file_lock.unlock()

    def get_tube(self, id):
        """
        Returns the tube specified by id. May wait for the database to be unlocked.
        """
        #db_lock = locks.Lock("database")
        #db_lock.wait()
        tubes = shelve.open(self.path)
        try:
            ret_tube = tubes[id]
        except KeyError:
            tubes.close()
            raise KeyError
        tubes.close()
        return ret_tube

    def get_tubes(self, selection=None):
        tubes = shelve.open(self.path)
        if selection:
            ret_tubes = []
            for ID in selection:
                try:
                    ret_tubes.append(tubes[ID])
                except KeyError:
                    pass
        else:
            ret_tubes = list(tubes.values())
        tubes.close()
        return ret_tubes


    def get_IDs(self):
        db_lock = locks.Lock("database")
        db_lock.wait()
        tubes = shelve.open(self.path)
        ret_ids = list(tubes.keys())
        tubes.close()
        return ret_ids

    def delete_tube(self, tube_id):
        if type(tube_id) == str:
            ID = tube_id
        else:
            ID = tube_id.get_ID()
        dt = datetime.datetime.now()
        timestamp = dt.timestamp()
        filename = str(timestamp) + str(random.randrange(0, 999)) + ".del.tube"
        new_data_path = os.path.join(self.sMDT_DIR, "new_data")

        if not os.path.isdir(new_data_path):
            os.mkdir(new_data_path)

        tube = Tube()
        tube.set_ID(ID)

        file_lock = locks.Lock(filename)
        file_lock.lock()
        with open(os.path.join(new_data_path, filename), "wb") as f:
            pickle.dump(tube, f)
        file_lock.unlock()

    def overwrite_tube(self, tube):
        dt = datetime.datetime.now()
        timestamp = dt.timestamp()

        filename = str(timestamp) + str(random.randrange(0, 999)) + ".edit.tube"

        new_data_path = os.path.join(self.sMDT_DIR, "new_data")

        if not os.path.isdir(new_data_path):
            os.mkdir(new_data_path)

        file_lock = locks.Lock(filename)
        file_lock.lock()
        with open(os.path.join(new_data_path, filename), "wb") as f:
            pickle.dump(tube, f)
        file_lock.unlock()

class db_manager():
    sMDT_DIR = os.path.dirname(os.path.abspath(__file__))
    containing_dir = os.path.dirname(sMDT_DIR)
    DROPBOX_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(DROPBOX_DIR)

    def __init__(self, db_path=os.path.join(containing_dir, "database.s"), archive=True, testing=False):
        """
        Constructor, builds the database manager object. Gets the path to the database
        """
        self.path = db_path
        self.archive = archive
        self.testing = testing

    def wipe(self, confirm=False):
        """
        Wipes the database. confirm must be "confirm" to proceed. 
        Exercise extreme caution with this, but it is necessary for many test cases.
        """
        if confirm == 'confirm':
            db_lock = locks.Lock("database")
            db_lock.lock()

            tubes = shelve.open(self.path, flag='n')

            tubes.close()

            db_lock.unlock()
        else:
            raise RuntimeError

    def cleanup(self) -> None:
        new_data_path = os.path.join(self.sMDT_DIR, "new_data")
        if not os.path.isdir(new_data_path):
            os.mkdir(new_data_path)
        for filename in os.listdir(new_data_path):
            os.remove(os.path.join(new_data_path, filename))
        locks.Lock.cleanup()

    def update(self, logging=True):
        """
        Updates the database by looking for .p files in the new_data directory.
        They should be pickled tubes, and they will be added to the database
        Needs to be ran after a db object calls add_tube(), otherwise the database will not contain the data in time for get_tube()
        """

        # dropbox_folder = os.path.dirname(sMDT_DIR)

        if not self.testing:
            pickler = station_pickler(os.path.dirname(self.path), archive=self.archive, logging=logging)
            pickler.pickle_swage()
            pickler.pickle_tension()
            pickler.pickle_leak()
            pickler.pickle_darkcurrent()
            pickler.pickle_bentness()
            pickler.write_errors()


        # Lock the database
       # db_lock = locks.Lock("database")
       # db_lock.lock()

        new_data_path = os.path.join(self.sMDT_DIR, "new_data")

        with shelve.open(self.path) as tubes:

            addcount = editcount = delcount = 0
            log_activity = open('activity.log','a')
            t = time.localtime()
            for filename in os.listdir(new_data_path):
                new_data_file = open(os.path.join(new_data_path, filename), 'rb')  # open the file
                tube = pickle.load(new_data_file)  # load the tube from pickle
                new_data_file.close()  # close the file

                if filename.endswith(".del.tube"):
                    if tube.get_ID() in tubes:
                        del tubes[tube.get_ID()]
                        if logging:
                            log_activity.write(time.strftime("%d-%b-%Y %H:%M:%S", t) + "\tDeleting tube " + tube.get_ID() + " from database.\n")
                            print("Deleting tube", tube.get_ID(), "from database.")
                            delcount += 1
                    else:
                        if logging:
                            log_activity.write(time.strftime("%d-%b-%Y %H:%M:%S", t) + "\tAttempted to delete tube " + tube.get_ID() + ", tube not found.\n")
                            print("Attempted to delete tube", tube.get_ID(), ", tube not found.")

                elif filename.endswith(".edit.tube"):
                    if logging:
                        log_activity.write(time.strftime("%d-%b-%Y %H:%M:%S", t) + "\tRewriting the data of " + tube.get_ID() + " due to edit\n")
                        print("Rewriting the data of", tube.get_ID(), "due to edit")
                        editcount += 1
                    tubes[tube.get_ID()] = tube


                elif filename.endswith(".tube"):
                    if logging:
                        log_activity.write(time.strftime("%d-%b-%Y %H:%M:%S", t) + "\tLoading tube or adding data to " + tube.get_ID() + " into database.\n")
                        print("Loading tube", tube.get_ID(), "into database.")

                    if tube.get_ID() in tubes:  # add the tubes to the database
                        temp = tubes[tube.get_ID()] + tube
                        tubes[tube.get_ID()] = temp
                    else:
                        tubes[tube.get_ID()] = tube

                    addcount += 1
                else:
                    if logging:
                        print("Unrecognized file type in new_data folder")

                os.remove(os.path.join(new_data_path, filename))  # delete the file that we added the tube from
            t = time.localtime()
            if logging:
                print(addcount, "tubes added,", editcount, "edited,", delcount, "deleted at", time.strftime("%H:%M:%S", t))
            log_activity.close()
        # unlock the database
        #db_lock.unlock()
