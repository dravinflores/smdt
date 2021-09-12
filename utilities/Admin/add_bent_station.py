import os
import sys
import shelve
 

DROPBOX_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DROPBOX_DIR)

from sMDT import db
from sMDT.data.bent import Bent

print('loading database')
count = 0
datab = db.db()
with shelve.open("database_with_bent_station.s") as tubes:
    for tube in datab.get_tubes():
        if not hasattr(tube, "bent"):
            tube.bent =  Bent()
            count += 1
            tubes[tube.get_ID()] = tube
            continue
        else:
            tubes[tube.get_ID()] = tube
print(str(count) + " tubes had bent stations added to them")

