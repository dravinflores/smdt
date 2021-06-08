#
# sMDT tube construction, collect data from previous week
# 
# Author: Reinhard Schwienhorst, based on DatabaseViewer example
# 2021-06-02
#

from datetime import datetime, timedelta

from sMDT import db, tube
from sMDT.data import status
import sys

# get all of the tubes in the database
database=db.db()
tubes = database.get_tubes()
EndDate=datetime(2021,6,4)

totTubes=0
totGood=0
totInc=0

# Start date is the date when we started makign tubes for the tube PRR
StartDate=datetime(2020,8,14)
week = 0

while StartDate < datetime.today():
    # counters
    TubesWeeklySwaged=0
    errorTubes=0
    goodTubes=0
    incTubes=0
    if(week > 0): StartDate=StartDate+timedelta(days=7)
    week +=1
    EndDate = StartDate+timedelta(days=7)


    for tube in tubes:
        #print(tube.get_ID())
        isGood = tube.status()

        try:
            swage_date = tube.swage.get_record('last').date
            if swage_date != None and swage_date < (EndDate+timedelta(days=1)) and swage_date > StartDate :
                TubesWeeklySwaged+=1
                #print(swage_date)
                if isGood == status.Status.PASS: goodTubes+=1
                elif isGood == status.Status.INCOMPLETE:
                        # For incomplete tubes, check if they pass dark current
                        # they may be incomplete if the second tension test is done at UMich
                        incTubes+=1
                        #print(tube.get_ID()," is incomplete.")
                        try:
                            cur = tube.dark_current.get_record().dark_current
                            #print("Dark current ",cur)
                            if cur > 2.:
                                incTubes-=1
                        except IndexError:
                            incTubes-=1
                            #print("no dark current")
                #elif isGood == status.Status.FAIL and StartDate < datetime(2020,11,25):
                #    print(tube.get_ID())
                #    print("tension: "+str(tube.tension.status()))
                #    print("leak: "+str(tube.leak.status()))
                #    print("current: "+str(tube.dark_current.status()))
                #    print(tube.dark_current.get_record().__str__())
        except IndexError:
            #print("Error tube, "+tube.get_ID())
            errorTubes+=1

    print("Week from ",StartDate," to ", EndDate)
    if TubesWeeklySwaged>0:
        print("Total ",TubesWeeklySwaged," swaged, good/incomplete ",goodTubes,"/",incTubes," failure rate %2.1f" % (100.-(goodTubes+incTubes)/TubesWeeklySwaged*100.))
        totTubes+=TubesWeeklySwaged
        totGood+=goodTubes
        totInc+=incTubes
    else:
        print("No tube swaged")
# end of loop over weeks
#
print("Summary:")
print("Total ",totTubes," swaged, good/incomplete ",totGood,"/",totInc," failure rate %2.1f" % (100.-(totGood+totInc)/totTubes*100.))
sys.exit(0)
