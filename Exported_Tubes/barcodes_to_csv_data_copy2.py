import sys
import os
import datetime
DROPBOX_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(DROPBOX_DIR)

from sMDT import db

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



f = open("6-24-2021.txt")
lines = f.readlines()
f.close()

barcodes = []
for line in lines:
    if line == '': continue
    if line[0] != 'M': continue
    barcodes.append(line.replace("\n",""))

print(len(barcodes))
f = open("06.24.2021_09_15_00.csv","w")
f.write("Logger,Barcode,First Tension [g],Tension Frequency [Hz],First Tension Date [yyyy:mm:dd],Dark Current [nA],Leak Rate [mbar l/s]\n")
datab = db.db()
for barcode in barcodes:
    print(barcode)
    tube1 = datab.get_tube(barcode)
    firstTensionRecord = getFirstTensionRecord(tube1.tension.get_record(mode='all'))
    tension = firstTensionRecord.tension
    tensiond = firstTensionRecord.date.strftime("%Y:%m:%d")
    tensionf = firstTensionRecord.frequency
    dc = tube1.dark_current.get_record().dark_current
    leak = tube1.leak.get_record().leak_rate 
    f.write(f"Winston,{barcode},{tension},{tensionf},{tensiond},{dc},{leak}\n")
f.close()
