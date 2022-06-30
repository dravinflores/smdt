#
# sMDT tube construction, collect data from previous week for all stations and users
# 
# Author: Reinhard Schwienhorst, based on DailyProductionHistory
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


def addToDict(date, user, myDict,earlyDict,lateDict):
    #if user == "": print(date, user)
    if myDict.get(user)==None:
        myDict[user]=1
    else:
        myDict[user]+=1
    # keep track of earliest and latest activity of user
    if earlyDict.get(user)==None:
        earlyDict[user]=date
    elif date < earlyDict[user]:
        earlyDict[user]=date
    if lateDict.get(user)==None:
        lateDict[user]=date
    elif date > lateDict[user]:
        lateDict[user]=date
# end of funcxtion addToDict

# Start date is the date one week ago
StartDate=datetime.today().date() - timedelta(days=21)
day = 0


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
    attrErr=0
    if(day > 0): StartDate=StartDate+timedelta(days=1)
    day +=1
    swageDict={}
    curDict={}
    tenDict={}
    leakDict={}
    bentDict={}
    # and keep track of time in the lab
    earlyDict={}
    lateDict={}

    for tube in tubes:
        # first go through swage records
        try:
            for record in tube.swage.m_records:
                date = record.date
                date = datetime(date.year,date.month, date.day).date()
                if date != None and date == StartDate:
                    user=record.user.strip()
                    date=record.date
                    addToDict(date, user, swageDict,earlyDict,lateDict)
        except IndexError:
            # no swage record entry, skip
            print("tube ",tube.get_ID()," index error for swage")
        except AttributeError:
            # swage record exists, but is not of the correct attribute, print it out
            #print("tube ",tube.get_ID()," attribute error for swage")
            attrErr+=1

        # next is dark current
        try:
            for record in tube.dark_current.m_records:
                date = record.date
                date = datetime(date.year,date.month, date.day).date()
                #print(swage_date, type(swage_date))
                if date != None and date == StartDate:
                    user=record.user.strip()
                    date=record.date
                    addToDict(date, user, curDict,earlyDict,lateDict)
        except IndexError:
            # no record entry, skip
            print("tube ",tube.get_ID()," index error for dark current")
        except AttributeError:
            #  record exists, but is not of the correct attribute
            #print("tube ",tube.get_ID()," attribute error for dark current")
            attrErr+=1

        # next is tension current
        try:
            for record in tube.tension.m_records:
                date = record.date
                date = datetime(date.year,date.month, date.day).date()
                #print(swage_date, type(swage_date))
                if date != None and date == StartDate:
                    user=record.user.strip()
                    date=record.date
                    addToDict(date, user, tenDict,earlyDict,lateDict)
        except IndexError:
            # no record entry, skip
            print("tube ",tube.get_ID()," index error for tension")
        except AttributeError:
            #  record exists, but is not of the correct attribute
            #print("tube ",tube.get_ID()," attribute error for tension")
            attrErr+=1

        # next is leak
        try:
            for record in tube.leak.m_records:
                date = record.date
                date = datetime(date.year,date.month, date.day).date()
                #print(swage_date, type(swage_date))
                if date != None and date == StartDate:
                    user=record.user.strip()
                    date=record.date
                    addToDict(date, user, leakDict,earlyDict,lateDict)
        except IndexError:
            # no record entry, skip
            print("tube ",tube.get_ID()," index error for leak")
        except AttributeError:
            #  record exists, but is not of the correct attribute
            #print("tube ",tube.get_ID()," attribute error for leak")
            attrErr+=1

        # next is bent
        try:
            for record in tube.bent.m_records:
                date = record.date
                date = datetime(date.year,date.month, date.day).date()
                #print(swage_date, type(swage_date))
                if date != None and date == StartDate:
                    user=record.user.strip()
                    date=record.date
                    addToDict(date, user, bentDict,earlyDict,lateDict)
        except IndexError:
            # no record entry, skip
            print("tube ",tube.get_ID()," index error for bent")
        except AttributeError:
            #  record exists, but is not of the correct attribute
            #print("tube ",tube.get_ID()," attribute error for bent")
            attrErr+=1
    # end of loop over tubes
            
    print("===============================================")
    print("Day ",StartDate)
    print("Total tasks completed")
    print("  Bentness:",sum(bentDict.values()))
    print("  Swage:   ",sum(swageDict.values()))
    print("  Tension: ",sum(tenDict.values()))
    print("  Dar Cur: ",sum(curDict.values()))

    print("Per user")
    for user in earlyDict:
        print("  ",user," first entry ",earlyDict[user].strftime("%a %I:%M%p")," last entry ",lateDict[user].strftime("%a %I:%M%p"))
        if bentDict.get(user)!=None: print("    ",bentDict[user]," tube bentness checks done")
        if swageDict.get(user)!=None: print("    ",swageDict[user]," tubes swaged")
        if tenDict.get(user)!=None: print("    ",tenDict[user]," tube tensioning done")
        if leakDict.get(user)!=None: print("    ",leakDict[user]," tube leak-checking done")
        if curDict.get(user)!=None: print("    ",curDict[user]," tube dark currents checked")
    # end of loop over user


sys.exit(0)
