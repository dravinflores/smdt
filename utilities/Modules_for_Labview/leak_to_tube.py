from sMDT import db
from sMDT import tube as Tube
from sMDT.data.leak import LeakRecord

import sys
import datetime


def main(name, leak, barcode, date):
    date = datetime.datetime.strptime(date, '%m/%d/%Y%I:%M %p')

    datab = db.db()
    tube = Tube()
    tube.set_ID(barcode)
    tube.leak.add_record(LeakRecord(leak_rate=leak,
                                    date=date, 
                                    user=name))
    datab.add_tube(tube)