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
    td=tube.get_mfg_date()
    if td!=None:
        continue
    print("Need to fix date ",orig_id)
    # find the tube with the next higher ID
    found_id=0
    check_id='MSU'+'{:05d}'.format(int(orig_id[3:])+1)
    while(found_id==0):
        print("checking ID",check_id)
        try:
            tube2=database.get_tube(check_id)
        except KeyError:
            check_id='MSU'+'{:05d}'.format(int(check_id[3:])+1)
            continue
        td2=tube2.get_mfg_date()
        if td2==None:
            check_id='MSU'+'{:05d}'.format(int(check_id[3:])+1)
            continue
        
        print("tube date found,",td2,", adding comment")
        #tube.new_comment(("Adding closest mfg date","Reinhard",td2,status.Status.PASS))
        #database.add_tube(tube)
        found_id=check_id
# end of loop
    
sys.exit(0)
