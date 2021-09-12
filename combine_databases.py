from sMDT import db 
import sys
import os
import shelve

sMDT_DIR = os.path.dirname(os.path.abspath(__file__))
containing_dir = os.path.dirname(sMDT_DIR)
DROPBOX_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DROPBOX_DIR)

database = db.db()
with shelve.open("database_new.s") as tubes:
    for tube in tubes:
        #print(tube)
        #print(tubes[tube])
        database.add_tube(tubes[tube])