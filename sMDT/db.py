###############################################################################
#   File: db.py
#   Author(s): Paul Johnecheck, Dravin Flores
#   Date Created: 11 April, 2021
#
#   Purpose: This is the class representing the database. It will act 
#       as the main interface for reading and writing to the database. 
#
#   Known Issues: The database appears to delete itself every-so-often.
#
#   Workarounds: In order to better ensure that the database access is 
#       restricted, the portalocker library is used; this is a cross-platform
#       locking library.
#  Modifications:
#  2022-06, Sara Sawford, Reinhard Schwienhorst, add UMich information
#
###############################################################################

import shelve
import pickle
import time
import datetime
import random
import os
import sys
#import dbm # used only to make sure the database is in dmb.dumb format for compatibility

import portalocker

from pathlib import Path

from sMDT.tube import Tube
from sMDT.legacy import station_pickler
from sMDT import DBLogger

logging = False


class db:
    def __init__(self):
        # Here are all the directories that are relevant to the database.
        # We are essentially asking for the directory that is two directories
        # up. All paths are then relative to this path.

        #Gets first two directories of the full path involved in finding the dropbox
        self.dropbox_directory = Path(__file__).resolve().parents[1]
        #uses above path to put the database in this directory as datdabase.s
        self.db_file = self.dropbox_directory / 'database.s'
        self.lock_file = self.dropbox_directory /'sMDT'/'locks'/'db_lock.lock'
        #creates new directory from data in 'new data'
        self.new_data_dir = self.dropbox_directory / 'sMDT' / 'new_data'
        #print("Database directory ",self.new_data_dir)

        # We need to check if the database lock file exists. If
        # not, then we'll have to make those directories.
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)

        # Now we'll go ahead and create the lock file.
        self.lock_file.touch(exist_ok=True)

        if logging:
            self.logger = DBLogger()

    def open_shelve(self):
        # We are going to use portalocker to have an os-independent locking
        # system. Whenever we ask to open a file, we will lock the 
        # 'db_file_lock.lock' file. Then, we'll use this exclusively accessed
        # file to open the database using shelve. The database file itself is 
        # not locked, just an auxiliary file.

        # Before anything, we will go ahead and convert the path object into a 
        # normal string. This is because portalocker has it's own internal 
        # method of opening the database.

        #turning path into string
        s = str(self.lock_file.resolve())

        #try/except lines
        #try lets you test a block for errors
        #if there are errors, use except to handle them. if not, runs all good
        try:
            #r+ probably means to read and write to the file
            with portalocker.Lock(s, 'r+', timeout=30) as locked_file:
                # We've got exclusive access to the database.

                #remembering self.db_file is the database.s
                db_file = str(self.db_file.resolve())
                #print("Database file format: ",dbm.whichdb(db_file))

                #'r' is just a read only file
                return_dict = shelve.open(db_file, 'r')
        except portalocker.LockException:
            # Just in-case we can't open the database, we'll return an
            # empty dictionary.
            return_dict = dict()

        return return_dict

    def close_shelve(self, shelve_obj):
        s = str(self.lock_file.resolve())
        try:
            with portalocker.Lock(s, 'r+', timeout=30) as locked_file:
                shelve_obj.close()

        #if the database doesn't exist, there is nothing to close
        except portalocker.LockException as e:
            pass

    def size(self):
        #since open_shelve returns the dictionary (either blank or database.s), tube_dict = return_dict
        tube_dict = self.open_shelve()
        number_of_tubes = len(tube_dict)

        #close_shelve is an action, not return value
        self.close_shelve(tube_dict)
        return number_of_tubes

    def add_tube(self, tube=Tube()):
        dt = datetime.datetime.now()
        timestamp = dt.timestamp()

        filename = str(timestamp) + str(random.randrange(0, 999)) + ".tube"
        #creates a new .tube file named after the data,time and random number. located in new_data
        file_obj = self.new_data_dir / filename
        if not file_obj.exists():
            #parents=True creates any directories that don't exist yet
            #exist_ok=True does nothing if a directory already exists
            file_obj.parent.mkdir(parents=True, exist_ok=True)

            #creates file.txt at file_obj path
            file_obj.touch()

        s = str(self.lock_file.resolve())
        try:
            with portalocker.Lock(s, 'r+', timeout=30) as locked_file:

                #wb+ to write a binary file
                with file_obj.open('wb+') as f:
                    #writing tube to file_obj we just opened
                    #print("writing tube ",tube.get_ID()," to file ",filename)
                    pickle.dump(tube, f)
        except portalocker.LockException as e:
            #print("Error trying to write to database file ",filename)
            pass

    def get_tube(self, barcode):
        tubes = self.open_shelve()
        #if the tube with the specific parameter barcode exists, then return it and close the shelf
        try:
            ret_tube = tubes[barcode]
        except KeyError:
            self.close_shelve(tubes)
            raise KeyError
        else:
            self.close_shelve(tubes)
            return ret_tube

    def get_tubes(self, selection=None):
        tubes = self.open_shelve()

        #if selection=None, then goes to else statement
        #if selection != None, appends the tubes in the list to return list
        #else, returns the initial tube values
        if selection:
            ret_tubes = []
            for ID in selection:
                try:
                    ret_tubes.append(tubes[ID])
                except KeyError:
                    pass
        else:
            ret_tubes = list(tubes.values())
        self.close_shelve(tubes)
        return ret_tubes

    def get_IDs(self):
        #returns keys of dictionary
        tubes = self.open_shelve()
        ret_ids = list(tubes.keys())
        self.close_shelve(tubes)
        return ret_ids

    def delete_tube(self, tube_id):
        #unless the remove is in umich_tube(), only creates .del.tube, doesn't remove from database
        if type(tube_id) is not str:
            tube_id = tube_id.get_ID()

        dt = datetime.datetime.now()
        timestamp = dt.timestamp()

        filename = str(timestamp) + str(random.randrange(0, 999)) + ".del.tube"
        file_obj = self.new_data_dir / filename

        if not file_obj.exists():
            file_obj.touch()

        tube = Tube()
        tube.set_ID(tube_id)

        s = str(self.lock_file.resolve())
        try:
            with portalocker.Lock(s, 'r+', timeout=30) as locked_file:
                with file_obj.open('wb+') as f:
                    pickle.dump(tube, f)
        except portalocker.LockException as e:
            pass

    def overwrite_tube(self, tube):
        #doesn't seem to remove the wrong tube, just edits one of the ids
        dt = datetime.datetime.now()
        timestamp = dt.timestamp()

        filename = str(timestamp) + str(random.randrange(0, 999)) + ".edit.tube"
        file_obj = self.new_data_dir / filename

        if not file_obj.exists():
            file_obj.touch()

        s = str(self.lock_file.resolve())
        try:
            with portalocker.Lock(s, 'r+', timeout=30) as locked_file:
                with file_obj.open('wb+') as f:
                    pickle.dump(tube, f)
        except portalocker.LockException as e:
            pass


class db_manager:
    def __init__(self, db_path=None, archive=True, testing=False):
        self.dropbox_directory = Path(__file__).resolve().parents[1]

        #if db_path = None, create a new database
        if not db_path:
            self.db_file = self.dropbox_directory / 'database.s'

        self.lock_file = self.dropbox_directory /'sMDT'/'locks'/'db_lock.lock'
        self.new_data_dir = self.dropbox_directory / 'sMDT' / 'new_data'

        self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        self.lock_file.touch(exist_ok=True)

        self.path = str(self.db_file.resolve())
        self.archive = archive
        self.testing = testing

    def wipe(self, confirm=False):
        if confirm == 'confirm':
            s = str(self.lock_file.resolve())
            try:
                with portalocker.Lock(s, 'r+', timeout=30) as locked_file:
                    tubes = shelve.open(self.path, 'n')
            except portalocker.LockException as e:
                pass
        else:
            raise RuntimeError

    def cleanup(self):
        for file_obj in self.new_data_dir.iterdir():
            file_obj.unlink()

    def update(self, logging=True):
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
            #pickler.pickle_umich()

        # Now we lock the database to write.
        s = str(self.lock_file.resolve())
        
        with portalocker.Lock(s, 'r+', timeout=30) as locked_file:
            with shelve.open(self.path) as tubes:
                log_activity = open('activity.log', 'a')

                # Check if the stored database is more recent.
                if not (len(tubes) or len(tubes) < 50) and not self.testing:
                    print("\nThe Database has been corrupted. ") 
                    print_str = "Size is {}.\n".format(len(tubes))
                    print_str += "The database will continue to sync. \n"
                    print(print_str)
                    t = datetime.datetime.now()
                    print("At Time:",t.strftime("%d-%b-%Y %H:%M:%S"),"\n\n")

                    error_dir = Path('DatabaseError')
                    ext = '.txt'
                    file_name = t.isoformat(timespec='seconds', sep='_') + ext
                    error_file = error_dir / file_name

                    if not error_dir.exists():
                        error_dir.mkdir()

                    with error_file.open('w+') as f:
                        f.write(print_str)

                addcount = editcount = delcount = 0
                t = time.localtime()
                #
                # loop over files in new_data directory
                for filename in os.listdir(self.new_data_dir):
                    new_data_file = open(
                        os.path.join(self.new_data_dir, filename), 'rb'
                    ) 

                    try:
                        tube = pickle.load(new_data_file) 
                        new_data_file.close()
                    except EOFError:
                        # this file is being written to as we're trying to open it, skip for now
                        continue

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
                            #print("Tube ",tube.get_ID()," already exists")
                            temp = tubes[tube.get_ID()] + tube
                            tubes[tube.get_ID()] = temp
                        else:
                            tubes[tube.get_ID()] = tube

                        addcount += 1
                    else:
                        if logging:
                            print("Unrecognized file type in new_data folder")

                    # delete the file that we added the tube from
                    os.remove(os.path.join(self.new_data_dir, filename))  

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
