#
# sMDT tube construction, collect data from previous week
# 
# Author: Reinhard Schwienhorst, based on DatabaseViewer example
# 2021-06-27
#

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from sMDT import db, tube
from sMDT.data import status
import sys

# get all of the tubes in the database
database=db.db()
tubes = database.get_tubes()

totTubes=0
totGood=0
totInc=0
totBent=0

# Start date for making tubes was August 14, 2020
# enter it as August 1 so that we stay at the month boundary
StartDate=datetime(year=2020, month=8,day=1, hour=23, minute=59)
month = 0

while StartDate < datetime.today():
    # counters
    TubesMonthlySwaged=0
    errorTubes=0
    goodTubes=0
    incTubes=0
    bentTubes=0
    tensionFail=0
    leakFail=0
    darkFail=0
    swageFail=0
    commentFail=0
    tubesErr=0

    if(month > 0): StartDate=StartDate+relativedelta(months=1)
    month +=1
    EndDate = StartDate+relativedelta(months=1)


    for tube in tubes:
        #print(tube.get_ID())
        isGood = tube.status()

        # get the swage date and start processing
        swage_date=tube.get_mfg_date()
        # skip all of the early tubes that have no date
        if swage_date == None:
            tubesErr+=1
            continue

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

        if swage_date < EndDate and swage_date > StartDate :
            TubesMonthlySwaged+=1
            #print(swage_date)
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
            elif isGood == status.Status.FAIL:
                #print(tube.get_ID())
                if tube.status_bentness() == status.Status.FAIL:
                    bentTubes+=1
                elif tube.swage.status()== status.Status.FAIL:
                    swageFail+=1 
                elif tube.tension.status()== status.Status.FAIL:
                    # if the swaged tube hasn't been tension tested yet, declare it incomplete
                    dt=tube.swage.get_record(mode='last').date
                    if dt > tube.tension.get_record(mode='last').date:
                        #print("tube not yet tested after swaging")
                        incTubes+=1
                    else:
                        tensionFail+=1 
                elif tube.leak.status()== status.Status.FAIL:
                    leakFail+=1 
                elif tube.dark_current.status()== status.Status.FAIL:
                    darkFail+=1
                elif tube.comment_fails():
                    commentFail+=1

    
    TubesMonthlySwaged -=bentTubes
    print("For month",StartDate.strftime("%B %Y"))
    if TubesMonthlySwaged>0:
        print("Total ",TubesMonthlySwaged," swaged, good+incomplete ",goodTubes,"+",incTubes,"=",goodTubes+incTubes,", failure rate %2.1f%%" % (100.-(goodTubes+incTubes)/TubesMonthlySwaged*100.))
        print("  Failure reason for",TubesMonthlySwaged-goodTubes-incTubes," tubes: Swage:",swageFail,", Tension:",tensionFail,", Leak:",leakFail,", dark:",darkFail, ", comment:",commentFail)
        print("  Plus",bentTubes,"bent tubes.")

        totTubes+=TubesMonthlySwaged
        totGood+=goodTubes
        totInc+=incTubes
        totBent+=bentTubes
    else:
        print("No tube swaged")
# end of loop over months
#
print("Summary:")
print("Total ",totTubes," swaged, good+incomplete ",totGood,"+",totInc,"=",totGood+totInc,", fail",totTubes-totGood-totInc,", failure rate %2.1f%%" % (100.-(totGood+totInc)/totTubes*100.))
print("PLus",totBent," bent tubes.")
print("Plus ",tubesErr," tubes without a date")
sys.exit(0)
