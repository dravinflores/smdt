#
# sMDT tube construction, collect data from previous week
# 
# Author: Reinhard Schwienhorst, based on Monthly production example
# 2021-08-24
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

# Start date for making tubes was August 14, 2020
# enter it as August 1 so that we stay at the month boundary
StartDate=datetime(year=2020, month=8,day=1, hour=23, minute=59)
EndDateMod0=datetime(year=2020, month=11,day=20, hour=23, minute=59)
totMod0=0
totProd=0
goodMod0=0
goodProd=0
errMod0=0
errProd=0
incMod0=0
incProd=0
bentMod0=0
bentProd=0
tubesErr=0
totOld=0
goodOld=0
errOld=0
incOld=0
first_swage_date=datetime.today()

for tube in tubes:
    #print(tube.get_ID())
    isGood = tube.status()
    swage_date=tube.get_mfg_date()

    if swage_date == None:
        tubesErr+=1
        continue
    if swage_date > StartDate :
        if swage_date < EndDateMod0:
            totMod0+=1
            if isGood == status.Status.PASS: goodMod0+=1
            elif isGood == status.Status.INCOMPLETE:  incMod0+=1
            elif tube.status_bentness() == status.Status.FAIL: bentMod0+=1
            else: errMod0+=1
        else:
            totProd+=1
            if isGood == status.Status.PASS: goodProd+=1
            elif isGood == status.Status.INCOMPLETE:  incProd+=1
            elif tube.status_bentness() == status.Status.FAIL: bentProd+=1
            else: errProd+=1
    else:
        # older than the start date means old tubes, before module 0 tubes, including short tubes
            totOld+=1
            if swage_date < first_swage_date: first_swage_date =  swage_date
            if isGood == status.Status.PASS: goodOld+=1
            elif isGood == status.Status.INCOMPLETE:  incOld+=1
            else: errOld+=1
        
# end of loop over tubes
totMod0 -= bentMod0
totProd -= bentProd

print("Old, pre-mod0 tubes (before August 2020):")
print(" ",totOld," swaged, good+inc ",goodOld,"+",incOld,"=",goodOld+incOld,", fail ",errOld,", failure rate %2.1f%%" % (errOld/totOld*100.))
print(" First tube was officially swaged on ",first_swage_date)
print("Module 0 tubes (Aug 2020 to Nov 2020):")
print(" ",totMod0," swaged, good+inc ",goodMod0,"+",incMod0,"=",goodMod0+incMod0,", fail ",errMod0,", failure rate %2.1f%%" % (errMod0/totMod0*100.))
print(" Plus",bentMod0," bent tubes.")
print("Production tubes (since Dec 2020):")
print(" ",totProd," swaged, good+inc ",goodProd,"+",incProd,"=",goodProd+incProd,", fail ",errProd,", failure rate %2.1f%%" % (errProd/totProd*100.))
print(" Plus",bentProd," bent tubes.")
tubesNeeded=576*9+40*472
print(" Tubes needed:",tubesNeeded,", completed fraction %2.1f%%" % ((goodProd+incProd)/tubesNeeded*100.))
print("Total tubes:")
print(" ",totMod0+totProd," swaged, good+inc ",goodMod0+goodProd,"+",incMod0+incProd,"=",goodMod0+goodProd+incMod0+incProd,", fail ",errMod0+errProd,", failure rate %2.1f%%" % ((errMod0+errProd)/(totMod0+totProd)*100.))
print(" Plus",bentMod0+bentProd," bent tubes.")
print("tubes without date ",tubesErr)

sys.exit(0)
