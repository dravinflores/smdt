#
# sMDT tube construction, collect data from previous week
# 
# Author: Reinhard Schwienhorst, based on WeeklyProductionHistory
# 2021-06-11
#

from datetime import datetime, timedelta

from sMDT import db, tube
from sMDT.data import status
import sys

# get all of the tubes in the database
database=db.db()
tubes = database.get_tubes()
if len(tubes)==0:
    print("Error, no tubes found!")
    sys.exit(1)
EndDate=datetime(2021,6,4).date()

totTubes=0
totGood=0
totInc=0
totBent=0

# Start date is the date one week ago
StartDate=datetime.today().date() - timedelta(days=7)
day = 0
noProdDay=0

while StartDate < datetime.today().date():
    # counters
    TubesSwaged=0
    errorTubes=0
    goodTubes=0
    incTubes=0
    bentTubes=0
    tensionFail=0
    darkFail=0
    swageFail=0
    commentFail=0
    if(day > 0): StartDate=StartDate+timedelta(days=1)
    day +=1

    for tube in tubes:
        #print(tube.get_ID())
        isGood = tube.status()
        # for each tube, first check if it is swaged
        try:
            swage=tube.swage
        except AttributeError:
            # swage record doesn't exist, skip to the next tube
            print(tube.get_ID()," swage record doesn't exist")
            continue
        try:
            swage_record = swage.get_record('first')
        except IndexError:
            # no swage record entry, skip to the next tube
            continue
        except AttributeError:
            # swage record exists, but is not of the correct attribute, print it out
            if swage_record != "":
                print("tube ",tube.get_ID()," swage record ",swage_record)
            continue
        # skip this tube if the swage record is an empty string
        if isinstance(swage_record,str):
            #print("swage record is a string:",swage_record)
            continue
        # now we finally have a valid swage record, get the swage date and start processing
        swage_date=tube.get_mfg_date()
        if swage_date != None:
            #print(swage_date, type(swage_date))
            swage_date = datetime(swage_date.year,swage_date.month, swage_date.day).date()
            #print(swage_date, type(swage_date))
            if swage_date != None and swage_date == StartDate :
                TubesSwaged+=1
                if isGood == status.Status.PASS: goodTubes+=1
                elif isGood == status.Status.INCOMPLETE:
                    # For incomplete tubes, check if they pass dark current
                    # they may be incomplete if the second tension test is done at UMich
                    #print(tube.get_ID()," is incomplete.")
                    try:
                        cur = tube.dark_current.get_record().dark_current
                        #print("Tube ",tube.get_ID()," is incomplete, dark current ",cur)
                        if cur < 2.:
                            # dark current is ok, so this is a good tube!
                            goodTubes+=1
                    except IndexError:
                        # no dark current, so this tube is truly incomplete
                        incTubes+=1
                    except AttributeError:
                        # no dark current, so this tube is truly incomplete
                        incTubes+=1
                elif isGood == status.Status.FAIL:
                    #print(tube.get_ID())
                    if tube.status_bentness() == status.Status.FAIL:
                        bentTubes+=1
                    elif tube.swage.status()== status.Status.FAIL:
                       swageFail+=1 
                    elif tube.tension.status()== status.Status.FAIL:
                       tensionFail+=1 
                    elif tube.dark_current.status()== status.Status.FAIL:
                       darkFail+=1
                    elif tube.comment_fails():
                        commentFail+=1
                    #print("tension: "+str(tube.tension.status()))
                    #print("leak: "+str(tube.leak.status()))
                    #print("current: "+str(tube.dark_current.status()))
                    #print(tube.dark_current.get_record().__str__())
        else:
            #print("Swage date is none, tube, "+tube.get_ID())
            errorTubes+=1

    print("Day ",StartDate)
    TubesSwaged-=bentTubes
    if TubesSwaged>0:
        print("  Swaged: ",TubesSwaged,", good/incomplete ",goodTubes,"/",incTubes,", fail ",TubesSwaged-goodTubes-incTubes,", failure rate %2.1f%%" % (100.-(goodTubes+incTubes)/TubesSwaged*100.))
        print("  Failure reason for",TubesSwaged-goodTubes-incTubes," tubes: Swage:",swageFail,", Tension:",tensionFail,", dark:",darkFail, ", comment:",commentFail)
        #print("  And",bentTubes,"bent tubes.")
        totTubes+=TubesSwaged
        totGood+=goodTubes
        totInc+=incTubes
        totBent+=bentTubes
    else:
        noProdDay+=1
        print("  No tube swaged")
# end of loop over weeks
#
print("Summary:")
print("Total",totTubes," swaged (",int(totTubes/(day-noProdDay)),"per day), good+incomplete",totGood,"+",totInc,"=",totGood+totInc,", fail ",totTubes-totGood-totInc,", failure rate %2.1f%%" % (100.-(totGood+totInc)/totTubes*100.))
#print(" And ",totBent," bent tubes.")
sys.exit(0)
