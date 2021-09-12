import sys
import os
import random
import datetime

DROPBOX_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(DROPBOX_DIR)

from sMDT import db

def keyDay(record):
    return record.date.day

def getFirstTensionRecord(records):
    earliestTensionDate = datetime.datetime(year=datetime.MAXYEAR, month=1, day=1)
    for record in records:
        if record.date < earliestTensionDate:
            earliestTensionDate = record.date
    firstTensionRecord = None
    firstTensionDate = datetime.datetime(year=datetime.MINYEAR, month=1, day=1)
    for record in records:
        if record.date.day == earliestTensionDate.day and record.date.month == earliestTensionDate.month:
            if record.date > firstTensionDate:
                firstTensionRecord = record
                firstTensionDate = record.date
    return firstTensionRecord


def getLastTension(records):
    lastRecordDate = datetime.datetime(year=datetime.MINYEAR, month=1, day=1)
    lastRecord = None
    for record in records:
        if record.date > lastRecordDate:
            lastRecord = record
            lastRecordDate = lastRecord.date
    return lastRecord

def swageDateKey(tube):
    try:
        date = tube.swage.get_record().date
        if date == None:
            return datetime.datetime(year=datetime.MINYEAR, month=1, day=1)
        else:
            return date
    except:
        return datetime.datetime(year=datetime.MINYEAR, month=1, day=1)

datab = db.db()
tubes = datab.get_tubes()
tubes.sort(key=swageDateKey, reverse=True)

f = open('database.csv','w')
f.write('Barcode,Status [Pass/Incomplete/Fail],First Tension [g],First Frequency [Hz],First Tension Date [YYYY-MM-DD HH:MM:SS],')
f.write('Last Tension [g],Last Frequency [Hz],Last Tension Date [YYYY-MM-DD HH:MM:SS],Leak Rate,')
f.write('Leak Date [YYYY-MM-DD HH:MM:SS],Dark Current [nA],Dark Current Date,Raw Length [mm],')
f.write('Swage Length [mm], Swage Date [YYYY-MM-DD HH:MM:SS]\n')

for tube in tubes:
    barcode = tube.get_ID()
    status = tube.status().name
    ###### Tension Data
    # Returns the last tension record on the first day it was tensioned
    try:
        record = getFirstTensionRecord(tube.tension.get_record(mode='all'))
        first_tension = record.tension
        first_frequency = record.frequency
        first_tension_date = record.date 
    except:
        first_tension = None
        first_frequency = None
        first_tension_date = None

    # Returns the last tension record, this is defined as the second tension
    try:
        lastRecord = getLastTension(tube.tension.get_record(mode='all'))
        last_tension = lastRecord.tension
        last_frequency = lastRecord.frequency
        last_tension_date = lastRecord.date
    except:
        last_tension = None
        last_frequency = None
        last_tension_date = None

    ###### Leak Data
    try:
        leak = tube.leak.get_record().leak_rate
        leak_date = tube.leak.get_record().date
    except:
        leak = None
        leak_date = None

    ###### Dark current
    try:
        current = tube.current.get_record().dark_current
        current_date = tube.current.get_record().date
    except:
        current = None
        current_date = None

    ###### Swage Info
    try:
        swage_date = tube.swage.get_record().date
        raw_length = tube.swage.get_record().raw_length
        swage_length = tube.swage.get_record().swage_length
    except:
        swage_date = None
        raw_length = None
        swage_length = None
    f.write(f'{barcode},{status},{first_tension},{first_frequency},{first_tension_date},{last_tension},{last_frequency},{last_tension_date},')
    f.write(f'{leak},{leak_date},{current},{current_date},{raw_length},{swage_length},{swage_date}\n')

f.close()