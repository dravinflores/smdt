#
# sMDT tube construction, fix duplicate database entries
# 
# Author: Reinhard Schwienhorst, based on Monthly production example
# 2021-08-25
#

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from sMDT import db, tube
from sMDT.data import status
import sys

# get all of the tubes in the database
database=db.db()
tubes = database.get_tubes()



for tube in tubes:
    #print(tube.get_ID())
    orig_id=tube.get_ID()
    if orig_id[:3]!="MSU":
        print("Need to fix, merge tube ",orig_id)
        if orig_id[:3]=="msu":
            id = "MSU"+orig_id[3:]
        print("changing to",id)
        # check for existing tube
        try:
            tube2=database.get_tube(id)
        except KeyError:
            print("tube not found, adding it")
            #print(tube)
            #tube.set_ID(id)
            #database.add_tube(tube)
            continue
        #print("tube found, adding records")
        #tube.set_ID(id)
        #database.add_tube(tube)

        # if tube was already added, then erase the duplicate
        #tube.set_ID(orig_id)
        #database.delete_tube(tube)
# end of loop
    
sys.exit(0)
