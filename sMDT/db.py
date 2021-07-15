###############################################################################
#   File: db.py
#   Author(s): Paul Johnecheck, Dravin Flores
#   Date Created: 11 April, 2021
#
#   Purpose: This is the class representing the database.
#    It will act as the main interface for reading and writing to the database. 
#
#   Known Issues: The database appears to delete itself every-so-often.
#
#   Workarounds: In order to figure out why it's deleting itself, we're going
#       to have a bunch of logging files to help.
#
###############################################################################

import shelve
import pickle
import time
import datetime
import random
import os
import sys

from copy import deepcopy
from pathlib import Path

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
        self.logger = DBLogger()

    def open_database(self):
        """
        Try to open up the database in read-only mode. An empty dictionary will
        be returned if the file cannot be found.
        """
        try:
            write_str = "A request for read-only access to the " \
                        "database has been made"
            self.logger.write(write_str)
            r = shelve.open(self.path, 'r')
        except Exception as e:
            # We need to create the database on the fly.
            return dict()
            write_str = f"The database was unable to be opened." \
                        f"The error is as follows: {e}"
            self.logger.write(write_str, mode='critical')
        else:
            write_str = f"Database was able to be obtained."
            self.logger.write(write_str)
            return r

    def close_database(self, shelf_obj):
        """
        Close any opened shelve file.
        """
        try:
            write_str = "Closing the database"
            shelf_obj.close()
        except Exception as e:
            write_str = f"Database was unable to be closed." \
                        f"The error is as follows {e}."
            self.logger.write(write_str, mode='critical')

    def size(self):
        """
        Return the integer size of the database. 
        May wait for the database to be unlocked
        """

        self.logger.write("Locking the database to obtain size information.")
        db_lock = locks.Lock("database")
        db_lock.wait()
        # tubes = shelve.open(self.path)
        tubes = self.open_database()
        ret_size = len(tubes)
        # tubes.close()
        self.close_database(tubes)

        self.logger.write(f"Size of the database was {ret_size}")
        return ret_size

    def add_tube(self, tube: Tube()):
        """
        Adds tube to the database. It does so by pickling the tube,
        and adding it to the new_data file for the database manager 
        to add to the database with update()
        """

        dt = datetime.datetime.now()
        timestamp = dt.timestamp()

        filename = str(timestamp) + str(random.randrange(0, 999)) + ".tube"

        new_data_path = os.path.join(self.sMDT_DIR, "new_data")

        if not os.path.isdir(new_data_path):
            os.mkdir(new_data_path)

        self.logger.write("Locking the database to add a tube.")
        file_lock = locks.Lock(filename)
        file_lock.lock()
        with open(os.path.join(new_data_path, filename), "wb") as f:
            pickle.dump(tube, f)
        file_lock.unlock()

    def get_tube(self, id):
        """
        Returns the tube specified by id. 
        May wait for the database to be unlocked.
        """
        #db_lock = locks.Lock("database")
        #db_lock.wait()

        self.logger.write("Request for a tube has been made.")

        # The database is opened up as read-only
        # tubes = shelve.open(self.path)
        tubes = self.open_database()
        try:
            ret_tube = tubes[id]
        except KeyError:
            # tubes.close()
            self.close_database(tubes)
            raise KeyError
        else:
            # tubes.close()
            self.close_database(tubes)
            return ret_tube

    def get_tubes(self, selection=None):
        # tubes = shelve.open(self.path)
        self.logger.write("Request for all tubes has been made.")
        tubes = self.open_database()
        if selection:
            ret_tubes = []
            for ID in selection:
                try:
                    ret_tubes.append(tubes[ID])
                except KeyError:
                    pass
        else:
            ret_tubes = list(tubes.values())
        # tubes.close()
        self.close_database(tubes)
        return ret_tubes

    def get_IDs(self):
        db_lock = locks.Lock("database")
        db_lock.wait()
        # tubes = shelve.open(self.path)
        self.logger.write("Request for all tubes has been made.")
        tubes = self.open_database()
        ret_ids = list(tubes.keys())
        # tubes.close()
        self.close_database(tubes)
        return ret_ids

    def delete_tube(self, tube_id):
        self.logger.write("Request to delete a tube has been made.")

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
        self.logger.write("Request to overwrite a tube has been made.")
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

    def __init__(
        self, 
        db_path=os.path.join(containing_dir, "database.s"), 
        archive=True, 
        testing=False
    ):
        """
        Constructor, builds the database manager object. 
        Gets the path to the database
        """
        self.path = db_path
        self.archive = archive
        self.testing = testing

        with shelve.open(self.path) as tubes:
            self.database_backup = deepcopy(dict(tubes))

        self.size = len(self.database_backup)
        self.need_to_restore = False

        self.logger = DBLogger(author="DB Manager", file='db_man_log.log')

    def wipe(self, confirm=False):
        """
        Wipes the database. confirm must be "confirm" to proceed. 
        Exercise extreme caution with this, but it is necessary 
        for many test cases.
        """
        self.logger.write("A call has been made to wipe the database.")
        if confirm == 'confirm':
            db_lock = locks.Lock("database")
            db_lock.lock()

            tubes = shelve.open(self.path, flag='n')

            tubes.close()
            db_lock.unlock()
        else:
            raise RuntimeError

    def cleanup(self) -> None:
        self.logger.write("A call has been made for cleanup.")
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
        Needs to be ran after a db object calls add_tube(), 
        otherwise the database will not contain the data in time for get_tube()
        """
        self.logger.write("A call has been made to update the database.")

        # dropbox_folder = os.path.dirname(sMDT_DIR)

        if not self.testing:
            pickler = station_pickler(
                os.path.dirname(self.path), 
                archive=self.archive, 
                logging=logging
            )
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
            log_activity = open('activity.log', 'a')

            # Check if the stored database is more recent.
            if self.size - len(tubes) > 10:
                self.logger.write("The database must be restored.")
                self.need_to_restore = True
                for (code, tube) in self.database_backup.items():
                    tubes[code] = tube

                padding = '\n\n'

                restored_str = '---------- DATABASE WAS RESTORED ----------'
                data_restored_str = padding + restored_str + padding
                log_activity.write(data_restored_str)

                t = datetime.datetime.now()
                time_str = f'Restored at {t.strftime("%d-%b-%Y %H:%M:%S")}'
                time_restored_str = time_str + padding
                log_activity.write(time_restored_str)

                print_str = data_restored_str + time_restored_str
                print(print_str)

                error_dir = Path('DatabaseError')
                file_name = t.isoformat(timespec='seconds', sep='_') + '.txt'
                error_file = error_dir / file_name

                if not error_dir.exists():
                    error_dir.mkdir()

                with error_file.open('w+') as f:
                    f.write(print_str)

            else:
                self.logger.write("Database does not need to be restored.")
                addcount = editcount = delcount = 0
                # log_activity = open('activity.log','a')
                t = time.localtime()
                for filename in os.listdir(new_data_path):
                    new_data_file = open(
                        os.path.join(new_data_path, filename), 
                        'rb'
                    ) 

                    tube = pickle.load(new_data_file) 
                    new_data_file.close()

                    if filename.endswith(".del.tube"):
                        if tube.get_ID() in tubes:
                            del tubes[tube.get_ID()]
                            if logging:

                                log_activity.write(
                                    time.strftime("%d-%b-%Y %H:%M:%S", t) 
                                    + "\tDeleting tube " 
                                    + tube.get_ID() 
                                    + " from database.\n"
                                )

                                print(
                                    "Deleting tube", 
                                    tube.get_ID(), 
                                    "from database."
                                )
                                delcount += 1
                        else:
                            if logging:
                                log_activity.write(
                                    time.strftime("%d-%b-%Y %H:%M:%S", t) 
                                    + "\tAttempted to delete tube " 
                                    + tube.get_ID() 
                                    + ", tube not found.\n"
                                
                                )
                                print(
                                    "Attempted to delete tube", 
                                    tube.get_ID(), 
                                    ", tube not found."
                                )

                    elif filename.endswith(".edit.tube"):
                        if logging:
                            log_activity.write(
                                time.strftime("%d-%b-%Y %H:%M:%S", t) 
                                + "\tRewriting the data of " 
                                + tube.get_ID() 
                                + " due to edit\n"
                            )
                            print(
                                "Rewriting the data of", 
                                tube.get_ID(), 
                                "due to edit"
                            )
                            editcount += 1
                        tubes[tube.get_ID()] = tube


                    elif filename.endswith(".tube"):
                        if logging:
                            log_activity.write(
                                time.strftime("%d-%b-%Y %H:%M:%S", t) 
                                + "\tLoading tube or adding data to " 
                                + tube.get_ID() 
                                + " into database.\n"
                            )
                            print(
                                "Loading tube", 
                                tube.get_ID(), 
                                "into database."
                            )

                        if tube.get_ID() in tubes: 
                            # add the tubes to the database
                            temp = tubes[tube.get_ID()] + tube
                            tubes[tube.get_ID()] = temp
                        else:
                            tubes[tube.get_ID()] = tube

                        addcount += 1
                    else:
                        if logging:
                            print("Unrecognized file type in new_data folder")

                    # delete the file that we added the tube from
                    os.remove(os.path.join(new_data_path, filename))  

                t = time.localtime()
                if logging:
                    print(
                        addcount, 
                        "tubes added,", 
                        editcount, 
                        "edited,", 
                        delcount, 
                        "deleted at", 
                        time.strftime("%H:%M:%S", t)
                    )
                log_activity.close()

                self.database_backup = deepcopy(dict(tubes))
                self.size = len(self.database_backup)

        # unlock the database
        # db_lock.unlock()


class DBLogger:
    def __init__(self, author=None, file=None):
        self.author = author
        self.dropbox_path = Path(__file__).parents[1].resolve()
        self.logging_path = self.dropbox_path / 'DatabaseLogging'

        if not file:
            self.logging_file = self.logging_path / 'database_log_extra.log'
        else:
            self.logging_file = self.logging_path / file

        self.logging_path.mkdir(parents=True, exist_ok=True)

        if not self.logging_file.exists():
            self.logging_file.touch()

    def write(self, write_str, external_author=None, mode='normal'):
        current_time = datetime.datetime.now()
        time_str = current_time.isoformat(timespec='seconds', sep=' ')

        if external_author:
            message = f"{time_str}: {mode} [{external_author}] {write_str}\n"
        elif self.author:
            message = f"{time_str}: {mode} [{self.author}] {write_str}\n"
        else:
            message = f"{time_str}: {mode} {write_str}\n"

        with self.logging_file.open('a') as f:
            f.write(message)
